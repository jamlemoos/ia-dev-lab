---
name: "speckit-taskstoissues"
description: "Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts."
argument-hint: "Optional filter or label for GitHub issues"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/taskstoissues.md"
user-invocable: true
disable-model-invocation: false
---

# Transformar tarefas em issues do GitHub (SpecKit)

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json` para achar a pasta.
2. Leia `tasks.md` e monte a lista de ids que vao virar issue.
3. Confira o que ja existe (`gh issue list`) para nao duplicar.
4. Crie uma issue por tarefa com `gh issue create`, com o id no titulo, o
   contexto no corpo e o link para a spec.
5. Registre o numero da issue ao lado da tarefa em `tasks.md`.

Confirme com o usuario antes de criar, porque issue criada aparece para todo
mundo no repositorio.
