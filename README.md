# ia-dev-lab

Laboratório de prática de desenvolvimento de software assistido por IA — Programa de
Pós-Graduação em TI / IMD-UFRN. Configuração de ambiente, contexto de projeto (CLAUDE.md),
boas práticas de prompt e integração com Git/GitHub e MCP.

## Instalação
```bash
git clone <url-do-repo>
cd ia-dev-lab
python3 -m venv .venv && source .venv/bin/activate   # opcional
pip install pytest                                    # só para rodar os testes
```

## Comandos principais
| Comando | O que faz |
|---|---|
| `python -m src.saudacao.hello` | Executa a saudação |
| `python -m pytest -q` | Roda os testes |

## Estrutura
```
ia-dev-lab/
|-- CLAUDE.md
|-- README.md
|-- .mcp.json
|-- docs/
|   |-- adr/0001-escolha-da-ferramenta-de-ia.md
|   `-- prompts-comparacao.md
|-- src/saudacao/        (hello.py + regra customizada de escopo)
`-- tests/               (test_hello.py)
```
