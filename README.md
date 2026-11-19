> **Uso defensivo:** rode sÃ³ na SUA mÃ¡quina e nos SEUS repositÃ³rios. O kit sÃ³ lÃª: nÃ£o instala, nÃ£o atualiza, nÃ£o corrige, nÃ£o varre outras mÃ¡quinas e nÃ£o envia nada: sÃ³ consulta os servidores de atualizaÃ§Ã£o do seu prÃ³prio sistema.

# corrija-antes â€” o relÃ³gio de quem defende

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![Corrija antes](guia/assets/banner.jpg)](https://inematds.github.io/corrija-antes/guia/)

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## O que Ã©

Em julho de 2026, as IAs abertas estavam de 4 a 7 meses atrÃ¡s das fechadas em ataque. Em outubro, num teste de invasÃ£o de rede de empresa, essa distÃ¢ncia chegou a zero: quem defende perdeu a folga de tempo. corrija-antes Ã© um kit grÃ¡tis que faz, na sua mÃ¡quina, as trÃªs coisas que ainda funcionam: **atualizar mais rÃ¡pido, vigiar a rede e achar os seus buracos antes dos outros**. Um script de diagnÃ³stico mostra o que corrigir AGORA e o que pode esperar a semana, e um prompt pronto pÃµe a IA para revisar o seu cÃ³digo. Serve para quem tem computador, servidor ou app no ar e nÃ£o trabalha com seguranÃ§a todo dia. Precisa de Python 3 (Linux ou macOS).

## ðŸ“– Guia de uso

Guia completo, com o vÃ­deo: **https://inematds.github.io/corrija-antes/guia/**

VÃ­deo: [A China soltou de graÃ§a a IA hacker que a OpenAI trancou](https://www.youtube.com/watch?v=1WFT-VgGuPM) Â· [versÃ£o vertical](https://youtube.com/shorts/-R65CemeRvc)

## Teste em 1 minuto

```bash
git clone https://github.com/inematds/corrija-antes.git
cd corrija-antes
python3 relogio.py --repo ~/seu-projeto --saida relatorio
```

Sai uma lista na tela e um `relatorio/relatorio.md`. Cada item tem prioridade:

| Prioridade | Quer dizer |
|---|---|
| **AGORA** | correÃ§Ã£o de seguranÃ§a esperando, banco/Redis/Ollama/tela remota aberto para a rede, SSH com senha, segredo no cÃ³digo |
| **SEMANA** | atualizaÃ§Ã£o comum, porta aberta que vocÃª precisa conferir, firewall desligado, imagem Docker com mais de 4 meses, `.env` fora do `.gitignore`, chave com cara de exemplo, dependÃªncias paradas |
| **SEM TESTE** | nÃ£o deu para conferir (falta permissÃ£o ou ferramenta): nÃ£o conta como seguro |
| **OK** | conferido e em dia |

Veja um [relatÃ³rio de exemplo](exemplos/relatorio-exemplo.md) (servidor fictÃ­cio de uma loja, dados inventados).

## Os 3 blocos

1. **Atualize**: pacotes do sistema com correÃ§Ã£o de seguranÃ§a (apt, dnf, Homebrew, macOS), snaps, pacotes globais do npm, imagens Docker em uso com mais de 4 meses, reinÃ­cio pendente e **hÃ¡ quantos dias** foi a Ãºltima atualizaÃ§Ã£o.
2. **Vigie a rede**: o que estÃ¡ escutando sÃ³ na mÃ¡quina, sÃ³ na rede interna/VPN ou aberto para qualquer rede; portas crÃ­ticas (bancos, Redis, Ollama, VNC/RDP, API do Docker); firewall; SSH com senha ou root; portas que o Docker publica **por cima do ufw**.
3. **Seus buracos** (`--repo`): `.env` dentro do git, `.gitignore` sem `.env`, chaves e tokens escritos no cÃ³digo (o valor sai mascarado), dependÃªncias sem mudanÃ§a hÃ¡ mais de 4 meses e o lembrete da revisÃ£o com IA.

   Formatos reconhecidos: AWS, OpenAI/Anthropic, DeepSeek, OpenRouter, Stripe, GitHub, Slack (token e webhook), Google, Telegram, Mercado Pago, Groq, Hugging Face, GitLab, SendGrid, npm, Resend, service_role do Supabase, chave privada, senha em endereÃ§o de banco e senhas/chaves do `wp-config.php`. Olha sÃ³ os arquivos atuais, nÃ£o o histÃ³rico do git; senha genÃ©rica (`password=â€¦`) e chave de outros serviÃ§os passam sem aviso.

## OpÃ§Ãµes

```bash
python3 relogio.py                              # sÃ³ a mÃ¡quina
python3 relogio.py --repo ~/app --repo ~/api    # mÃ¡quina + dois repositÃ³rios
python3 relogio.py --blocos vigie               # sÃ³ um bloco: atualize, vigie, codigo
python3 relogio.py --saida relatorio            # grava relatorio.md e relatorio.json
python3 relogio.py --json                       # resultado em JSON na tela
python3 relogio.py --mostrar-ips                # nÃ£o mascara IPs, usuÃ¡rio e nome da mÃ¡quina
```

CÃ³digo de saÃ­da: `0` = nada para AGORA Â· `1` = tem item AGORA Â· `2` = erro de uso. Sem `sudo`, alguns itens ficam SEM TESTE (ex.: regras do firewall); o script diz qual comando rodar para conferir.

## O processo, do inÃ­cio ao fim

1. ðŸ§  **VocÃª** clona o kit e roda `python3 relogio.py --repo <seu projeto> --saida relatorio`.
2. âš™ï¸ **Script** lista os itens AGORA / SEMANA / SEM TESTE / OK e grava o relatÃ³rio (sÃ³ lendo).
3. ðŸ§  **VocÃª** faz backup e confere a saÃºde do sistema antes de mexer.
4. ðŸ§  **VocÃª** fecha os itens AGORA, um de cada vez ([ROTINA.md](ROTINA.md)).
5. ðŸ¤– **IA** (Claude Code, Codex ou modelo local) revisa o seu cÃ³digo com o [prompt de revisÃ£o](prompts/revisao-com-ia.md).
6. âš™ï¸ **Script** roda de novo para confirmar; opcional: toda segunda pelo cron.

## Para ir mais fundo (kits INEMA de auditoria e diagnÃ³stico)

| Kit | Para quÃª |
|---|---|
| [auditoria-seguranca](https://inematds.github.io/auditoria-seguranca/guia/) | testa se suas ferramentas ainda confiam em certificados vazados e se o PHP tem a falha PHP2Shell |
| [blinda-site](https://inematds.github.io/blinda-site/guia/) | diagnÃ³stico do site por dentro: plano, backup, simulaÃ§Ã£o e nÃ­veis de risco |
| [invada-seu-proprio-app](https://inematds.github.io/invada-seu-proprio-app/guia/) | as 5 brechas mais comuns de app feito com IA, testadas na sua cÃ³pia de teste |
| [agente-blindado](https://inematds.github.io/agente-blindado/guia/) | 5 travas contra injeÃ§Ã£o de prompt e 10 ataques para testar o seu agente |
| [caixa-do-agente](https://inematds.github.io/caixa-do-agente/guia/) | nota do seu harness de agente e uma caixa Docker descartÃ¡vel, sem rede e sem `.env` |
| [ia-sem-censura-defensiva](https://inematds.github.io/ia-sem-censura-defensiva/guia/) | modelo aberto sem trava, usado sÃ³ para defesa, rodando na sua mÃ¡quina |
| [protegendo-seus-repos](https://inematds.github.io/protegendo-seus-repos/guia/) | backup em 3 camadas dos seus repositÃ³rios contra bloqueio ou invasÃ£o |

## Testes

```bash
python3 testes/run.py        # 82 testes com dados inventados
python3 testes/gera_exemplo.py   # refaz o relatÃ³rio de exemplo
```

Python 3, sem dependÃªncias. ConteÃºdo autoral. LicenÃ§a [MIT](LICENSE). Mais em [INEMA.CLUB](https://inema.club).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>