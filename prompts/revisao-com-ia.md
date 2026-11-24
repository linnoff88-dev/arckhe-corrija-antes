# RevisÃ£o com IA: ache os seus buracos antes dos outros

A mesma IA que ataca tambÃ©m acha o buraco antes do invasor. Este prompt pede para ela revisar **o seu prÃ³prio cÃ³digo**, sÃ³ lendo, e devolver uma lista do que corrigir primeiro.

**Use sÃ³ em cÃ³digo que Ã© seu** (ou que vocÃª tem permissÃ£o escrita para revisar). Rode numa cÃ³pia ou num branch, nunca direto em produÃ§Ã£o.

## Onde rodar

- **Claude Code** ou **Codex**, abertos na pasta do projeto, pela sua assinatura.
- **Modelo local** (Ollama, LM Studio) para cÃ³digo que nÃ£o pode sair da mÃ¡quina. Ã‰ mais lento e acha menos, mas nada vai para fora.

Se o `relogio.py` jÃ¡ gerou um `relatorio.md`, cole os achados do bloco "Seus buracos" no fim do pedido.

## O prompt (copie tudo daqui para baixo)

```text
VocÃª Ã© um revisor de seguranÃ§a defensiva. Este projeto Ã© MEU e eu quero corrigir os buracos antes que alguÃ©m os ache.

Regras:
- SÃ³ LEIA. NÃ£o rode nada que mude arquivos, banco, rede ou contas. NÃ£o instale nada.
- NÃ£o escreva exploraÃ§Ã£o, nÃ£o teste contra servidor nenhum. Aponte o defeito e a correÃ§Ã£o.
- Se nÃ£o tiver certeza, diga "suspeita" e o que eu preciso conferir.
- Nunca copie o valor de uma senha ou chave na resposta: diga sÃ³ arquivo e linha.

Procure, nesta ordem:
1. Segredos: chaves, tokens e senhas no cÃ³digo, no histÃ³rico do git ou em arquivos de exemplo.
2. Login e permissÃ£o: rota que nÃ£o confere quem estÃ¡ logado; usuÃ¡rio que consegue ver ou mudar dado de outro trocando um id; painel de admin sem trava.
3. Dados que vÃªm de fora: formulÃ¡rio, URL, upload, webhook ou mensagem que chega no banco, no terminal ou na pÃ¡gina sem validaÃ§Ã£o (SQL, comando, HTML/JS).
4. Dinheiro e limites: preÃ§o, desconto, quantidade ou plano que o navegador manda e o servidor aceita; rota cara sem limite de uso.
5. Agente de IA: e-mail, pÃ¡gina ou documento lido pelo agente que pode virar ordem; ferramenta perigosa sem confirmaÃ§Ã£o humana.
6. DependÃªncias e configuraÃ§Ã£o: pacote muito velho, modo debug ligado, CORS aberto para todos, cookie sem Secure/HttpOnly, serviÃ§o escutando em 0.0.0.0 sem precisar.

Responda com uma tabela, do mais grave para o menos grave:
| Prioridade (AGORA/SEMANA/DEPOIS) | Arquivo:linha | O que estÃ¡ errado, em uma frase simples | Como corrigir | Como eu confiro que ficou certo |

Depois da tabela, no mÃ¡ximo 5 linhas: o que vocÃª NÃƒO conseguiu revisar e por quÃª.
```

## Depois da resposta

1. Comece pelos itens **AGORA**. Corrija um de cada vez e rode os testes do projeto.
2. PeÃ§a Ã  IA para **conferir a correÃ§Ã£o** ("revise sÃ³ o arquivo X de novo, o item 1 ficou fechado?").
3. Rode de novo `python3 relogio.py --blocos codigo --repo <pasta>`.
4. Se aparecer segredo, **troque a chave no painel do serviÃ§o**. Apagar do arquivo nÃ£o basta, porque ela continua no histÃ³rico do git.

Kits ARCKHÉ para ir mais fundo: [invada-seu-proprio-app](https://linnoff88-dev.github.io/ (as 5 brechas de app feito com IA) e [agente-blindado](https://linnoff88-dev.github.io/ (injeÃ§Ã£o de prompt em agentes).
