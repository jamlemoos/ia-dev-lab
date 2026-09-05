---
name: "speckit-implement"
description: "Execute the implementation plan by processing and executing all tasks defined in tasks.md"
argument-hint: "Optional implementation guidance or task filter"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/implement.md"
user-invocable: true
disable-model-invocation: false
---

# Implementar (SpecKit)

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json` para achar a pasta.
2. Leia `tasks.md`, `plan.md` e `spec.md`.
3. Execute as tarefas na ordem das fases, respeitando as dependencias.
   Tarefas com `[P]` podem sair juntas.
4. Marque `[x]` em cada tarefa assim que ela estiver pronta e testada.
5. Rode a suite de testes ao fim de cada fase.
6. No fim, relate o que foi feito, o que falhou e o que ficou de fora.

Se uma tarefa nao bater com a spec, pare e diga qual das duas esta errada.
Nao conserte a spec no meio da implementacao sem avisar.
