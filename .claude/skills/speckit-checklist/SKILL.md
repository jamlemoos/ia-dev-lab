---
name: "speckit-checklist"
description: "Generate a custom checklist for the current feature based on user requirements."
argument-hint: "Domain or focus area for the checklist"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/checklist.md"
user-invocable: true
disable-model-invocation: false
---

# Gerar um checklist (SpecKit)

Cria um checklist de revisao para um aspecto da funcionalidade (seguranca,
acessibilidade, dados, o que o usuario pedir).

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json --template checklist`
   para achar a pasta.
2. Leia a constituicao e os artefatos da funcionalidade.
3. Faca ate 3 perguntas para saber o foco e a profundidade.
4. Escreva o checklist em `checklists/<assunto>.md`, item por item.

## O que faz um item bom

- verifica a qualidade do que esta escrito na spec, nao o comportamento do codigo
- da para responder sim ou nao olhando os artefatos
- aponta o requisito ou a secao a que se refere

Nao repita item, nao gere teste de codigo disfarcado de checklist.
