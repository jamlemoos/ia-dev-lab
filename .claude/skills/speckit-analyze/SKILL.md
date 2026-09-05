---
name: "speckit-analyze"
description: "Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation."
argument-hint: "Optional focus areas for analysis"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/analyze.md"
user-invocable: true
disable-model-invocation: false
---

# Analisar a coerencia dos artefatos (SpecKit)

Compara `spec.md`, `plan.md` e `tasks.md` entre si. Nao altera nenhum deles.

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json` para achar a pasta.
2. Leia os tres arquivos e a constituicao.
3. Procure:
   - requisito da spec sem tarefa correspondente
   - tarefa que nao serve a nenhum requisito
   - contradicao entre spec e plano
   - termo usado com dois sentidos diferentes
   - violacao da constituicao sem justificativa
4. Classifique cada achado em critico, alto, medio ou baixo.
5. Apresente uma tabela: id, severidade, onde esta, o que esta errado.
6. Ofereca corrigir. So corrija se o usuario pedir.
