---
name: "speckit-constitution"
description: "Create or update the project constitution from interactive or provided principle inputs."
argument-hint: "Principles or values for the project constitution"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/constitution.md"
user-invocable: true
disable-model-invocation: false
---

# Constituicao do projeto (SpecKit)

Cria ou atualiza `.specify/memory/constitution.md`: os principios que valem para
todas as funcionalidades.

## Passos

1. Leia a constituicao atual, se existir.
2. Colete os principios com o usuario. Cada um precisa ser verificavel:
   "so a biblioteca padrao" da para conferir, "codigo limpo" nao.
3. Escreva cada principio com nome, regra e o motivo dela existir.
4. Atualize a versao no rodape (semver) e a data da ultima emenda.
5. Diga quais specs e planos existentes podem ter ficado em conflito.

Nao invente principio que o usuario nao pediu. Nao mexa em codigo aqui.
