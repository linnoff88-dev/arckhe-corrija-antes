> **Uso defensivo:** rode sêÂ³ na SUA mêÂ¡quina e nos SEUS repositêÂ³rios. O kit sêÂ³ lêÂª: nêÂ£o instala, nêÂ£o atualiza, nêÂ£o corrige, nêÂ£o varre outras mêÂ¡quinas e nêÂ£o envia nada: sêÂ³ consulta os servidores de atualizaêÂ§êÂ£o do seu prêÂ³prio sistema.

# corrija-antes ê¢â¬â o relêÂ³gio de quem defende

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![Corrija antes](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## O que êÂ©

Em julho de 2026, as IAs abertas estavam de 4 a 7 meses atrêÂ¡s das fechadas em ataque. Em outubro, num teste de invasêÂ£o de rede de empresa, essa distêÂ¢ncia chegou a zero: quem defende perdeu a folga de tempo. corrija-antes êÂ© um kit grêÂ¡tis que faz, na sua mêÂ¡quina, as trêÂªs coisas que ainda funcionam: **atualizar mais rêÂ¡pido, vigiar a rede e achar os seus buracos antes dos outros**. Um script de diagnêÂ³stico mostra o que corrigir AGORA e o que pode esperar a semana, e um prompt pronto pêÂµe a IA para revisar o seu cêÂ³digo. Serve para quem tem computador, servidor ou app no ar e nêÂ£o trabalha com seguranêÂ§a todo dia. Precisa de Python 3 (Linux ou macOS).

## ê°Å¸ââ Guia de uso

Guia completo, com o vêÂ­deo: **https://linnoff88-dev.github.io/

VêÂ­deo: [A China soltou de graêÂ§a a IA hacker que a OpenAI trancou](https://www.youtube.com/watch?v=1WFT-VgGuPM) êÂ· [versêÂ£o vertical](https://youtube.com/shorts/-R65CemeRvc)

## Teste em 1 minuto

```bash
git clone https://github.com/linnoff88-dev/corrija-antes.git
cd corrija-antes
python3 relogio.py --repo ~/seu-projeto --saida relatorio
```

Sai uma lista na tela e um `relatorio/relatorio.md`. Cada item tem prioridade:

| Prioridade | Quer dizer |
|---|---|
| **AGORA** | correêÂ§êÂ£o de seguranêÂ§a esperando, banco/Redis/Ollama/tela remota aberto para a rede, SSH com senha, segredo no cêÂ³digo |
| **SEMANA** | atualizaêÂ§êÂ£o comum, porta aberta que vocêÂª precisa conferir, firewall desligado, imagem Docker com mais de 4 meses, `.env` fora do `.gitignore`, chave com cara de exemplo, dependêÂªncias paradas |
| **SEM TESTE** | nêÂ£o deu para conferir (falta permissêÂ£o ou ferramenta): nêÂ£o conta como seguro |
| **OK** | conferido e em dia |

Veja um [relatêÂ³rio de exemplo](exemplos/relatorio-exemplo.md) (servidor fictêÂ­cio de uma loja, dados inventados).

## Os 3 blocos

1. **Atualize**: pacotes do sistema com correêÂ§êÂ£o de seguranêÂ§a (apt, dnf, Homebrew, macOS), snaps, pacotes globais do npm, imagens Docker em uso com mais de 4 meses, reinêÂ­cio pendente e **hêÂ¡ quantos dias** foi a êÂºltima atualizaêÂ§êÂ£o.
2. **Vigie a rede**: o que estêÂ¡ escutando sêÂ³ na mêÂ¡quina, sêÂ³ na rede interna/VPN ou aberto para qualquer rede; portas crêÂ­ticas (bancos, Redis, Ollama, VNC/RDP, API do Docker); firewall; SSH com senha ou root; portas que o Docker publica **por cima do ufw**.
3. **Seus buracos** (`--repo`): `.env` dentro do git, `.gitignore` sem `.env`, chaves e tokens escritos no cêÂ³digo (o valor sai mascarado), dependêÂªncias sem mudanêÂ§a hêÂ¡ mais de 4 meses e o lembrete da revisêÂ£o com IA.

   Formatos reconhecidos: AWS, OpenAI/Anthropic, DeepSeek, OpenRouter, Stripe, GitHub, Slack (token e webhook), Google, Telegram, Mercado Pago, Groq, Hugging Face, GitLab, SendGrid, npm, Resend, service_role do Supabase, chave privada, senha em endereêÂ§o de banco e senhas/chaves do `wp-config.php`. Olha sêÂ³ os arquivos atuais, nêÂ£o o histêÂ³rico do git; senha genêÂ©rica (`password=ê¢â¬Â¦`) e chave de outros serviêÂ§os passam sem aviso.

## OpêÂ§êÂµes

```bash
python3 relogio.py                              # sêÂ³ a mêÂ¡quina
python3 relogio.py --repo ~/app --repo ~/api    # mêÂ¡quina + dois repositêÂ³rios
python3 relogio.py --blocos vigie               # sêÂ³ um bloco: atualize, vigie, codigo
python3 relogio.py --saida relatorio            # grava relatorio.md e relatorio.json
python3 relogio.py --json                       # resultado em JSON na tela
python3 relogio.py --mostrar-ips                # nêÂ£o mascara IPs, usuêÂ¡rio e nome da mêÂ¡quina
```

CêÂ³digo de saêÂ­da: `0` = nada para AGORA êÂ· `1` = tem item AGORA êÂ· `2` = erro de uso. Sem `sudo`, alguns itens ficam SEM TESTE (ex.: regras do firewall); o script diz qual comando rodar para conferir.

## O processo, do inêÂ­cio ao fim

1. ê°Å¸Â§Â  **VocêÂª** clona o kit e roda `python3 relogio.py --repo <seu projeto> --saida relatorio`.
2. ê¢Å¡â¢ê¯Â¸Â **Script** lista os itens AGORA / SEMANA / SEM TESTE / OK e grava o relatêÂ³rio (sêÂ³ lendo).
3. ê°Å¸Â§Â  **VocêÂª** faz backup e confere a saêÂºde do sistema antes de mexer.
4. ê°Å¸Â§Â  **VocêÂª** fecha os itens AGORA, um de cada vez ([ROTINA.md](ROTINA.md)).
5. ê°Å¸Â¤â **IA** (Claude Code, Codex ou modelo local) revisa o seu cêÂ³digo com o [prompt de revisêÂ£o](prompts/revisao-com-ia.md).
6. ê¢Å¡â¢ê¯Â¸Â **Script** roda de novo para confirmar; opcional: toda segunda pelo cron.

## Para ir mais fundo (kits ARCKHê de auditoria e diagnêÂ³stico)

| Kit | Para quêÂª |
|---|---|
| [auditoria-seguranca](https://linnoff88-dev.github.io/ | testa se suas ferramentas ainda confiam em certificados vazados e se o PHP tem a falha PHP2Shell |
| [blinda-site](https://linnoff88-dev.github.io/ | diagnêÂ³stico do site por dentro: plano, backup, simulaêÂ§êÂ£o e nêÂ­veis de risco |
| [invada-seu-proprio-app](https://linnoff88-dev.github.io/ | as 5 brechas mais comuns de app feito com IA, testadas na sua cêÂ³pia de teste |
| [agente-blindado](https://linnoff88-dev.github.io/ | 5 travas contra injeêÂ§êÂ£o de prompt e 10 ataques para testar o seu agente |
| [caixa-do-agente](https://linnoff88-dev.github.io/ | nota do seu harness de agente e uma caixa Docker descartêÂ¡vel, sem rede e sem `.env` |
| [ia-sem-censura-defensiva](https://linnoff88-dev.github.io/ | modelo aberto sem trava, usado sêÂ³ para defesa, rodando na sua mêÂ¡quina |
| [protegendo-seus-repos](https://linnoff88-dev.github.io/ | backup em 3 camadas dos seus repositêÂ³rios contra bloqueio ou invasêÂ£o |

## Testes

```bash
python3 testes/run.py        # 82 testes com dados inventados
python3 testes/gera_exemplo.py   # refaz o relatêÂ³rio de exemplo
```

Python 3, sem dependêÂªncias. ConteêÂºdo autoral. LicenêÂ§a [MIT](LICENSE). Mais em [ARCKHê AI](https://ARCKHê AI).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>