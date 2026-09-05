---
name: openspec-apply-change
description: Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.12.0"
---

# Implementar uma mudanca (OpenSpec)

Executa as tarefas ja planejadas de uma mudanca.

## Passos

1. Escolha a mudanca. Se o usuario nao disse qual, liste com
   `openspec status --json` e pergunte.
2. `openspec status --change "<nome>" --json` para ver o schema e o progresso.
3. `openspec instructions apply --change "<nome>" --json` para as instrucoes.
4. Leia os artefatos de contexto que as instrucoes apontarem (proposal, design, specs).
5. Mostre o progresso atual antes de comecar.
6. Implemente tarefa por tarefa, na ordem, marcando cada uma como concluida
   no arquivo de tarefas assim que terminar. Pare se travar em alguma.
7. No fim (ou na pausa), mostre o status e o que ficou pendente.

## Cuidados

- Uma tarefa por vez. Nao marque como feita o que nao rodou.
- Se travar, diga onde e por que, em vez de improvisar outra solucao.
