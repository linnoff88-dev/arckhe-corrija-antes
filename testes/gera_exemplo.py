#!/usr/bin/env python3
"""Gera exemplos/relatorio-exemplo.md passando DADOS INVENTADOS pelo código de verdade do relogio.py.
Nada da máquina onde roda entra no exemplo. Uso: python3 testes/gera_exemplo.py"""
import os
import subprocess
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)
import relogio as R  # noqa: E402

AGORA = time.mktime((2026, 11, 12, 9, 0, 0, 0, 0, -1))
FALSO = {
    "apt": "Listing...\nopenssl/noble-security 3.0.13-0ubuntu3.6 amd64 [upgradable from: 3.0.13-0ubuntu3.4]\n"
           "openssh-server/noble-security 1:9.6p1-3ubuntu13.9 amd64 [upgradable from: 1:9.6p1-3ubuntu13.5]\n"
           "nginx/noble-updates 1.24.0-2ubuntu7.4 amd64 [upgradable from: 1.24.0-2ubuntu7.1]\n",
    "snap": "Name Version Rev Size Publisher Notes\nfirefox 145.0 7000 280MB mozilla -\n",
    "npm": '{"@openai/codex":{},"pm2":{}}',
    "ss": "LISTEN 0 511 0.0.0.0:80 0.0.0.0:* users:((\"nginx\",pid=1,fd=6))\n"
          "LISTEN 0 128 0.0.0.0:22 0.0.0.0:*\n"
          "LISTEN 0 511 0.0.0.0:6379 0.0.0.0:* users:((\"redis-server\",pid=2,fd=6))\n"
          "LISTEN 0 4096 127.0.0.1:5432 0.0.0.0:*\n"
          "LISTEN 0 4096 0.0.0.0:11434 0.0.0.0:* users:((\"ollama\",pid=3,fd=3))\n"
          "LISTEN 0 50 0.0.0.0:3000 0.0.0.0:* users:((\"node\",pid=4,fd=3))\n",
    "docker ps names": "loja-db|0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp\nloja-web|127.0.0.1:8080->80/tcp\n",
    "docker ps imgs": "loja-db|postgres:14\nloja-web|nginx:1.25\n",
}
ARQ = {"/var/log/apt/history.log": "Start-Date: 2026-09-20  10:00:00\n",
       "/etc/ufw/ufw.conf": "ENABLED=no\n",
       "/etc/ssh/sshd_config": "PasswordAuthentication yes\nPermitRootLogin prohibit-password\n"}


def rodar(cmd, timeout=90):
    c = " ".join(cmd)
    if c.startswith("apt list"):
        return 0, FALSO["apt"]
    if c.startswith("snap refresh"):
        return 0, FALSO["snap"]
    if c.startswith("npm -g outdated"):
        return 1, FALSO["npm"]
    if c.startswith("ss "):
        return 0, FALSO["ss"]
    if c == "docker ps --format {{.Names}}|{{.Ports}}":
        return 0, FALSO["docker ps names"]
    if c == "docker ps --format {{.Names}}|{{.Image}}":
        return 0, FALSO["docker ps imgs"]
    if c.startswith("docker image inspect"):
        return 0, "2025-05-02T10:00:00.000Z" if "postgres" in c else "2026-10-20T10:00:00.000Z"
    if cmd[0] == "git":
        return subprocess.run(cmd, capture_output=True, text=True).returncode, \
            subprocess.run(cmd, capture_output=True, text=True).stdout
    return None


R.rodar = rodar
R.ler = lambda p: ARQ.get(p) if p in ARQ else (open(p).read() if p.startswith(tempfile.gettempdir()) else None)
R.glob.glob = lambda padrao: []
_existe = os.path.exists
R.os.path.exists = lambda p: p in ARQ or (p.startswith(tempfile.gettempdir()) and _existe(p))
R.shutil.which = lambda n: "/usr/bin/" + n if n in ("apt", "snap", "npm", "ss", "docker", "git") else None

achados = R.checa_apt(AGORA) + R.checa_snap() + R.checa_npm() + R.checa_docker_imagens(AGORA)
ps, vistas = R.checa_portas()
achados += ps + R.checa_firewall() + R.checa_ssh(vistas) + R.checa_docker_portas()

with tempfile.TemporaryDirectory() as d:
    loja = os.path.join(d, "minha-loja")
    os.makedirs(loja)
    g = lambda *a: subprocess.run(["git", "-C", loja, *a], capture_output=True, check=True)
    g("init", "-q"), g("config", "user.email", "x@x"), g("config", "user.name", "x")
    open(os.path.join(loja, ".env"), "w").write("DB_SENHA=inventada\n")
    open(os.path.join(loja, ".gitignore"), "w").write("node_modules\n")
    open(os.path.join(loja, "pagamento.js"), "w").write('const chave = "sk-' + "proj-Zq8vN2kR7tB4mW9xL3pC6yH1dF5gJ0s" + '";\n')
    g("add", "-A"), g("commit", "-qm", "inicio")
    achados += R.checa_repo(loja, AGORA)

os.makedirs(os.path.join(RAIZ, "exemplos"), exist_ok=True)
md = R.para_markdown(achados, "12/11/2026 09:00")
md = md.replace("IPs e nome da máquina mascarados.", "**Exemplo com dados inventados** (servidor fictício de uma loja).")
open(os.path.join(RAIZ, "exemplos", "relatorio-exemplo.md"), "w", encoding="utf-8").write(md)
print(md.splitlines()[2])
