# CLAUDE.md

## Sobre o projeto
`ia-dev-lab` é um laboratório de prática do fluxo de desenvolvimento assistido por IA
(configuração de ambiente, contexto de projeto, boas práticas de prompt e integração
Git/GitHub/MCP). As funcionalidades são uma saudação em Python e o registro de sessões de estudo
(`src/estudo/`). O registro foi especificado com OpenSpec (`openspec/`) e o resumo com
SpecKit (`specs/` e `.specify/`).

## Comandos
- `python -m src.saudacao.hello` -> executa a saudação padrão
- `python -m src.estudo.cli add --data ... --inicio ... --dur ... --topico ...` -> registra sessão
- `python -m src.estudo.cli resumo [--periodo semana|mes] [--topico X] [--formato texto|json]` -> resume o período
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
- Não fazer merge de PR sem revisão humana (checkpoint obrigatório, ver docs/checkpoint.md)
- Não alterar o formato de `data/sessoes.json` sem subir `versao` e atualizar docs/formato-sessoes.md
