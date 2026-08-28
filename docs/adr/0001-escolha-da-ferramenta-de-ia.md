# ADR 0001 — Escolha da ferramenta de IA

- Status: Aceito
- Data: 2026-08-27

## Contexto
A atividade exige pelo menos uma ferramenta de IA para desenvolvimento, instalada,
autenticada e testada, cobrindo as categorias IDE+assistente e CLI agent.

## Decisão
Usar **Claude Code** (CLI agent) como ferramenta principal, complementada por
**VS Code + assistente** como IDE. Justificativa: Claude Code integra terminal, edição de
arquivos e Git no mesmo fluxo, suporta arquivos de contexto `CLAUDE.md` por escopo e
configuração de servidores MCP via `.mcp.json`, atendendo diretamente às Etapas 2 e 5.

## Consequências
- Contexto do projeto centralizado em `CLAUDE.md` (raiz) + regra por escopo em `src/saudacao/`.
- Integração MCP declarada em `.mcp.json`.
- Revisão humana obrigatória antes de aceitar commits/PRs gerados pela IA.
