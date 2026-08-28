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
**Git/GitHub push e Pull Request:** o `gh` não estava instalado nem autenticado no ambiente.
**Resolvido:** instalei o `gh` via binário em `~/.local/bin` (sem `sudo`), autentiquei com
`gh auth login` e configurei o credential helper com `gh auth setup-git`. Repositório e PR
publicados com sucesso.

- Repositório: https://github.com/jamlemoos/ia-dev-lab
- Pull Request: https://github.com/jamlemoos/ia-dev-lab/pull/1

### Publicação (comandos usados)
```bash
gh repo create ia-dev-lab --public --source=. --remote=origin --push
git push -u origin feature/setup-inicial
gh pr create --base main --head feature/setup-inicial \
  --title "Setup inicial do ia-dev-lab" --body "Estrutura, CLAUDE.md, ADR, MCP e testes."
```

## Checklist de entrega
- [x] Repositório com histórico de commits (publicado no GitHub)
- [x] `CLAUDE.md` + regra customizada de escopo (`src/saudacao/CLAUDE.md`)
- [x] Estrutura organizada, `README.md` e ADR em `docs/adr/`
- [x] `docs/prompts-comparacao.md`
- [x] Pull Request aberto (#1)
- [x] `.mcp.json`
- [x] Relatório final (este arquivo)
