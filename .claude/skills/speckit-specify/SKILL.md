---
name: "speckit-specify"
description: "Create or update the feature specification from a natural language feature description."
argument-hint: "Describe the feature you want to specify"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/specify.md"
user-invocable: true
disable-model-invocation: false
---

# Escrever a spec da funcionalidade (SpecKit)

## Passos

1. `.specify/scripts/bash/create-new-feature.sh --json "<descricao>"` e leia
   `BRANCH_NAME` e `SPEC_FILE` do JSON.
2. Leia `.specify/memory/constitution.md`.
3. Escreva `spec.md` a partir de `.specify/templates/spec-template.md`, com:
   - historias de usuario priorizadas (P1, P2, P3), cada uma com o porque da
     prioridade, um teste independente e cenarios de aceite
   - casos de borda
   - requisitos funcionais numerados (FR-001...)
   - criterios de sucesso mensuraveis (SC-001...), sem falar de tecnologia
   - secao de premissas
4. Revise o que escreveu: todo requisito precisa ser testavel e sem ambiguidade.

## Regras

- Comportamento observavel, nao implementacao. Nada de framework ou classe aqui.
- Preencha lacunas com um padrao razoavel e registre em Premissas.
- No maximo 3 marcas `[NEEDS CLARIFICATION]`, so para decisoes que mudam o escopo.
