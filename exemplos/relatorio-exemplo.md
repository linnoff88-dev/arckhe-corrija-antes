# Relógio de quem defende — 12/11/2026 09:00

**8 para AGORA · 6 para esta SEMANA · 0 sem teste · 2 ok**

Gerado por `relogio.py` (corrija-antes), só leitura. **Exemplo com dados inventados** (servidor fictício de uma loja).

## 1. Atualize

| Prioridade | Item | O que vi | O que fazer |
|---|---|---|---|
| AGORA | Correções de segurança do sistema (apt) | 2 pacote(s) com correção de segurança esperando, de 3 no total. Ex.: openssl, openssh-server | Backup e saúde antes; depois `sudo apt update && sudo apt upgrade` e reinicie o que pedir. |
| AGORA | Última atualização instalada | há 52 dia(s). Em julho de 2026 quem defendia tinha de 4 a 7 meses de folga; em outubro, num teste de invasão, essa folga foi a zero. | Atualizar toda semana, num dia fixo. |
| SEMANA | Snaps | 1 snap(s) com versão nova: firefox | `sudo snap refresh` (o snap também atualiza sozinho, mas pode estar adiado). |
| SEMANA | Pacotes globais do npm | 2 desatualizado(s): @openai/codex, pm2 | `npm -g update` (ou `npm -g install <pacote>@latest`), um de cada vez. |
| SEMANA | Imagens Docker em uso | 1 de 2 container(s) com imagem de mais de 4 meses: loja-db (postgres:14, 559 dias) | Backup dos volumes, `docker pull` da imagem nova, recriar o container e conferir. |

## 2. Vigie a rede

| Prioridade | Item | O que vi | O que fazer |
|---|---|---|---|
| AGORA | Porta 6379 aberta para a rede | Redis escutando em todos os endereços (processo redis-server). Se o roteador ou a nuvem deixar passar, qualquer um na internet tenta entrar. | Se só você usa: prender em 127.0.0.1 na configuração do serviço. Se outra máquina usa: liberar só o IP dela no firewall, e pôr senha. |
| AGORA | Porta 11434 aberta para a rede | Ollama (IA local sem senha) escutando em todos os endereços (processo ollama). Se o roteador ou a nuvem deixar passar, qualquer um na internet tenta entrar. | Se só você usa: prender em 127.0.0.1 na configuração do serviço. Se outra máquina usa: liberar só o IP dela no firewall, e pôr senha. |
| AGORA | SSH aceita senha | o SSH aceita login por senha: é a porta que robôs testam com milhares de senhas por dia | Entre com chave, confirme que funciona, e então `PasswordAuthentication no` + reiniciar o ssh. |
| AGORA | Portas publicadas pelo Docker | 1 porta(s) de container abertas para qualquer rede (loja-db:5433). O Docker abre essas portas POR CIMA do ufw. | No compose, troque `"5432:5432"` por `"127.0.0.1:5432:5432"` quando só a máquina usa. |
| SEMANA | Outras portas abertas para a rede | 2 porta(s) escutando em todos os endereços: 80/nginx, 3000/node | Para cada uma: precisa estar aberta? Se não, prender em 127.0.0.1 ou desligar o serviço. |
| SEMANA | Firewall (ufw) | ufw instalado mas DESLIGADO | Libere antes o que você usa (ex.: `sudo ufw allow OpenSSH`) e depois `sudo ufw enable`. Atenção: portas publicadas pelo Docker passam por cima do ufw. |
| OK | Resumo das portas | 1 só nesta máquina, 0 só na rede interna/VPN, 5 abertas para qualquer rede | — |

## 3. Seus buracos (código)

| Prioridade | Item | O que vi | O que fazer |
|---|---|---|---|
| AGORA | minha-loja: .env dentro do git | 1 arquivo(s) de senhas versionado(s): .env | Troque TODAS as chaves que estão nele (já estão no histórico), depois `git rm --cached <arquivo>` e ponha `.env` e `.env.*` (ou `wp-config.php`) no .gitignore. |
| AGORA | minha-loja: segredo escrito no código | 1 ocorrência(s): pagamento.js:1 chave OpenAI/Anthropic sk-p…(39 caracteres) | Troque a chave no painel do serviço (apagar do arquivo não basta: ela fica no histórico) e leia de variável de ambiente. |
| SEMANA | minha-loja: .gitignore sem .env | o git não ignora o .env: um `git add .` distraído sobe as suas chaves | Acrescente uma linha `.env` (e `.env.*`) no .gitignore e confira com `git check-ignore -v .env`. |
| OK | minha-loja: lembrete — revisão com IA | o script só acha o óbvio; a revisão que pega lógica errada (login, permissão, preço) é com IA | Use o prompt de `prompts/revisao-com-ia.md` no Claude Code, no Codex ou num modelo local. |

## Antes de corrigir

1. Backup do que importa (banco, volumes, configuração).
2. Confira que o sistema está saudável ANTES (assim você sabe se a atualização quebrou algo).
3. Corrija um item por vez e teste.
