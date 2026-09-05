---
name: openspec-propose
description: Propose a new change with all artifacts generated in one step. Use when the user wants to quickly describe what they want to build and get a complete proposal with design, specs, and tasks ready for implementation.
allowed-tools: Bash(openspec:*)
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.12.0"
---

# Propor uma mudanca (OpenSpec)

Cria a mudanca e escreve todos os artefatos de planejamento de uma vez.
Nao escreva codigo aqui. Planejamento so.

## Passos

1. Entenda o pedido. Se algo ambiguo mudar o escopo, pergunte antes.
2. Escolha o schema do fluxo (`openspec status --json` mostra os disponiveis).
3. Crie a pasta da mudanca:
   `openspec new change "<nome-em-kebab-case>"`
4. Descubra a ordem dos artefatos:
   `openspec status --change "<nome>" --json`
5. Para cada artefato, na ordem:
   - `openspec instructions <id> --change "<nome>" --json`
   - escreva o arquivo no caminho que as instrucoes indicarem
6. Valide: `openspec validate "<nome>" --strict`
7. Mostre o status final e diga qual e o proximo passo (`/opsx:apply`).

## Cuidados

- `#### Scenario:` usa exatamente quatro `#`. Menos que isso e a validacao falha.
- Cada spec delta precisa de `## Purpose` com pelo menos 50 caracteres.
- Toda requirement precisa de pelo menos um cenario.
