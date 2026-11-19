#!/usr/bin/env python3
"""corrija-antes — o relógio de quem defende.

Diagnóstico SÓ LEITURA da sua própria máquina e dos seus próprios repositórios, em 3 blocos:
  1. ATUALIZE  — o que está desatualizado (sistema, snap, npm global, imagens Docker) e há quantos dias
  2. VIGIE     — o que está escutando na rede, firewall, SSH e portas que o Docker publica
  3. SEUS BURACOS — segredos dentro do git, .env versionado e dependências paradas (--repo)

Não instala, não atualiza, não corrige, não varre outras máquinas e não chama nenhuma API.
Cada achado sai com uma prioridade: AGORA, SEMANA, OK ou SEM TESTE (não deu para conferir).

Uso:
  python3 relogio.py                          # máquina
  python3 relogio.py --repo ~/meu-app         # máquina + o repositório (repita --repo)
  python3 relogio.py --saida relatorio/       # grava relatorio.md e relatorio.json
  python3 relogio.py --blocos codigo --repo . # só um bloco (atualize, vigie, codigo)
  python3 relogio.py --mostrar-ips            # o relatório mostra IPs e nome da máquina (padrão: mascarado)
  python3 relogio.py --json                   # resultado em JSON na tela
Saída: 0 = nada para AGORA · 1 = tem item AGORA · 2 = erro de uso.
"""
import argparse
import datetime as dt
import glob
import ipaddress
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time

VERSAO = "1.0.4"
NIVEIS = ["AGORA", "SEMANA", "SEM TESTE", "OK"]
DIA = 86400

# Portas que nunca deveriam ficar abertas para todas as redes sem você saber.
PORTAS_CRITICAS = {
    2375: "API do Docker sem senha", 2376: "API do Docker", 3306: "MySQL", 5432: "PostgreSQL",
    5433: "PostgreSQL", 5434: "PostgreSQL", 6379: "Redis", 27017: "MongoDB", 9200: "Elasticsearch",
    11434: "Ollama (IA local sem senha)", 5900: "VNC (tela remota)", 5901: "VNC (tela remota)",
    3389: "RDP (tela remota)", 23: "Telnet", 21: "FTP", 445: "compartilhamento Windows (SMB)",
    8888: "Jupyter", 9000: "painel/MinIO", 9001: "painel/MinIO",
}


def achado(bloco, item, nivel, detalhe, corrigir=""):
    return {"bloco": bloco, "item": item, "nivel": nivel, "detalhe": detalhe, "corrigir": corrigir}


def rodar(cmd, timeout=90):
    """Roda um comando de leitura. Devolve (rc, saída) ou None se o programa não existe."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           env={**os.environ, "LC_ALL": "C", "LANG": "C"})
        return p.returncode, (p.stdout or "") + (p.stderr if p.returncode and not p.stdout else "")
    except subprocess.TimeoutExpired:
        return -1, "tempo esgotado"
    except OSError as e:
        return -1, str(e)


def ler(caminho):
    try:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def idade_dias(segundos_epoch, agora=None):
    agora = agora or time.time()
    return int((agora - segundos_epoch) // DIA)


# ───────────────────────── bloco 1: ATUALIZE ─────────────────────────

def parse_apt_upgradable(saida):
    """'pkg/noble-updates,noble-security 1.2 arm64 [upgradable from: 1.1]' → (total, seguranca, nomes_seg)."""
    total, seg, nomes = 0, 0, []
    for linha in saida.splitlines():
        m = re.match(r"^([^/\s]+)/(\S+)\s+\S+\s+\S+\s+\[upgradable from", linha)
        if not m:
            continue
        total += 1
        if "security" in m.group(2):
            seg += 1
            nomes.append(m.group(1))
    return total, seg, nomes


def parse_apt_history_ultima(texto):
    """Última 'Start-Date: 2026-11-01  10:02:03' do history.log → epoch ou None."""
    datas = re.findall(r"^Start-Date:\s+(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})", texto or "", re.M)
    if not datas:
        return None
    d, h = datas[-1]
    return dt.datetime.strptime(f"{d} {h}", "%Y-%m-%d %H:%M:%S").timestamp()


def checa_apt(agora=None):
    out = []
    r = rodar(["apt", "list", "--upgradable"])
    if r is None:
        return out
    rc, saida = r
    if rc not in (0,):
        return [achado("atualize", "Pacotes do sistema (apt)", "SEM TESTE", f"apt list falhou: {saida[:120]}")]
    total, seg, nomes = parse_apt_upgradable(saida)
    listas = [os.path.getmtime(p) for p in glob.glob("/var/lib/apt/lists/*Packages*")]
    velha = idade_dias(max(listas), agora) if listas else None
    nota = f" (lista de pacotes de {velha} dias atrás: rode `sudo apt update` para ver o que saiu depois)" \
        if velha is not None and velha > 3 else ""
    if seg:
        out.append(achado("atualize", "Correções de segurança do sistema (apt)", "AGORA",
                          f"{seg} pacote(s) com correção de segurança esperando, de {total} no total. "
                          f"Ex.: {', '.join(nomes[:6])}{nota}",
                          "Backup e saúde antes; depois `sudo apt update && sudo apt upgrade` e reinicie o que pedir."))
    elif total:
        out.append(achado("atualize", "Pacotes do sistema (apt)", "SEMANA",
                          f"{total} pacote(s) com versão nova, nenhuma marcada como segurança{nota}",
                          "`sudo apt upgrade` na janela da semana."))
    else:
        out.append(achado("atualize", "Pacotes do sistema (apt)", "SEMANA" if nota else "OK",
                          "nada pendente na lista local" + nota))
    # há quantos dias foi a última atualização instalada
    ultima = parse_apt_history_ultima(ler("/var/log/apt/history.log"))
    if ultima is None and os.path.exists("/var/log/dpkg.log"):
        ultima = os.path.getmtime("/var/log/dpkg.log")
    if ultima:
        dias = idade_dias(ultima, agora)
        nivel = "AGORA" if dias > 30 and seg else ("SEMANA" if dias > 7 else "OK")
        out.append(achado("atualize", "Última atualização instalada", nivel,
                          f"há {dias} dia(s). Em julho de 2026 quem defendia tinha de 4 a 7 meses de folga; "
                          "em outubro, num teste de invasão, essa folga foi a zero.",
                          "Atualizar toda semana, num dia fixo." if nivel != "OK" else ""))
    if os.path.exists("/var/run/reboot-required"):
        pk = (ler("/var/run/reboot-required.pkgs") or "").split()
        out.append(achado("atualize", "Reinício pendente", "SEMANA",
                          "o sistema atualizou peças que só valem depois de reiniciar"
                          + (f" ({', '.join(pk[:4])})" if pk else ""),
                          "Reinicie na janela de manutenção."))
    return out


def checa_dnf():
    r = rodar(["dnf", "-q", "check-update"], timeout=180)
    if r is None:
        return []
    rc, saida = r
    if rc == 0:
        return [achado("atualize", "Pacotes do sistema (dnf)", "OK", "nada pendente")]
    if rc == 100:
        n = len([l for l in saida.splitlines() if re.match(r"^\S+\.\S+\s+\S+\s+\S+", l)])
        rs = rodar(["dnf", "-q", "updateinfo", "list", "--security"], timeout=180)
        nseg = len([l for l in (rs[1] if rs else "").splitlines() if l.strip()])
        return [achado("atualize", "Pacotes do sistema (dnf)", "AGORA" if nseg else "SEMANA",
                       f"{n} pacote(s) com versão nova, {nseg} aviso(s) de segurança",
                       "Backup antes; depois `sudo dnf upgrade`.")]
    return [achado("atualize", "Pacotes do sistema (dnf)", "SEM TESTE", saida[:120])]


def checa_brew():
    r = rodar(["brew", "outdated", "--quiet"], timeout=180)
    if r is None:
        return []
    rc, saida = r
    itens = [l for l in saida.split() if l.strip()]
    if rc != 0:
        return [achado("atualize", "Homebrew", "SEM TESTE", saida[:120])]
    return [achado("atualize", "Homebrew", "SEMANA" if itens else "OK",
                   f"{len(itens)} programa(s) desatualizado(s)" + (f": {', '.join(itens[:6])}" if itens else ""),
                   "`brew upgrade`." if itens else "")]


def checa_macos():
    if platform.system() != "Darwin":
        return []
    r = rodar(["softwareupdate", "-l"], timeout=240)
    if r is None:
        return []
    rc, saida = r
    if "No new software available" in saida:
        return [achado("atualize", "macOS", "OK", "sistema em dia")]
    n = saida.count("* Label:")
    seg = bool(re.search(r"Security|Rapid|Segurança", saida))
    return [achado("atualize", "macOS", ("AGORA" if seg else "SEMANA") if n else "SEM TESTE",
                   f"{n} atualização(ões) do sistema esperando" if n else saida[:120],
                   "Ajustes do Sistema → Geral → Atualização de Software.")]


def parse_snap_refresh(saida):
    if "All snaps up to date" in saida:
        return []
    nomes = []
    for l in saida.splitlines()[1:]:
        p = l.split()
        if p:
            nomes.append(p[0])
    return nomes


def checa_snap():
    r = rodar(["snap", "refresh", "--list"])
    if r is None:
        return []
    rc, saida = r
    if rc != 0:
        return [achado("atualize", "Snaps", "SEM TESTE", saida.strip()[:120])]
    nomes = parse_snap_refresh(saida)
    return [achado("atualize", "Snaps", "SEMANA" if nomes else "OK",
                   f"{len(nomes)} snap(s) com versão nova: {', '.join(nomes[:6])}" if nomes else "todos em dia",
                   "`sudo snap refresh` (o snap também atualiza sozinho, mas pode estar adiado)." if nomes else "")]


def parse_npm_outdated(saida):
    try:
        d = json.loads(saida or "{}")
    except json.JSONDecodeError:
        return None
    return sorted(d.keys())


def checa_npm():
    r = rodar(["npm", "-g", "outdated", "--json"], timeout=120)
    if r is None:
        return []
    rc, saida = r
    nomes = parse_npm_outdated(saida)
    if nomes is None:
        return [achado("atualize", "Pacotes globais do npm", "SEM TESTE", "a resposta do npm não veio em JSON")]
    return [achado("atualize", "Pacotes globais do npm", "SEMANA" if nomes else "OK",
                   f"{len(nomes)} desatualizado(s): {', '.join(nomes[:6])}" if nomes else "todos em dia",
                   "`npm -g update` (ou `npm -g install <pacote>@latest`), um de cada vez." if nomes else "")]


def checa_docker_imagens(agora=None):
    r = rodar(["docker", "ps", "--format", "{{.Names}}|{{.Image}}"], timeout=30)
    if r is None:
        return []
    rc, saida = r
    if rc != 0:
        return [achado("atualize", "Imagens Docker em uso", "SEM TESTE",
                       "sem acesso ao Docker (usuário fora do grupo docker?)")]
    velhas, total = [], 0
    for linha in saida.splitlines():
        if "|" not in linha:
            continue
        nome, img = linha.split("|", 1)
        total += 1
        ri = rodar(["docker", "image", "inspect", "--format", "{{.Created}}", img], timeout=30)
        if not ri or ri[0] != 0:
            continue
        criada = ri[1].strip()[:19]
        try:
            ts = dt.datetime.strptime(criada, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc).timestamp()
        except ValueError:
            continue
        dias = idade_dias(ts, agora)
        if dias > 120:
            velhas.append(f"{nome} ({img}, {dias} dias)")
    if not total:
        return [achado("atualize", "Imagens Docker em uso", "OK", "nenhum container rodando")]
    return [achado("atualize", "Imagens Docker em uso", "SEMANA" if velhas else "OK",
                   f"{len(velhas)} de {total} container(s) com imagem de mais de 4 meses: {'; '.join(velhas[:5])}"
                   if velhas else f"{total} container(s), nenhuma imagem com mais de 4 meses",
                   "Backup dos volumes, `docker pull` da imagem nova, recriar o container e conferir." if velhas else "")]


# ───────────────────────── bloco 2: VIGIE ─────────────────────────

def classifica_endereco(host):
    """→ 'local' | 'todas' | 'interna' | 'publica'."""
    h = host.strip("[]").split("%")[0]
    if h in ("*", "0.0.0.0", "::", ""):
        return "todas"
    if h == "localhost":
        return "local"
    try:
        ip = ipaddress.ip_address(h)
    except ValueError:
        return "interna"
    if ip.is_loopback:
        return "local"
    if ip.is_private or ip.is_link_local or ip in ipaddress.ip_network("100.64.0.0/10"):
        return "interna"
    return "publica"


def parse_ss(saida):
    """Linhas de `ss -H -tlnp` → lista de (host, porta, processo)."""
    portas = []
    for linha in saida.splitlines():
        p = linha.split()
        if len(p) < 4:
            continue
        local = p[3]
        if ":" not in local:
            continue
        host, _, porta = local.rpartition(":")
        if not porta.isdigit():
            continue
        m = re.search(r'users:\(\("([^"]+)"', linha)
        proc = m.group(1).split()[0].split("/")[-1] if m and m.group(1).strip() else ""
        portas.append((host, int(porta), proc))
    return portas


def parse_lsof(saida):
    portas = []
    for linha in saida.splitlines()[1:]:
        p = linha.split()
        if len(p) < 9:
            continue
        host, _, porta = p[8].rpartition(":")
        if porta.isdigit():
            portas.append((host, int(porta), p[0]))
    return portas


def checa_portas(do_docker=()):
    if shutil.which("ss"):
        r = rodar(["ss", "-H", "-tlnp"])
        portas = parse_ss(r[1]) if r and r[0] == 0 else None
    elif shutil.which("lsof"):
        r = rodar(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"])
        portas = parse_lsof(r[1]) if r and r[0] == 0 else None
    else:
        portas = None
    if portas is None:
        return [achado("vigie", "Portas escutando", "SEM TESTE", "sem `ss` nem `lsof` para listar")], []
    vistas = {}
    for host, porta, proc in portas:
        cl = classifica_endereco(host)
        ordem = {"local": 0, "interna": 1, "todas": 2, "publica": 3}
        if porta not in vistas or ordem[cl] > ordem[vistas[porta][0]]:
            vistas[porta] = (cl, proc)
    out = []
    abertas = sorted(p for p, (cl, _) in vistas.items() if cl in ("todas", "publica"))
    criticas = [p for p in abertas if p in PORTAS_CRITICAS and p not in do_docker]
    locais = sorted(p for p, (cl, _) in vistas.items() if cl == "local")
    internas = sorted(p for p, (cl, _) in vistas.items() if cl == "interna")
    for p in criticas:
        proc = vistas[p][1]
        out.append(achado("vigie", f"Porta {p} aberta para a rede", "AGORA",
                          f"{PORTAS_CRITICAS[p]} escutando em todos os endereços"
                          + (f" (processo {proc})" if proc else "")
                          + ". Se o roteador ou a nuvem deixar passar, qualquer um na internet tenta entrar.",
                          "Se só você usa: prender em 127.0.0.1 na configuração do serviço. "
                          "Se outra máquina usa: liberar só o IP dela no firewall, e pôr senha."))
    outras = [p for p in abertas if p not in PORTAS_CRITICAS and p != 22 and p not in do_docker]
    if outras:
        out.append(achado("vigie", "Outras portas abertas para a rede", "SEMANA",
                          f"{len(outras)} porta(s) escutando em todos os endereços: "
                          + ", ".join(f"{p}{'/' + vistas[p][1] if vistas[p][1] else ''}" for p in outras[:15]),
                          "Para cada uma: precisa estar aberta? Se não, prender em 127.0.0.1 ou desligar o serviço."))
    out.append(achado("vigie", "Resumo das portas", "OK",
                      f"{len(locais)} só nesta máquina, {len(internas)} só na rede interna/VPN, "
                      f"{len(abertas)} abertas para qualquer rede"))
    return out, sorted(vistas)


def checa_firewall():
    sistema = platform.system()
    if sistema == "Darwin":
        r = rodar(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"])
        if r and "enabled" in r[1].lower():
            return [achado("vigie", "Firewall", "OK", "firewall do macOS ligado")]
        return [achado("vigie", "Firewall", "SEMANA", "firewall do macOS desligado ou sem leitura",
                       "Ajustes do Sistema → Rede → Firewall.")]
    conf = ler("/etc/ufw/ufw.conf")
    if conf is not None:
        if re.search(r"^ENABLED=yes", conf, re.M):
            return [achado("vigie", "Firewall (ufw)", "OK", "ufw ligado (confira as regras com `sudo ufw status`)")]
        return [achado("vigie", "Firewall (ufw)", "SEMANA", "ufw instalado mas DESLIGADO",
                       "Libere antes o que você usa (ex.: `sudo ufw allow OpenSSH`) e depois `sudo ufw enable`. "
                       "Atenção: portas publicadas pelo Docker passam por cima do ufw.")]
    r = rodar(["systemctl", "is-active", "firewalld"])
    if r and r[1].strip() == "active":
        return [achado("vigie", "Firewall (firewalld)", "OK", "firewalld ativo")]
    r = rodar(["systemctl", "is-active", "nftables"])
    if r and r[1].strip() == "active":
        return [achado("vigie", "Firewall (nftables)", "OK", "nftables ativo (confira as regras com `sudo nft list ruleset`)")]
    return [achado("vigie", "Firewall", "SEM TESTE", "não achei ufw, firewalld nem nftables ativos (pode haver firewall na nuvem/roteador)",
                   "Se for servidor na internet: ligue um firewall ou use o da nuvem.")]


def le_sshd(caminho="/etc/ssh/sshd_config", _prof=0):
    """Junta as linhas do sshd_config expandindo Include, na ordem (vale a 1ª ocorrência)."""
    texto = ler(caminho)
    if texto is None or _prof > 3:
        return []
    linhas = []
    for l in texto.splitlines():
        s = l.strip()
        if not s or s.startswith("#"):
            continue
        if s.lower().startswith("match "):
            break  # o que vem depois de Match vale só para alguns usuários; paramos aqui
        if s.lower().startswith("include "):
            for padrao in s.split()[1:]:
                if not padrao.startswith("/"):
                    padrao = os.path.join("/etc/ssh", padrao)
                for f in sorted(glob.glob(padrao)):
                    linhas += le_sshd(f, _prof + 1)
            continue
        linhas.append(s)
    return linhas


def valor_sshd(linhas, chave, padrao):
    for s in linhas:
        p = s.split(None, 1)
        if len(p) == 2 and p[0].lower() == chave.lower():
            return p[1].strip().lower()
    return padrao


def checa_ssh(portas_vistas):
    if not os.path.exists("/etc/ssh/sshd_config"):
        return []
    if 22 not in portas_vistas:
        return [achado("vigie", "SSH", "OK", "servidor SSH instalado mas não escutando na porta 22")]
    linhas = le_sshd()
    if not linhas:
        return [achado("vigie", "SSH", "SEM TESTE", "não consegui ler o sshd_config (confira com `sudo sshd -T`)")]
    senha = valor_sshd(linhas, "PasswordAuthentication", "yes")
    root = valor_sshd(linhas, "PermitRootLogin", "prohibit-password")
    out = []
    if senha == "yes":
        out.append(achado("vigie", "SSH aceita senha", "AGORA",
                          "o SSH aceita login por senha: é a porta que robôs testam com milhares de senhas por dia",
                          "Entre com chave, confirme que funciona, e então `PasswordAuthentication no` + reiniciar o ssh."))
    if root == "yes":
        out.append(achado("vigie", "SSH aceita root com senha", "AGORA", "PermitRootLogin yes",
                          "Troque para `PermitRootLogin prohibit-password` (ou `no`)."))
    if not out:
        out.append(achado("vigie", "SSH", "OK", f"senha desligada, root: {root}"))
    return out


def parse_docker_ports(saida):
    """'nome|0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp' → [(nome, porta_host)] só das abertas a todos."""
    abertas = []
    for linha in saida.splitlines():
        if "|" not in linha:
            continue
        nome, portas = linha.split("|", 1)
        for m in re.finditer(r"(0\.0\.0\.0|\[::\]|::):(\d+)(?:-(\d+))?->", portas):
            ini = int(m.group(2))
            fim = int(m.group(3) or ini)
            for p in range(ini, min(fim, ini + 20) + 1):
                if (nome, p) not in abertas:
                    abertas.append((nome, p))
    return abertas


def checa_docker_portas():
    r = rodar(["docker", "ps", "--format", "{{.Names}}|{{.Ports}}"], timeout=30)
    if r is None or r[0] != 0:
        return []
    abertas = parse_docker_ports(r[1])
    if not abertas:
        return [achado("vigie", "Portas publicadas pelo Docker", "OK", "nenhum container publicado em todos os endereços")]
    criticas = [(n, p) for n, p in abertas if p in PORTAS_CRITICAS]
    nivel = "AGORA" if criticas else "SEMANA"
    lista = ", ".join(f"{n}:{p}" for n, p in (criticas or abertas)[:10])
    return [achado("vigie", "Portas publicadas pelo Docker", nivel,
                   f"{len(abertas)} porta(s) de container abertas para qualquer rede ({lista}). "
                   "O Docker abre essas portas POR CIMA do ufw.",
                   "No compose, troque `\"5432:5432\"` por `\"127.0.0.1:5432:5432\"` quando só a máquina usa.")]


# ───────────────────────── bloco 3: SEUS BURACOS ─────────────────────────

SEGREDOS = [
    ("chave AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("chave OpenAI/Anthropic", re.compile(r"\bsk-(?:ant-(?:api\d\d-)?|proj-|svcacct-|or-v1-)?[A-Za-z0-9_\-]{20,}")),
    ("chave Stripe", re.compile(r"\b[sr]k_(?:live|test)_[0-9A-Za-z]{20,}")),
    ("token GitHub", re.compile(r"\b(?:ghp|gho|ghs|ghu|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}")),
    ("token Slack", re.compile(r"\bxox[abpr]-[A-Za-z0-9\-]{10,}")),
    ("chave Google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("token Telegram", re.compile(r"\b\d{8,10}:AA[0-9A-Za-z_\-]{33}\b")),
    ("token Mercado Pago", re.compile(r"\bAPP_USR-\d{6,}-\d{6}-[0-9a-f]{32}-\d{6,}")),
    ("chave Groq", re.compile(r"\bgsk_[A-Za-z0-9]{40,}")),
    ("token Hugging Face", re.compile(r"\bhf_[A-Za-z0-9]{30,}")),
    ("token GitLab", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}")),
    ("chave SendGrid", re.compile(r"\bSG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{30,}")),
    ("chave service_role do Supabase", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}")),
    ("webhook do Slack", re.compile(r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]{20,}")),
    ("token npm", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("chave Resend", re.compile(r"\bre_[A-Za-z0-9]{6,}_[A-Za-z0-9]{12,}")),
    ("senha/chave do WordPress", re.compile(r"define\(\s*['\"](?:DB_PASSWORD|(?:SECURE_AUTH|LOGGED_IN|NONCE|AUTH)_(?:KEY|SALT))['\"]\s*,\s*['\"][^'\"]{4,}['\"]")),
    ("senha em endereço de banco", re.compile(r"\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|amqp)://[^:\s/@]*:[^@\s/]{4,}@[^\s'\"]+")),
    ("chave privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED |PGP )?PRIVATE KEY(?: BLOCK)?-----")),
]
EXEMPLO_ENV = re.compile(r"\.(example|sample|exemplo|template|dist)$", re.I)
PREFIXO = re.compile(r"^(sk-(ant-(api\d\d-)?|proj-|svcacct-|or-v1-)?|[sr]k_(live|test)_|AKIA|AIza|gh[pousr]_|github_pat_|xox[abpr]-)")


def lista(itens, n=30):
    return "; ".join(itens[:n]) + (f"; … e mais {len(itens) - n} (lista inteira em relatorio.json, campo itens)" if len(itens) > n else "")


def mascara(s):
    return s[:4] + "…" + f"({len(s)} caracteres)"


def parece_chave(tipo, token, prox_linha="", resto=""):
    """Descarta o que só tem o formato: classe CSS 'sk-spinner-wave', cabeçalho de chave sem a chave,
    endereço de banco com senha de mentira (${VAR}, <senha>, password)."""
    if tipo == "chave privada":   # a chave vem na linha de baixo, ou na mesma linha depois de \n (JSON do Google)
        return bool(re.fullmatch(r"\s*[A-Za-z0-9+/=]{40,}\s*", prox_linha) or re.match(r"(\\n)+[A-Za-z0-9+/=]{40,}", resto))
    if tipo == "senha em endereço de banco":
        senha = token.split("://", 1)[1].split("@", 1)[0].split(":", 1)[1]
        return not re.search(r"^[$<{%]|senha|password|pass|secret|xxx|user|usuario|\*\*\*", senha, re.I)
    if tipo == "chave service_role do Supabase":
        import base64
        try:
            meio = token.split(".")[1]
            dados = base64.urlsafe_b64decode(meio + "=" * (-len(meio) % 4)).decode("utf-8", "replace")
        except (ValueError, IndexError):
            return False
        return '"service_role"' in dados   # a anon key é pública por desenho; só a service_role é segredo
    if tipo == "senha/chave do WordPress":
        return not re.search(r"put your unique phrase here|password_here|senha_aqui|^[$<{%]", token, re.I)
    if tipo == "chave Resend":
        corpo = token[3:]
        return bool(re.search(r"\d", corpo) and re.search(r"[A-Z]", corpo) and re.search(r"[a-z]", corpo))
    if tipo != "chave OpenAI/Anthropic":
        return True
    m = PREFIXO.match(token)
    corpo = PREFIXO.sub("", token)
    if m.group(0) == "sk-" and re.fullmatch(r"[0-9a-f]{32}", corpo):
        return True    # DeepSeek: sk- + 32 hexadecimais
    if m.group(0) == "sk-or-v1-":
        return bool(re.fullmatch(r"[0-9a-f]{64}", corpo))   # OpenRouter
    if m.group(0) == "sk-" and ("-" in corpo or len(corpo) < 32):
        return False   # chave antiga da OpenAI: sk- + 48 letras/números, sem hífen
    return bool(re.search(r"\d", corpo) and re.search(r"[A-Z]", corpo) and re.search(r"[a-z]", corpo))


def procura_segredos(texto, arquivo=""):
    """→ [(tipo, linha, trecho_mascarado, parece_exemplo)]"""
    achou = []
    linhas = texto.splitlines()
    for n, linha in enumerate(linhas, 1):
        if len(linha) > 2000:
            linha = linha[:2000]
        prox = linhas[n] if n < len(linhas) else ""
        for tipo, rx in SEGREDOS:
            for m in rx.finditer(linha):
                if parece_chave(tipo, m.group(0), prox[:2000], linha[m.end():m.end() + 200]):
                    tok = m.group(0)
                    trecho = re.search(r"[A-Z_]{6,}", tok).group(0) if tipo == "senha/chave do WordPress" else mascara(tok)
                    achou.append((tipo, n, trecho, parece_exemplo(arquivo, linha, tok, tipo)))
                    break
    return achou


CAMINHO_EXEMPLO = re.compile(r"(^|/)(tests?|testes?|spec|__tests__|fixtures?|mocks?|exemplos?|examples?|amostras?)(/|$)|(_test|\.test|\.spec|_spec)\.", re.I)
PALAVRA_EXEMPLO = re.compile(r"\b(exemplo|example|fake|dummy|placeholder|teste|test|xxxx+|your[_-]?(api[_-]?)?key|sua[_-]?chave)\b", re.I)


def baixa_variedade(token):
    """Valor de mentira: poucos caracteres diferentes (Ab1Ab1…) ou sequência (abcdefgh, 123456)."""
    corpo = PREFIXO.sub("", token)
    if len(corpo) >= 12 and len(set(corpo)) < 10:   # contagem absoluta: chave longa de verdade tem dezenas
        return True
    seq = maior = 1
    for x, y in zip(corpo, corpo[1:]):
        seq = seq + 1 if ord(y) - ord(x) == 1 else 1
        maior = max(maior, seq)
    return maior >= 6


SENHAS_FRACAS = {"postgres", "root", "admin", "password", "senha", "123456", "12345678", "secret", "dev", "test",
                 "teste", "mysql", "redis", "guest", "changeme", "example"}


def parece_exemplo(arquivo, linha_txt, token, tipo=""):
    """Chave de mentira: o valor diz EXAMPLE/fake (ex.: AKIAIOSFODNN7EXAMPLE, a de exemplo da AWS), valor
    repetitivo ou em sequência, a variável ao lado diz exemplo/test, ou arquivo de teste. Chave de produção
    (sk_live_) não é rebaixada pela pasta. Chave em docs/ ou .env.example com valor de verdade continua AGORA."""
    if re.search(r"example|exemplo|fake|dummy|xxxx|your|here|goes|replace|seu[_-]|sua[_-]|aqui", token, re.I):
        return True
    if tipo == "senha em endereço de banco":
        usuario, senha = token.split("://", 1)[1].split("@", 1)[0].split(":", 1)
        host = token.split("@", 1)[1]
        return senha.lower() in SENHAS_FRACAS or senha == usuario or bool(
            re.match(r"(localhost|127\.0\.0\.1|0\.0\.0\.0|db|postgres|mysql|redis)([:/]|$)", host)) or bool(
            CAMINHO_EXEMPLO.search(arquivo))
    if tipo not in ("token Mercado Pago",) and baixa_variedade(token):
        return True
    i = linha_txt.find(token)
    perto = linha_txt[max(0, i - 40):i] if i >= 0 else ""
    if PALAVRA_EXEMPLO.search(perto):
        return True
    return bool(CAMINHO_EXEMPLO.search(arquivo)) and not re.match(r"[sr]k_live_", token)


def env_versionados(arquivos):
    """.env*, menos os de exemplo. (wp-config.php só acusa se tiver senha escrita: regra de conteúdo.)"""
    return [a for a in arquivos
            if re.search(r"(^|/)\.env(\.[^/]*)?$", a) and not EXEMPLO_ENV.search(a)]


def checa_repo(caminho, agora=None):
    nome = os.path.basename(os.path.abspath(caminho)) or caminho
    b = "codigo"
    r = rodar(["git", "-C", caminho, "ls-files", "-z"])
    if r is None or r[0] != 0:
        return [achado(b, f"Repositório {nome}", "SEM TESTE", "não é um repositório git (ou o git não está instalado)")]
    arquivos = [a for a in r[1].split("\0") if a]
    out = []
    envs = env_versionados(arquivos)
    if envs:
        out.append(achado(b, f"{nome}: .env dentro do git", "AGORA",
                          f"{len(envs)} arquivo(s) de senhas versionado(s): {', '.join(envs[:5])}",
                          "Troque TODAS as chaves que estão nele (já estão no histórico), depois "
                          "`git rm --cached <arquivo>` e ponha `.env` e `.env.*` (ou `wp-config.php`) no .gitignore."))
    ci = rodar(["git", "-C", caminho, "check-ignore", "-q", "--no-index", ".env"])
    if ci and ci[0] == 1:
        out.append(achado(b, f"{nome}: .gitignore sem .env", "SEMANA",
                          "o git não ignora o .env: um `git add .` distraído sobe as suas chaves",
                          "Acrescente uma linha `.env` (e `.env.*`) no .gitignore e confira com `git check-ignore -v .env`."))
    segredos, exemplos, grandes = [], [], []
    for a in arquivos:
        p = os.path.join(caminho, a)
        try:
            if not os.path.isfile(p):
                continue
            if os.path.getsize(p) > 1_000_000:
                with open(p, "rb") as f:
                    if b"\0" not in f.read(4096):
                        grandes.append(a)
                continue
            with open(p, "rb") as f:
                bruto = f.read()
        except OSError:
            continue
        if b"\0" in bruto[:4096]:
            continue
        for tipo, linha, trecho, ex in procura_segredos(bruto.decode("utf-8", "replace"), a):
            nota = " (arquivo de exemplo com chave que parece real)" if EXEMPLO_ENV.search(a) and not ex else ""
            (exemplos if ex else segredos).append(f"{a}:{linha} {tipo} {trecho}{nota}")
    if segredos:
        out.append(achado(b, f"{nome}: segredo escrito no código", "AGORA",
                          f"{len(segredos)} ocorrência(s): " + lista(segredos),
                          "Troque a chave no painel do serviço (apagar do arquivo não basta: ela fica no histórico) "
                          "e leia de variável de ambiente."))
        out[-1]["itens"] = segredos
    if exemplos:
        out.append(achado(b, f"{nome}: chave com cara de exemplo", "SEMANA",
                          f"{len(exemplos)} ocorrência(s) em teste ou marcadas como exemplo, provavelmente falsas: "
                          + lista(exemplos),
                          "Abra cada linha e confirme que não é uma chave de verdade."))
        out[-1]["itens"] = exemplos
    if grandes:
        out.append(achado(b, f"{nome}: arquivos grandes não conferidos", "SEM TESTE",
                          f"{len(grandes)} arquivo(s) de texto acima de 1 MB ficaram fora da busca de segredos: "
                          + ", ".join(grandes[:5]),
                          "Abra ou procure neles à mão (ex.: `grep -n 'sk-\\|AKIA\\|BEGIN' <arquivo>`)."))
    travas = [a for a in arquivos if os.path.basename(a) in (
        "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "requirements.txt", "poetry.lock",
        "uv.lock", "Pipfile.lock", "composer.lock", "Gemfile.lock", "go.sum", "Cargo.lock")]
    paradas = []
    for t in travas[:10]:
        rl = rodar(["git", "-C", caminho, "log", "-1", "--format=%ct", "--", t])
        if rl and rl[0] == 0 and rl[1].strip().isdigit():
            dias = idade_dias(int(rl[1].strip()), agora)
            if dias > 120:
                paradas.append(f"{t} ({dias} dias)")
    if paradas:
        out.append(achado(b, f"{nome}: dependências paradas", "SEMANA",
                          f"lista de dependências sem mudança há mais de 4 meses: {', '.join(paradas[:5])}",
                          "Rode o auditor do seu gerenciador (`npm audit`, `pip-audit`, `composer audit`…) e atualize."))
    if not out:
        out.append(achado(b, f"Repositório {nome}", "OK",
                          f"{len(arquivos)} arquivo(s) conferido(s): sem .env, sem segredo conhecido, dependências recentes"))
    out.append(achado(b, f"{nome}: lembrete — revisão com IA", "OK",
                      "o script só acha o óbvio; a revisão que pega lógica errada (login, permissão, preço) é com IA",
                      "Use o prompt de `prompts/revisao-com-ia.md` no Claude Code, no Codex ou num modelo local."))
    return out


# ───────────────────────── relatório ─────────────────────────

def mascarar_texto(texto, mostrar):
    if mostrar:
        return texto
    texto = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", lambda m: m.group(0) if m.group(0).startswith(("127.", "0.0.0.0")) else "x.x.x.x", texto)
    host = socket.gethostname()
    if host and len(host) > 2:
        texto = texto.replace(host, "esta-maquina")
    usuario = os.environ.get("USER", "")
    if usuario and len(usuario) > 2:
        texto = re.sub(rf"\b{re.escape(usuario)}\b", "voce", texto)
    return texto


def resumo(achados):
    return {n: sum(1 for a in achados if a["nivel"] == n) for n in NIVEIS}


def para_markdown(achados, data):
    r = resumo(achados)
    l = [f"# Relógio de quem defende — {data}", "",
         f"**{r['AGORA']} para AGORA · {r['SEMANA']} para esta SEMANA · {r['SEM TESTE']} sem teste · {r['OK']} ok**", "",
         "Gerado por `relogio.py` (corrija-antes), só leitura. IPs e nome da máquina mascarados.", ""]
    titulos = {"atualize": "1. Atualize", "vigie": "2. Vigie a rede", "codigo": "3. Seus buracos (código)"}
    for bloco, t in titulos.items():
        dob = [a for a in achados if a["bloco"] == bloco]
        if not dob:
            continue
        l += [f"## {t}", "", "| Prioridade | Item | O que vi | O que fazer |", "|---|---|---|---|"]
        for a in sorted(dob, key=lambda a: NIVEIS.index(a["nivel"])):
            cel = [a["nivel"], a["item"], a["detalhe"], a["corrigir"] or "—"]
            l.append("| " + " | ".join(c.replace("|", "\\|") for c in cel) + " |")
        l.append("")
    l += ["## Antes de corrigir", "",
          "1. Backup do que importa (banco, volumes, configuração).",
          "2. Confira que o sistema está saudável ANTES (assim você sabe se a atualização quebrou algo).",
          "3. Corrija um item por vez e teste.", ""]
    return "\n".join(l)


def imprime(achados):
    cores = {"AGORA": "\033[31m", "SEMANA": "\033[33m", "SEM TESTE": "\033[35m", "OK": "\033[32m"}
    fim = "\033[0m" if sys.stdout.isatty() else ""
    if not sys.stdout.isatty():
        cores = {k: "" for k in cores}
    for bloco, t in (("atualize", "ATUALIZE"), ("vigie", "VIGIE A REDE"), ("codigo", "SEUS BURACOS")):
        dob = sorted([a for a in achados if a["bloco"] == bloco], key=lambda a: NIVEIS.index(a["nivel"]))
        if not dob:
            continue
        print(f"\n== {t} ==")
        for a in dob:
            print(f"  {cores[a['nivel']]}[{a['nivel']}]{fim} {a['item']}: {a['detalhe']}")
            if a["corrigir"] and (a["nivel"] != "OK" or "lembrete" in a["item"]):
                print(f"      → {a['corrigir']}")
    r = resumo(achados)
    print(f"\nResumo: {r['AGORA']} AGORA · {r['SEMANA']} SEMANA · {r['SEM TESTE']} SEM TESTE · {r['OK']} OK")


def main(argv=None):
    ap = argparse.ArgumentParser(description="corrija-antes: diagnóstico só leitura (atualize, vigie, seus buracos)")
    ap.add_argument("--repo", action="append", default=[], help="repositório git seu para conferir (repita)")
    ap.add_argument("--blocos", default="atualize,vigie,codigo", help="atualize,vigie,codigo")
    ap.add_argument("--saida", help="pasta para gravar relatorio.md e relatorio.json")
    ap.add_argument("--json", action="store_true", help="imprime o resultado em JSON")
    ap.add_argument("--mostrar-ips", action="store_true", help="não mascara IPs, usuário e nome da máquina")
    ap.add_argument("--versao", action="store_true")
    a = ap.parse_args(argv)
    if a.versao:
        print(VERSAO)
        return 0
    blocos = {b.strip() for b in a.blocos.split(",") if b.strip()}
    if not blocos <= {"atualize", "vigie", "codigo"}:
        print("--blocos aceita: atualize, vigie, codigo", file=sys.stderr)
        return 2
    achados = []
    if "atualize" in blocos:
        for f in (checa_apt, checa_dnf, checa_brew, checa_macos, checa_snap, checa_npm, checa_docker_imagens):
            achados += f()
    if "vigie" in blocos:
        rd = rodar(["docker", "ps", "--format", "{{.Names}}|{{.Ports}}"], timeout=30)
        do_docker = {p for _, p in parse_docker_ports(rd[1])} if rd and rd[0] == 0 else set()
        ps, vistas = checa_portas(do_docker)
        achados += ps + checa_firewall() + checa_ssh(vistas) + checa_docker_portas()
    if "codigo" in blocos:
        if not a.repo:
            achados.append(achado("codigo", "Seus repositórios", "SEM TESTE",
                                  "nenhum repositório informado", "Rode de novo com `--repo <pasta do seu projeto>`."))
        for rp in a.repo:
            achados += checa_repo(os.path.expanduser(rp))
    for x in achados:
        for k in ("detalhe", "corrigir", "item"):
            x[k] = mascarar_texto(x[k], a.mostrar_ips)
    data = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    if a.json:
        print(json.dumps({"versao": VERSAO, "data": data, "resumo": resumo(achados), "achados": achados},
                         ensure_ascii=False, indent=2))
    else:
        print(f"corrija-antes {VERSAO} — relógio de quem defende — {data} (só leitura)")
        imprime(achados)
    if a.saida:
        os.makedirs(a.saida, exist_ok=True)
        with open(os.path.join(a.saida, "relatorio.md"), "w", encoding="utf-8") as f:
            f.write(para_markdown(achados, data))
        with open(os.path.join(a.saida, "relatorio.json"), "w", encoding="utf-8") as f:
            json.dump({"versao": VERSAO, "data": data, "resumo": resumo(achados), "achados": achados},
                      f, ensure_ascii=False, indent=2)
        if not a.json:
            print(f"Relatório: {os.path.join(a.saida, 'relatorio.md')}")
    return 1 if any(x["nivel"] == "AGORA" for x in achados) else 0


if __name__ == "__main__":
    sys.exit(main())
