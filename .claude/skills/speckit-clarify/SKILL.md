---
name: "speckit-clarify"
description: "Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec."
argument-hint: "Optional areas to clarify in the spec"
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "templates/commands/clarify.md"
user-invocable: true
disable-model-invocation: false
---

# Clarificar a spec (SpecKit)

Acha os pontos vagos da spec e transforma as respostas em texto dentro dela.

## Passos

1. `.specify/scripts/bash/check-prerequisites.sh --json` para achar a pasta da
   funcionalidade. Leia `spec.md` e a constituicao.
2. Liste os pontos ambiguos por impacto: escopo > seguranca e privacidade >
   experiencia de uso > detalhe tecnico.
3. Faca ate 5 perguntas, uma de cada vez, com opcoes concretas quando der.
4. Depois de cada resposta, edite a spec na hora, na secao certa
   (requisito, caso de borda ou premissa). Nao acumule tudo para o fim.
5. No fim, diga o que mudou e o que continua em aberto.

Nao pergunte o que a propria spec ja responde.
