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
| `python -m src.estudo.cli add --data AAAA-MM-DD --inicio HH:MM --dur MIN --topico ASSUNTO` | Registra uma sessão de estudo |
| `python -m src.estudo.cli resumo [--periodo semana\|mes] [--topico X] [--formato texto\|json]` | Resume as sessões do período |
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
|-- openspec/            (spec do registro de sessões, via OpenSpec)
|-- specs/               (spec do resumo agregado, via SpecKit)
|-- src/saudacao/        (hello.py + regra customizada de escopo)
|-- src/estudo/          (regras.py, armazenamento.py, resumo.py, cli.py)
`-- tests/               (test_hello, test_regras, test_cli_add, test_resumo, test_cli_resumo)
```

> Nota: adicionar CI de testes em iteração futura.

## Registro de sessões de estudo

```bash
python -m src.estudo.cli add --data 2026-09-03 --inicio 14:00 --dur 90 --topico SDD
```

Regras: a duração vai de 5 a 480 minutos, a data não pode ser futura, a sessão precisa
terminar no mesmo dia e não pode se sobrepor a outra já registrada (encostar é permitido).
Os dados ficam em `data/sessoes.json`, fora do controle de versão; o formato está descrito
em [docs/formato-sessoes.md](docs/formato-sessoes.md). Use `--arquivo` para apontar outro
caminho.

## Resumo das sessões

```bash
python -m src.estudo.cli resumo                      # semana corrente, de segunda a domingo
python -m src.estudo.cli resumo --periodo mes        # mês corrente
python -m src.estudo.cli resumo --topico SDD         # só um assunto (ignora maiúsculas)
python -m src.estudo.cli resumo --formato json       # para usar em outro programa
```

Os tópicos aparecem do que consumiu mais tempo para o que consumiu menos, com empate
resolvido em ordem alfabética. Os percentuais são arredondados para inteiro, então a soma
pode dar 99% ou 101%. Um período sem sessões avisa isso e ainda sai com código 0.
