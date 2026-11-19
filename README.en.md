> **Defensive use:** run only on YOUR machine and in YOUR repositories. The kit only reads: it does not install, update, fix, scan other machines, or send anything out: it only queries your own system's update servers.

# corrija-antes — the defender’s clock

[![Corrija antes](guia/assets/banner-en.jpg)](https://inematds.github.io/corrija-antes/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

In July 2026, open AI models were 4 to 7 months behind closed models in offensive capabilities. By October, that gap had reached zero in a company network penetration test: defenders had lost their time advantage. corrija-antes is a free kit that does the three things that still work, on your machine: **update faster, watch your network, and find your gaps before others do**. A diagnostic script shows what to fix NOW (AGORA) and what can wait until next week (SEMANA), and a ready-to-use prompt asks AI to review your code. It is for anyone with a computer, server, or app online who does not work in security every day. Requires Python 3 (Linux or macOS).

## 📖 User guide

Full guide, with video: **https://inematds.github.io/corrija-antes/guia/en/**

Video: [China released the hacker AI that OpenAI locked away for free](https://www.youtube.com/watch?v=1WFT-VgGuPM) · [vertical version](https://youtube.com/shorts/-R65CemeRvc)

## Try it in 1 minute

```bash
git clone https://github.com/inematds/corrija-antes.git
cd corrija-antes
python3 relogio.py --repo ~/seu-projeto --saida relatorio
```

It prints a list and creates `relatorio/relatorio.md`. Each item has a priority:

| Priority | Meaning |
|---|---|
| **AGORA (NOW)** | a security fix is waiting, a database/Redis/Ollama/remote screen is open to the network, SSH uses a password, or a secret is in the code |
| **SEMANA (WEEK)** | a routine update, an open port you need to check, firewall disabled, Docker image older than 4 months, `.env` not in `.gitignore`, a key that looks like an example, stale dependencies |
| **SEM TESTE (NOT TESTED)** | could not check (missing permission or tool): does not count as safe |
| **OK (OK)** | checked and up to date |

See a [sample report](exemplos/relatorio-exemplo.md) (in Portuguese; fictional store server, invented data).

## The 3 blocks

1. **Update**: system packages with security fixes (apt, dnf, Homebrew, macOS), snaps, global npm packages, Docker images in use older than 4 months, pending restart, and **how many days** since the last update.
2. **Watch the network**: what is listening only on the machine, only on the internal network/VPN, or open to any network; critical ports (databases, Redis, Ollama, VNC/RDP, Docker API); firewall; SSH with password or root; ports Docker publishes **over ufw**.
3. **Your gaps** (`--repo`): `.env` inside git, `.gitignore` without `.env`, keys and tokens written in code (the value is masked), dependencies unchanged for more than 4 months, and a reminder to review with AI.

   Recognized formats: AWS, OpenAI/Anthropic, DeepSeek, OpenRouter, Stripe, GitHub, Slack (token and webhook), Google, Telegram, Mercado Pago, Groq, Hugging Face, GitLab, SendGrid, npm, Resend, Supabase service_role, private key, password in a database URL, and `wp-config.php` passwords/keys. It only reads the current files, not the git history; a generic password (`password=…`) or keys from other services go unnoticed.

## Options

```bash
python3 relogio.py                              # the machine only
python3 relogio.py --repo ~/app --repo ~/api    # machine + two repositories
python3 relogio.py --blocos vigie               # one block only: update, watch, code
python3 relogio.py --saida relatorio            # saves relatorio.md and relatorio.json
python3 relogio.py --json                       # JSON output on screen
python3 relogio.py --mostrar-ips                # does not mask IPs, username, and machine name
```

Exit code: `0` = nothing marked AGORA (NOW) · `1` = an item is marked AGORA (NOW) · `2` = usage error. Without `sudo`, some items are marked SEM TESTE (NOT TESTED) (e.g., firewall rules); the script tells you which command to run to check.

## The process, start to finish

1. 🧠 **You** clone the kit and run `python3 relogio.py --repo <seu projeto> --saida relatorio`.
2. ⚙️ **Script** lists items marked AGORA / SEMANA / SEM TESTE / OK and saves the report (read-only).
3. 🧠 **You** make a backup and check system health before making changes.
4. 🧠 **You** resolve the AGORA items, one at a time ([ROTINA.md](ROTINA.md) (in Portuguese)).
5. 🤖 **AI** (Claude Code, Codex, or a local model) reviews your code with the [review prompt](prompts/revisao-com-ia.md) (in Portuguese).
6. ⚙️ **Script** runs again to confirm; optional: every Monday via cron.

## Go deeper (INEMA audit and diagnostic kits)

| Kit | What it does |
|---|---|
| [auditoria-seguranca](https://inematds.github.io/auditoria-seguranca/guia/) | checks whether your tools still trust leaked certificates and whether PHP has the PHP2Shell flaw |
| [blinda-site](https://inematds.github.io/blinda-site/guia/) | internal website diagnosis: plan, backup, simulation, and risk levels |
| [invada-seu-proprio-app](https://inematds.github.io/invada-seu-proprio-app/guia/) | the 5 most common gaps in AI-built apps, tested on your test copy |
| [agente-blindado](https://inematds.github.io/agente-blindado/guia/) | 5 safeguards against prompt injection and 10 attacks to test your agent |
| [caixa-do-agente](https://inematds.github.io/caixa-do-agente/guia/) | score for your agent harness and a disposable Docker box, with no network and no `.env` |
| [ia-sem-censura-defensiva](https://inematds.github.io/ia-sem-censura-defensiva/guia/) | an unrestricted open model used only for defense, running on your machine |
| [protegendo-seus-repos](https://inematds.github.io/protegendo-seus-repos/guia/) | 3-layer backup for your repositories against lockout or intrusion |

## Tests

```bash
python3 testes/run.py        # 82 tests with invented data
python3 testes/gera_exemplo.py   # regenerates the sample report
```

Python 3, no dependencies. Original content. [MIT License](LICENSE). More at [INEMA.CLUB](https://inema.club).