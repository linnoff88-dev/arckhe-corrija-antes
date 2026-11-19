#!/usr/bin/env python3
"""Testes do relogio.py com dados inventados (nada da sua máquina). Uso: python3 testes/run.py"""
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import relogio as R  # noqa: E402

falhas = []


def confere(nome, cond):
    print(("ok   " if cond else "FALHA ") + nome)
    if not cond:
        falhas.append(nome)


# ── apt ──
APT = """Listing...
openssl/noble-updates,noble-security 3.0.13-0ubuntu3.6 arm64 [upgradable from: 3.0.13-0ubuntu3.4]
curl/noble-updates 8.5.0-2ubuntu10.7 arm64 [upgradable from: 8.5.0-2ubuntu10.6]
libssh-4/noble-security 0.10.6-2ubuntu0.2 arm64 [upgradable from: 0.10.6-2]
"""
t, s, n = R.parse_apt_upgradable(APT)
confere("apt: 3 pendentes, 2 de segurança", (t, s, n) == (3, 2, ["openssl", "libssh-4"]))
confere("apt: lista vazia", R.parse_apt_upgradable("Listing...\n") == (0, 0, []))
H = "Start-Date: 2026-10-01  09:00:00\nCommandline: apt upgrade\nEnd-Date: x\n\nStart-Date: 2026-11-02  10:30:00\n"
confere("apt: última data do history.log", R.idade_dias(R.parse_apt_history_ultima(H),
        R.parse_apt_history_ultima("Start-Date: 2026-11-12  10:30:00")) == 10)
confere("apt: history vazio → None", R.parse_apt_history_ultima("") is None)

# ── snap / npm ──
confere("snap em dia", R.parse_snap_refresh("All snaps up to date.") == [])
confere("snap com 2", R.parse_snap_refresh("Name Version Rev Size Publisher Notes\nfirefox 1 2 3 mozilla -\ncore24 1 2 3 canonical base\n") == ["firefox", "core24"])
confere("npm outdated JSON", R.parse_npm_outdated('{"b":{},"a":{}}') == ["a", "b"])
confere("npm vazio", R.parse_npm_outdated("") == [])
confere("npm lixo → None", R.parse_npm_outdated("npm ERR!") is None)

# ── endereços ──
casos = {"127.0.0.1": "local", "[::1]": "local", "0.0.0.0": "todas", "*": "todas", "[::]": "todas",
         "192.168.0.10": "interna", "10.1.2.3": "interna", "100.64.5.6": "interna",
         "[fe80::1%eth0]": "interna", "8.8.8.8": "publica", "localhost": "local"}
confere("classifica 11 endereços", all(R.classifica_endereco(k) == v for k, v in casos.items()))

SS = """LISTEN 0 4096 127.0.0.1:5432 0.0.0.0:*
LISTEN 0 511 0.0.0.0:6379 0.0.0.0:* users:(("redis-server",pid=10,fd=6))
LISTEN 0 128 [::]:22 [::]:*
LISTEN 0 50 *:8080 *:* users:(("node /home/fulano/app",pid=11,fd=3))
"""
ps = R.parse_ss(SS)
confere("ss: 4 portas", [p for _, p, _ in ps] == [5432, 6379, 22, 8080])
confere("ss: processo sem caminho", ps[1][2] == "redis-server" and ps[3][2] == "node")

# checa_portas com ss falso
orig = R.rodar
R.rodar = lambda cmd, timeout=90: (0, SS) if cmd[0] == "ss" else orig(cmd, timeout)
saida, vistas = R.checa_portas()
R.rodar = orig
itens = {a["item"]: a["nivel"] for a in saida}
confere("portas: Redis aberto = AGORA", itens.get("Porta 6379 aberta para a rede") == "AGORA")
confere("portas: Postgres local não acusa", "Porta 5432 aberta para a rede" not in itens)
confere("portas: 8080 vai em SEMANA", itens.get("Outras portas abertas para a rede") == "SEMANA")
confere("portas: 22 fica para o bloco SSH", 22 in vistas)

# ── docker ──
DP = "db|0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp\nweb|127.0.0.1:3000->3000/tcp\nminio|0.0.0.0:9000-9001->9000-9001/tcp\nx|8080/tcp\n"
confere("docker: só as abertas a todos", R.parse_docker_ports(DP) == [("db", 5432), ("minio", 9000), ("minio", 9001)])

# ── sshd ──
with tempfile.TemporaryDirectory() as d:
    os.makedirs(os.path.join(d, "conf.d"))
    open(os.path.join(d, "conf.d", "10-x.conf"), "w").write("PasswordAuthentication no\n")
    principal = os.path.join(d, "sshd_config")
    open(principal, "w").write(f"Include {d}/conf.d/*.conf\nPasswordAuthentication yes\nPermitRootLogin yes\nMatch User git\n  PasswordAuthentication yes\n")
    linhas = R.le_sshd(principal)
    confere("sshd: Include vem antes e vence", R.valor_sshd(linhas, "PasswordAuthentication", "yes") == "no")
    confere("sshd: lê PermitRootLogin", R.valor_sshd(linhas, "PermitRootLogin", "x") == "yes")
    confere("sshd: padrão quando ausente", R.valor_sshd([], "PasswordAuthentication", "yes") == "yes")

# ── segredos ──
AWS = "AKIA" + "Q7RTZB2M4XWN8KPL"
GH = "ghp_" + "9fK2xQ7mZ3vB8nL1pR4tY6wE0aS5dG7hJ2kC"
confere("segredo AWS achado", R.procura_segredos(f'k = "{AWS}"', "app.py")[0][0] == "chave AWS")
confere("segredo mascarado", AWS not in str(R.procura_segredos(f'k = "{AWS}"', "app.py")))
confere("token GitHub achado", R.procura_segredos(f"TOKEN={GH}", "deploy.sh")[0][0] == "token GitHub")
CORPO_PEM = "b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW"
confere("chave privada achada", R.procura_segredos("-----BEGIN OPENSSH PRIVATE KEY-----\n" + CORPO_PEM, "id")[0][0] == "chave privada")
confere("só o cabeçalho da chave não acusa", R.procura_segredos('if pem.startswith("-----BEGIN RSA PRIVATE KEY-----"):', "a.py") == [])
confere("pasta testes/ = exemplo", R.procura_segredos(f'"{AWS}"', "testes/test_pag.py")[0][3] is True)
confere("sk-learn-Classifier2Model não é chave", R.procura_segredos("sk-learn-Classifier2Model-Version2x", "a.py") == [])
confere("senha em URL de banco", R.procura_segredos("DB=postgres://loja:Qz8vK2mR7t@db.loja.com/prod", "a.py")[0][0] == "senha em endereço de banco")
confere("URL de banco com ${VAR} não acusa", R.procura_segredos("DB=postgres://loja:${DB_PASS}@db/prod", "a.py") == [])
confere("Mercado Pago", R.procura_segredos("APP_USR-1234567-111222-" + "a1b2c3d4e5f60718293a4b5c6d7e8f90" + "-7654321", "a.py")[0][0] == "token Mercado Pago")
for nome, tok in (("chave Groq", "gsk_" + "Qz8vN2kR7tB4mW9xL3pC6yH1dF5gJ0sAbCdEfGhIj"),
                  ("token Hugging Face", "hf_" + "Qz8vN2kR7tB4mW9xL3pC6yH1dF5gJ0sA"),
                  ("token GitLab", "glpat-" + "Qz8vN2kR7tB4mW9xL3pC")):
    confere(nome, R.procura_segredos(f"k={tok}", "a.py")[0][0] == nome)
import base64, json as _j
def _jwt(role):
    b = lambda d: base64.urlsafe_b64encode(_j.dumps(d).encode()).decode().rstrip("=")
    return b({"alg": "HS256", "typ": "JWT"}) + "." + b({"iss": "supabase", "ref": "abcdefghijklmnop", "role": role, "iat": 1700000000}) + ".Qz8vN2kR7tB4mW9xL3pC6yH1dF5gJ0sA"
confere("Supabase service_role achada", R.procura_segredos(f'k="{_jwt("service_role")}"', "src/config.js")[0][0] == "chave service_role do Supabase")
confere("Supabase anon (pública) não acusa", R.procura_segredos(f'k="{_jwt("anon")}"', "src/config.js") == [])
confere("webhook do Slack", R.procura_segredos("u='https://hooks.slack.com/services/T0ABC123/B0DEF456/Qz8vN2kR7tB4mW9xL3pC6yH1'", "a.js")[0][0] == "webhook do Slack")
confere("token npm", R.procura_segredos("//registry.npmjs.org/:_authToken=npm_" + "Qz8vN2kR7tB4mW9xL3pC6yH1dF5gJ0sAbCdE", ".npmrc")[0][0] == "token npm")
confere("chave Resend", R.procura_segredos("RESEND=re_" + "Qz8vN2kR_7tB4mW9xL3pC6yH1", "a.py")[0][0] == "chave Resend")
confere("re_compile_pattern não é chave", R.procura_segredos("x = re_compile_patternsWithStuff", "a.py") == [])
confere("wp-config com senha", R.procura_segredos("define( 'DB_PASSWORD', 'Qz8vN2kR7t' );", "wp-config.php")[0][0] == "senha/chave do WordPress")
confere("wp-config de modelo não acusa", R.procura_segredos("define( 'AUTH_KEY', 'put your unique phrase here' );", "wp-config-sample.php") == [])
confere("wp-config só com getenv não acusa", R.procura_segredos("define( 'DB_PASSWORD', getenv('DB_PASSWORD') );", "wp-config.php") == [] and R.env_versionados(["wp-config.php"]) == [])
MP = "APP_USR-1234567-111222-" + "a1b2c3d4e5f60718293a4b5c6d7e8f90" + "-7654321"
confere("Mercado Pago real não vira exemplo", R.procura_segredos(f"MP={MP}", "src/pay.js")[0][3] is False)
confere("AKIAIOSFODNN7EXAMPLE = exemplo", R.procura_segredos("aws_access_key_id = AKIAIOSFODNN7EXAMPLE", "docs/deploy.md")[0][3] is True)
confere("postgres:postgres@localhost = exemplo", R.procura_segredos("DB=postgres://postgres:postgres@localhost:5432/dev", "a.py")[0][3] is True)
confere("sk_live em testes/ continua real", R.procura_segredos('STRIPE="sk_live_' + '51Hq8ZkR2vB7nM4xL9pC3tY6"', "testes/fixture.py")[0][3] is False)
confere("comentário longe com 'test' não rebaixa", R.procura_segredos('k = "sk_live_' + '51Hq8ZkR2vB7nM4xL9pC3tY6"' + "  # usado em test e prod", "src/a.py")[0][3] is False)
import random
random.seed(7)
_b = lambda n: "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for _ in range(n))
_jl = _jwt("service_role").rsplit(".", 1)[0] + "." + _b(180)
confere("service_role longa continua real", R.procura_segredos(f'k="{_jl}"', "src/config.py")[0][3] is False)
confere("sk_live_ de 200 caracteres continua real", R.procura_segredos("k=sk_live_" + _b(200), "src/a.py")[0][3] is False)
confere("xoxb-your-bot-token-here = exemplo", all(x[3] for x in R.procura_segredos("SLACK_TOKEN=xoxb-your-bot-token-here", "README.md")))
confere("ghp_YourPersonalAccessTokenGoesHere = exemplo", all(x[3] for x in R.procura_segredos("ghp_YourPersonalAccessTokenGoesHere123", "README.md")))
_sa = '"private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7' + _b(40) + '\\n-----END PRIVATE KEY-----\\n",'
confere("chave privada no JSON do Google", R.procura_segredos(_sa, "firebase-sa.json")[0][0] == "chave privada")
confere("redis://:senha@ sem usuário", R.procura_segredos("REDIS=redis://:Qz8vK2mR7tB@cache.loja.com:6379", "a.py")[0][0] == "senha em endereço de banco")
confere("DeepSeek sk-<32 hex>", R.procura_segredos("DEEPSEEK=sk-" + "3f9a1c7e5b2d4f8a6c0e9b1d7a3f5c2e", "a.py")[0][0] == "chave OpenAI/Anthropic")
confere("OpenRouter sk-or-v1-", R.procura_segredos("OR=sk-or-v1-" + "3f9a1c7e5b2d4f8a6c0e9b1d7a3f5c2e" * 2, "a.py")[0][0] == "chave OpenAI/Anthropic")
confere("wp-config mostra o nome da constante", R.procura_segredos("define( 'DB_PASSWORD', 'Qz8vK2mR7t' );", "wp-config.php")[0][2] == "DB_PASSWORD")
confere("lista longa avisa o resto", "e mais 5" in R.lista([str(i) for i in range(35)]))
confere("em tests/ = cara de exemplo", R.procura_segredos(f'"{AWS}"', "tests/test_x.py")[0][3] is True)
confere("em app.py = de verdade", R.procura_segredos(f'"{AWS}"', "src/app.py")[0][3] is False)
confere("sk-Ab1Ab1… = exemplo (baixa variedade)", R.procura_segredos('k="sk-' + 'Ab1' * 14 + '"', "src/a.js")[0][3] is True)
confere("AIza…abcdefgh = exemplo (sequência)", R.procura_segredos('k="AIzaSyDxabcdefghijklmnopqrstuvwxyz12345"', "src/a.js")[0][3] is True)
confere("classe CSS sk-spinner não é chave", R.procura_segredos('<div class="sk-spinner-wave-container-rect-item">', "a.html") == [])
confere("'latest' não vira exemplo", R.procura_segredos(f'const latestKey = "sk-proj-Zq8vN2kR7tB4mW9xL3pC6yH1dF5gJ0s"', "src/a.js")[0][3] is False)
confere("chave Stripe achada", R.procura_segredos('STRIPE="sk_live_' + '51Hq8ZkR2vB7nM4xL9pC3tY6"', "pay.py")[0][0] == "chave Stripe")
confere("chave em docs/ continua AGORA", R.procura_segredos(f'"{AWS}"', "docs/deploy.md")[0][3] is False)
confere("texto comum não acusa", R.procura_segredos("skill-de-teste e AKIA curto", "x.md") == [])
confere(".env versionado", R.env_versionados([".env", "api/.env.local", ".env.example", "a/b.env.sample", "x.txt"]) == [".env", "api/.env.local"])

# ── repositório de verdade (temporário) ──
with tempfile.TemporaryDirectory() as d:
    g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, check=True)
    g("init", "-q")
    g("config", "user.email", "t@t")
    g("config", "user.name", "t")
    open(os.path.join(d, ".env"), "w").write("SENHA=123\n")
    open(os.path.join(d, "app.py"), "w").write(f'TOKEN = "{GH}"\n')
    open(os.path.join(d, ".gitignore"), "w").write("node_modules\n")
    g("add", "-A")
    g("commit", "-qm", "x")
    res = {a["item"].split(": ", 1)[-1]: a["nivel"] for a in R.checa_repo(d)}
    confere("repo: .env no git = AGORA", res.get(".env dentro do git") == "AGORA")
    confere("repo: token no código = AGORA", res.get("segredo escrito no código") == "AGORA")
    confere("repo: .gitignore sem .env = SEMANA", res.get(".gitignore sem .env") == "SEMANA")
    for regra, protege in (("**/.env\n", True), (".env*\n", True), (".env.*\n", False), (".env\n!.env\n", False)):
        open(os.path.join(d, ".gitignore"), "w").write(regra)
        alarme = any(".gitignore sem .env" in a["item"] for a in R.checa_repo(d))
        confere(f"gitignore {regra.strip()!r}: {'protege' if protege else 'NÃO protege'}", alarme != protege)
    # versão limpa
    g("rm", "-q", "--cached", ".env")
    os.remove(os.path.join(d, ".env"))
    open(os.path.join(d, "app.py"), "w").write('TOKEN = os.environ["TOKEN"]\n')
    open(os.path.join(d, ".gitignore"), "w").write("node_modules\n.env\n")
    g("add", "-A")
    g("commit", "-qm", "limpo")
    niveis = [a["nivel"] for a in R.checa_repo(d)]
    confere("repo limpo: nada AGORA", "AGORA" not in niveis)
    for i in range(35):
        open(os.path.join(d, f"k{i}.py"), "w").write(f'T = "{GH[:-2]}{i:02d}"\n')
    g("add", "-A")
    g("commit", "-qm", "muitas")
    seg = [a for a in R.checa_repo(d) if "segredo escrito" in a["item"]][0]
    confere("35 segredos: lista inteira no campo itens", len(seg["itens"]) == 35 and "e mais 5" in seg["detalhe"])

with tempfile.TemporaryDirectory() as d:
    confere("pasta sem git = SEM TESTE", R.checa_repo(d)[0]["nivel"] == "SEM TESTE")

# ── máscara e saída ──
m = R.mascarar_texto("escutando em 192.168.0.7 e 127.0.0.1", False)
confere("máscara de IP", "192.168" not in m and "127.0.0.1" in m)
confere("--mostrar-ips mantém", R.mascarar_texto("192.168.0.7", True) == "192.168.0.7")
md = R.para_markdown([R.achado("vigie", "Porta 6379", "AGORA", "Redis | aberto", "prender")], "01/01/2026")
confere("markdown escapa |", "Redis \\| aberto" in md and "1 para AGORA" in md)
import contextlib, io
with contextlib.redirect_stderr(io.StringIO()):
    confere("--blocos inválido = 2", R.main(["--blocos", "tudo"]) == 2)

# ── só leitura: o script não chama nada que muda o sistema ──
fonte = open(os.path.join(os.path.dirname(AQUI), "relogio.py"), encoding="utf-8").read()
proibidos = ['"upgrade"]', '"install"', '"refresh"]', '"pull"', '"enable"', "sudo", "urlopen", "requests"]
cmds = [l for l in fonte.splitlines() if "rodar([" in l]
confere("nenhum comando que altera", not any(p in l for l in cmds for p in proibidos))

print(f"\n{len(falhas)} falha(s)" if falhas else "\ntodos os testes passaram")
sys.exit(1 if falhas else 0)
