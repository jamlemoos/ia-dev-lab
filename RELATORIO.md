# Relatório Final — Configuração do Ambiente e Fluxo de Trabalho com IA

**Aluna:** Maria Macedo · **Data:** 2026-08-27

## 1. Ferramenta(s) de IA e por quê
Configurei **Claude Code** (CLI agent) como ferramenta principal e **VS Code + assistente**
como IDE. O Claude Code une terminal, edição e Git no mesmo fluxo, lê arquivos `CLAUDE.md` por
escopo e integra servidores MCP via `.mcp.json` — cobrindo diretamente as Etapas 2 e 5.

## 2. Trecho mais útil do CLAUDE.md
```
## Comandos
- `python -m src.saudacao.hello` -> executa a saudação padrão
- `python -m pytest -q` -> roda os testes
```
Útil porque responde na hora "qual comando roda os testes?" sem a IA inventar caminhos.

## 3. Prompt fraco vs. prompt eficaz
O prompt fraco ("faz uma função de saudação") gerou código com `print`, sem type hints e sem
tratar entrada vazia. O prompt eficaz — com contexto, exemplo de assinatura, restrições e
critério de validação — gerou a função tipada, com fallback e testes pytest de uma só vez.
Detalhes em `docs/prompts-comparacao.md`.

## 4. Obstáculo enfrentado e resolução
**Git/GitHub push e Pull Request:** o ambiente local não tinha o `gh` autenticado, então o
push e a abertura do PR não puderam ser concluídos automaticamente. Resolução: deixei o
repositório local completo com a branch `feature/setup-inicial` e commits, e documentei os
comandos exatos de publicação abaixo para rodar após autenticar.

### Publicação (rodar após `gh auth login`)
```bash
gh repo create ia-dev-lab --public --source=. --remote=origin --push
git push -u origin feature/setup-inicial
gh pr create --base main --head feature/setup-inicial \
  --title "Setup inicial do ia-dev-lab" --body "Estrutura, CLAUDE.md, ADR, MCP e testes."
```

## Checklist de entrega
- [x] Repositório com histórico de commits (local; push documentado acima)
- [x] `CLAUDE.md` + regra customizada de escopo (`src/saudacao/CLAUDE.md`)
- [x] Estrutura organizada, `README.md` e ADR em `docs/adr/`
- [x] `docs/prompts-comparacao.md`
- [~] Pull Request (comandos prontos; requer `gh auth login`)
- [x] `.mcp.json`
- [x] Relatório final (este arquivo)
