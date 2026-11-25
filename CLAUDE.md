ï»¿# CLAUDE.md ê¢â¬â corrija-antes

Kit pêÂºblico (linnoff88-dev/corrija-antes, autor dos commits `linnoff88-dev <linnoff88-dev@gmail.com>`).

- `relogio.py` ê¢â¬â Sêâ LêÅ . Nunca acrescentar comando que instala, atualiza, liga/desliga serviêÂ§o ou varre outra mêÂ¡quina; nenhuma chamada de rede/API. O teste "nenhum comando que altera" em `testes/run.py` vigia isso.
- Antes de commitar: `python3 testes/run.py` ê¢â â `todos os testes passaram`.
- `exemplos/relatorio-exemplo.md` sai Sêâ de `python3 testes/gera_exemplo.py` (dados inventados). Nunca publicar saêÂ­da real de nenhuma mêÂ¡quina (portas, IPs, hosts, nomes de container).
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`; README em 3 idiomas. Mudou o PT, retraduza os dois. Dentro de `<pre>` sêÂ³ os comentêÂ¡rios mudam.
- Origem: vêÂ­deo "A China soltou de graêÂ§a a IA hacker que a OpenAI trancou" (lives11, 11/11/2026). Sem citar o vêÂ­deo de referêÂªncia nem o autor dele.

## Self-learning

Quando eu for corrigido ou perceber um erro: antes de seguir, acrescente a liêÂ§êÂ£o como regra de uma linha no TOPO de `## Lessons`.

## Lessons
- Chave em pasta de teste/docs aparecia como segredo AGORA: separar "cara de exemplo" (SEMANA, confira) do segredo real. (12/11/2026)
