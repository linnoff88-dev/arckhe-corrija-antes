# CLAUDE.md â€” corrija-antes

Kit pÃºblico (linnoff88-dev/corrija-antes, autor dos commits `linnoff88-dev <linnoff88-dev@gmail.com>`).

- `relogio.py` â€” SÃ“ LÃŠ. Nunca acrescentar comando que instala, atualiza, liga/desliga serviÃ§o ou varre outra mÃ¡quina; nenhuma chamada de rede/API. O teste "nenhum comando que altera" em `testes/run.py` vigia isso.
- Antes de commitar: `python3 testes/run.py` â†’ `todos os testes passaram`.
- `exemplos/relatorio-exemplo.md` sai SÃ“ de `python3 testes/gera_exemplo.py` (dados inventados). Nunca publicar saÃ­da real de nenhuma mÃ¡quina (portas, IPs, hosts, nomes de container).
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`; README em 3 idiomas. Mudou o PT, retraduza os dois. Dentro de `<pre>` sÃ³ os comentÃ¡rios mudam.
- Origem: vÃ­deo "A China soltou de graÃ§a a IA hacker que a OpenAI trancou" (lives11, 11/11/2026). Sem citar o vÃ­deo de referÃªncia nem o autor dele.

## Self-learning

Quando eu for corrigido ou perceber um erro: antes de seguir, acrescente a liÃ§Ã£o como regra de uma linha no TOPO de `## Lessons`.

## Lessons
- Chave em pasta de teste/docs aparecia como segredo AGORA: separar "cara de exemplo" (SEMANA, confira) do segredo real. (12/11/2026)
