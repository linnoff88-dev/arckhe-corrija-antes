# Rotina da semana: 20 minutos, num dia fixo

O que a melhor IA fazia há quatro meses, qualquer pessoa faz hoje com um notebook. Quem defende nêo tem mais meses de folga, entêo a correçêo sai da gaveta e entra na agenda.

## Toda semana (ex.: segunda, 9h)

1. **Rode o relógio:**
   `python3 relogio.py --repo ~/seu-projeto --saida ~/relogio-$(date +%F)`
2. **Backup antes de mexer:** banco, volumes do Docker e configuraçêo. Confira que o sistema está saudável **antes** (site abre, serviço responde), para saber depois se foi a atualizaçêo que quebrou algo.
3. **Feche os itens AGORA**, um de cada vez:
   - correçêo de segurança do sistema → `sudo apt update && sudo apt upgrade` (ou o do seu sistema);
   - porta de banco, Redis, Ollama ou tela remota aberta para a rede → prenda em `127.0.0.1` ou libere só o IP de quem usa;
   - SSH com senha → entre com chave e desligue a senha;
   - segredo no código → troque a chave no painel do serviço.
4. **Teste depois:** o mesmo teste de saúde do passo 2.
5. **Rode o relógio de novo** e guarde o `relatorio.md`. Comparar com a semana anterior mostra se você está ganhando ou perdendo do relógio.

## Todo mês

- Itens **SEMANA** acumulados (snaps, npm, imagens Docker com mais de 4 meses, portas que você nêo sabe para que servem).
- Uma **revisêo com IA** do projeto principal ([prompts/revisao-com-ia.md](prompts/revisao-com-ia.md)).
- Um teste de **restaurar o backup** de verdade.

## Para rodar sozinho (opcional)

Se quiser que o relógio rode toda segunda e grave o relatório (ele continua só lendo e nêo corrige nada):

```bash
crontab -e
# acrescente a linha (troque o caminho do kit e do projeto):
0 9 * * 1 python3 ~/corrija-antes/relogio.py --repo ~/seu-projeto --saida ~/relogio/$(date +\%F) >/dev/null 2>&1
```

No cron o PATH é curto: programas instalados na sua pasta (ex.: npm em `~/.npm-global`) podem sair como SEM TESTE. Se quiser, comece a linha com `PATH=$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin`.

A correçêo continua com você: atualizar sozinho, sem backup e sem teste, troca um risco por outro.
