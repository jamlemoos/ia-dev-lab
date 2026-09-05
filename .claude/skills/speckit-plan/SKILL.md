---
name: "speckit-plan"
description: "Execute the implementation planning workflow using the plan template to generate design artifacts."
argument-hint: "Optional guidance for the planning phase"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/plan.md"
user-invocable: true
disable-model-invocation: false
---

# Plano tecnico (SpecKit)

## Passos

1. `.specify/scripts/bash/setup-plan.sh --json` e leia os caminhos do JSON.
2. Leia `spec.md` e `.specify/memory/constitution.md`.
3. Escreva `plan.md` a partir do template, com:
   - resumo do que vai ser feito
   - contexto tecnico (linguagem, dependencias, armazenamento, testes, escala)
   - Constitution Check: principio por principio, atendido ou nao
   - estrutura de arquivos que vai mudar ou nascer
   - decisoes tecnicas, cada uma com o motivo
   - Complexity Tracking: so o que viola a constituicao, com justificativa
4. Gere `research.md`, `data-model.md` ou `contracts/` apenas se fizerem falta.
   Se nao gerar, escreva no plano por que nao.

Se o Constitution Check falhar e nao houver justificativa, ajuste o plano
antes de seguir para as tarefas.
