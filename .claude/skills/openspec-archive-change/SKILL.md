---
name: openspec-archive-change
description: Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.12.0"
---

# Arquivar uma mudanca concluida (OpenSpec)

## Passos

1. Escolha a mudanca.
2. Confira se todos os artefatos estao completos (`openspec status --change ... --json`).
3. Confira se todas as tarefas estao marcadas como feitas.
4. Veja se os deltas ja foram para as specs principais. Se nao foram, rode
   a sincronizacao antes (`/opsx:sync`).
5. Arquive: `openspec archive "<nome>"`.
6. Mostre o resumo do que foi arquivado.

Se algo estiver incompleto, diga o que falta e pare. Nao arquive pela metade.
