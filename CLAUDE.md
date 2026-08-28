# CLAUDE.md

## Sobre o projeto
`ia-dev-lab` é um laboratório de prática do fluxo de desenvolvimento assistido por IA
(configuração de ambiente, contexto de projeto, boas práticas de prompt e integração
Git/GitHub/MCP). A funcionalidade de exemplo é uma função de saudação em Python.

## Comandos
- `python -m src.saudacao.hello` -> executa a saudação padrão
- `python -m pytest -q` -> roda os testes
- `git add -A && git commit` -> versiona alterações

## Convenções de código
- Python 3, type hints em funções públicas
- Organização por domínio/funcionalidade em `src/` (não por tipo técnico)
- Testes em `tests/`, um arquivo `test_*.py` por módulo
- Mensagens de commit no imperativo, curtas

## Não fazer
- Não adicionar dependências externas sem necessidade
- Não commitar segredos, `.env` ou credenciais
- Não fazer merge de PR sem revisão humana
