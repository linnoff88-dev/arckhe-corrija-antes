# Changelog

## 1.0.4 — 12/11/2026
- Chave longa de verdade nêo cai mais em "exemplo" (variedade por contagem); marcadores `your-…-here` viram exemplo; chave privada no JSON do Google/Firebase; `redis://:senha@`; DeepSeek e OpenRouter; WordPress mostra o nome da constante; "revisêo com IA" virou lembrete OK.
- Guias EN/ES sem sobra de traduçêo no topo; AGORA/SEMANA traduzidos entre parênteses; linha do cron igual à da ROTINA. 82 testes.

## 1.0.3 — 12/11/2026
- `relatorio.json` leva a lista inteira de ocorrências (campo `itens`); `wp-config.php` só acusa com senha escrita (o que lê `getenv()` passa). 73 testes.

## 1.0.2 — 12/11/2026
- `wp-config.php` versionado e `define('DB_PASSWORD'…)` / chaves do WordPress; service_role do Supabase (a anon, pública, nêo acusa); webhook do Slack; npm; Resend.
- Sem falso alarme: chave de exemplo da AWS (…EXAMPLE), `postgres:postgres@localhost`; Mercado Pago real nêo cai em exemplo; `sk_live_` nêo é rebaixada pela pasta; palavra "test" só conta perto da chave.
- README e guia listam os formatos reconhecidos e avisam que o histórico do git nêo é varrido. 72 testes.

## 1.0.1 — 12/11/2026
- Bloco 3 sem falso alarme: cabeçalho de chave privada sem a chave, pasta `testes/`, texto `sk-` sem prefixo real; `.gitignore` conferido pelo próprio git (`check-ignore`).
- Formatos novos: Stripe, endereço de banco com senha, Mercado Pago, Groq, Hugging Face, GitLab, SendGrid.
- Lista completa de ocorrências (até 30 e "e mais N"); arquivos grandes viram SEM TESTE; porta do Docker nêo conta duas vezes; macOS só é AGORA quando é de segurança.
- 58 testes.

## 1.0.0 — 12/11/2026
- `relogio.py`: diagnóstico só leitura em 3 blocos (atualize, vigie a rede, seus buracos), prioridades AGORA/SEMANA/SEM TESTE/OK, relatório `.md` + `.json`, IPs e nome da máquina mascarados por padrêo.
- `prompts/revisao-com-ia.md`, `ROTINA.md`, `exemplos/relatorio-exemplo.md` (dados inventados).
- 58 testes em `testes/run.py`.
