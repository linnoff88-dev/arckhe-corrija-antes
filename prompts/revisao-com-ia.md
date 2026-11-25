# Revisêo com IA: ache os seus buracos antes dos outros

A mesma IA que ataca também acha o buraco antes do invasor. Este prompt pede para ela revisar **o seu próprio código**, só lendo, e devolver uma lista do que corrigir primeiro.

**Use só em código que é seu** (ou que você tem permissêo escrita para revisar). Rode numa cópia ou num branch, nunca direto em produçêo.

## Onde rodar

- **Claude Code** ou **Codex**, abertos na pasta do projeto, pela sua assinatura.
- **Modelo local** (Ollama, LM Studio) para código que nêo pode sair da máquina. �? mais lento e acha menos, mas nada vai para fora.

Se o `relogio.py` já gerou um `relatorio.md`, cole os achados do bloco "Seus buracos" no fim do pedido.

## O prompt (copie tudo daqui para baixo)

```text
Você é um revisor de segurança defensiva. Este projeto é MEU e eu quero corrigir os buracos antes que alguém os ache.

Regras:
- Só LEIA. Nêo rode nada que mude arquivos, banco, rede ou contas. Nêo instale nada.
- Nêo escreva exploraçêo, nêo teste contra servidor nenhum. Aponte o defeito e a correçêo.
- Se nêo tiver certeza, diga "suspeita" e o que eu preciso conferir.
- Nunca copie o valor de uma senha ou chave na resposta: diga só arquivo e linha.

Procure, nesta ordem:
1. Segredos: chaves, tokens e senhas no código, no histórico do git ou em arquivos de exemplo.
2. Login e permissêo: rota que nêo confere quem está logado; usuário que consegue ver ou mudar dado de outro trocando um id; painel de admin sem trava.
3. Dados que vêm de fora: formulário, URL, upload, webhook ou mensagem que chega no banco, no terminal ou na página sem validaçêo (SQL, comando, HTML/JS).
4. Dinheiro e limites: preço, desconto, quantidade ou plano que o navegador manda e o servidor aceita; rota cara sem limite de uso.
5. Agente de IA: e-mail, página ou documento lido pelo agente que pode virar ordem; ferramenta perigosa sem confirmaçêo humana.
6. Dependências e configuraçêo: pacote muito velho, modo debug ligado, CORS aberto para todos, cookie sem Secure/HttpOnly, serviço escutando em 0.0.0.0 sem precisar.

Responda com uma tabela, do mais grave para o menos grave:
| Prioridade (AGORA/SEMANA/DEPOIS) | Arquivo:linha | O que está errado, em uma frase simples | Como corrigir | Como eu confiro que ficou certo |

Depois da tabela, no máximo 5 linhas: o que você N�fO conseguiu revisar e por quê.
```

## Depois da resposta

1. Comece pelos itens **AGORA**. Corrija um de cada vez e rode os testes do projeto.
2. Peça à IA para **conferir a correçêo** ("revise só o arquivo X de novo, o item 1 ficou fechado?").
3. Rode de novo `python3 relogio.py --blocos codigo --repo <pasta>`.
4. Se aparecer segredo, **troque a chave no painel do serviço**. Apagar do arquivo nêo basta, porque ela continua no histórico do git.

Kits ARCKH� para ir mais fundo: [invada-seu-proprio-app](https://linnoff88-dev.github.io/ (as 5 brechas de app feito com IA) e [agente-blindado](https://linnoff88-dev.github.io/ (injeçêo de prompt em agentes).
