---
name: openspec-update-change
description: Update an OpenSpec change by revising its existing planning artifacts and keeping them coherent with one another. Use when the user wants to revise a change's plan, fold new decisions into it, or reconcile its artifacts after an edit. Never edits code.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.12.0"
---

# Revisar o plano de uma mudanca (OpenSpec)

Ajusta artefatos de planejamento que ja existem, mantendo os coerentes entre si.
Nunca mexe em codigo.

## Passos

1. Escolha a mudanca (`openspec status --json` se nao foi dita).
2. `openspec status --change "<nome>" --json` para listar os artefatos.
3. Entenda o que o usuario quer mudar.
4. Leia os artefatos afetados e veja o que mais precisa mudar junto:
   mexer na spec normalmente mexe nas tarefas.
5. Aplique um artefato por vez, confirmando com o usuario.
6. Valide (`openspec validate "<nome>" --strict`) e diga qual seria o proximo
   passo, sem executa-lo.
