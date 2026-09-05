---
name: "speckit-tasks"
description: "Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts."
argument-hint: "Optional task generation constraints"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/tasks.md"
user-invocable: true
disable-model-invocation: false
---

# Gerar as tarefas (SpecKit)

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json` para achar a pasta.
2. Leia `plan.md` e `spec.md` (e os artefatos de design, se existirem).
3. Escreva `tasks.md` agrupado em fases: preparacao, base comum, uma fase por
   historia de usuario (na ordem P1, P2, P3) e polimento.

## Formato de cada tarefa

`- [ ] T001 [P] [US1] Acao clara com o caminho do arquivo`

- numeracao sequencial na ordem de execucao
- `[P]` so quando da para fazer em paralelo (arquivos diferentes, sem dependencia)
- `[US<n>]` so nas tarefas de fase de historia

Cada historia precisa terminar entregavel sozinha. Todo caso de borda da spec
vira tarefa de teste.
