# CLAUDE.md — corrija-antes

Kit público (inematds/corrija-antes, autor dos commits `inematds <inematds@gmail.com>`).

- `relogio.py` — SÓ LÊ. Nunca acrescentar comando que instala, atualiza, liga/desliga serviço ou varre outra máquina; nenhuma chamada de rede/API. O teste "nenhum comando que altera" em `testes/run.py` vigia isso.
- Antes de commitar: `python3 testes/run.py` → `todos os testes passaram`.
- `exemplos/relatorio-exemplo.md` sai SÓ de `python3 testes/gera_exemplo.py` (dados inventados). Nunca publicar saída real de nenhuma máquina (portas, IPs, hosts, nomes de container).
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`; README em 3 idiomas. Mudou o PT, retraduza os dois. Dentro de `<pre>` só os comentários mudam.
- Origem: vídeo "A China soltou de graça a IA hacker que a OpenAI trancou" (lives11, 11/11/2026). Sem citar o vídeo de referência nem o autor dele.

## Self-learning

Quando eu for corrigido ou perceber um erro: antes de seguir, acrescente a lição como regra de uma linha no TOPO de `## Lessons`.

## Lessons
- Chave em pasta de teste/docs aparecia como segredo AGORA: separar "cara de exemplo" (SEMANA, confira) do segredo real. (12/11/2026)
