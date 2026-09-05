---
name: openspec-sync-specs
description: Sync delta specs from a change to main specs. Use when the user wants to update main specs with changes from a delta spec, without archiving the change.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.12.0"
---

# Sincronizar specs delta com as specs principais (OpenSpec)

Leva o que esta nos deltas da mudanca para as specs principais, sem arquivar a mudanca.

## Passos

1. Escolha a mudanca.
2. `openspec status --change "<nome>" --json` para achar o caminho dos deltas.
3. Localize os arquivos em `openspec/changes/<nome>/specs/<capability>/spec.md`.
4. Para cada delta, aplique na spec principal `openspec/specs/<capability>/spec.md`:
   - `## ADDED Requirements` -> acrescenta
   - `## MODIFIED Requirements` -> substitui a requirement de mesmo nome
   - `## REMOVED Requirements` -> remove
   - `## RENAMED Requirements` -> renomeia, mantendo o conteudo
   Se a spec principal nao existir, crie com `# <capability> Specification`,
   `## Purpose` e `## Requirements`.
5. `openspec validate --strict` nas specs alteradas.
6. Resuma o que entrou, saiu e mudou.
