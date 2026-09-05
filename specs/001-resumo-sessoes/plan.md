# Implementation Plan: Resumo agregado de sessões de estudo

**Branch**: `001-resumo-sessoes` | **Date**: 2026-09-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-resumo-sessoes/spec.md`

## Summary

Acrescentar o subcomando `estudo resumo`, que lê as sessões gravadas pela F1, filtra pelo
período (semana corrente de segunda a domingo, ou mês corrente) e opcionalmente por tópico, e
apresenta o total do período e a divisão por tópico, em texto ou em JSON. A agregação fica em
um módulo próprio de funções puras, reaproveitando a leitura já existente em
`src/estudo/armazenamento.py`; a interface entra como um segundo subcomando no `argparse` que
já existe, sem mexer no `add`.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: nenhuma. Só a biblioteca padrão (`datetime`, `json`, `argparse`),
como manda o princípio III da constituição.

**Storage**: o arquivo `data/sessoes.json`, formato versão 1, descrito em
`docs/formato-sessoes.md`. Somente leitura nesta funcionalidade.

**Testing**: pytest

**Target Platform**: linha de comando, Linux e macOS

**Project Type**: CLI de uso pessoal

**Performance Goals**: irrelevante na prática. Dezenas de sessões por mês, arquivo lido
inteiro na memória.

**Constraints**: nenhuma escrita no arquivo de dados; saída JSON sempre carregável; sem stack
trace em erro de uso.

**Scale/Scope**: um usuário, um arquivo, centenas de registros por ano.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio | Situação |
|---|---|
| I. Spec antes de código | Atendido. A spec desta funcionalidade veio antes, e as decisões de semana, empate e arredondamento foram fechadas nela. |
| II. Regras isoladas da interface | Atendido. A agregação vai para `src/estudo/resumo.py`, em funções puras que recebem a lista de sessões e a data de referência. A formatação de texto e JSON também não depende do `argparse`. |
| III. Só a biblioteca padrão | Atendido. Nada de novo. |
| IV. Cada caso de borda vira teste | Atendido pelo plano de tarefas: período vazio, empate alfabético, limites do período, caixa do filtro e soma que não fecha 100% têm teste próprio. |
| V. Revisão humana antes do merge | Atendido pelo processo: a funcionalidade entra pelo mesmo PR, com revisão do diff. |

Nenhuma violação. Nenhuma exceção precisa ser registrada em Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/001-resumo-sessoes/
├── spec.md              # especificação da funcionalidade
├── plan.md              # este arquivo
└── tasks.md             # plano de tarefas
```

Não foram gerados `research.md`, `data-model.md` nem `contracts/`: não há tecnologia
desconhecida a pesquisar, o modelo de dados já está fixado em `docs/formato-sessoes.md` e a
interface é um comando de terminal, não uma API.

### Source Code (repository root)

```text
src/estudo/
├── regras.py            # já existe (F1)
├── armazenamento.py     # já existe (F1), reaproveitado para leitura
├── resumo.py            # NOVO: recorte do período, agregação e formatação
└── cli.py               # MODIFICADO: novo subcomando `resumo`

tests/
├── test_regras.py       # já existe
├── test_cli_add.py      # já existe
├── test_resumo.py       # NOVO: agregação e formatação, sem tocar em disco
└── test_cli_resumo.py   # NOVO: ponta a ponta, com arquivo temporário
```

## Decisões técnicas

**Recorte do período calculado a partir de uma data de referência recebida por parâmetro.**
As funções de período recebem `hoje` em vez de chamar `date.today()` internamente, senão os
testes dependeriam do dia em que rodam. A semana usa `hoje - timedelta(days=hoje.weekday())`
como segunda-feira, e o mês vai do dia 1 ao último dia obtido por `calendar.monthrange`.

**Comparação de datas como texto ISO.**
As datas estão gravadas como `AAAA-MM-DD`, formato que ordena corretamente por comparação de
string. Comparar `inicio_iso <= sessao["data"] <= fim_iso` evita converter todas as sessões
para `date` só para filtrar.

**Ordenação por `(-minutos, topico)`.**
Uma chave só resolve o critério principal e o desempate alfabético, sem ordenar duas vezes.

**Formatação separada da agregação.**
`agregar()` devolve uma estrutura de dados; `formatar_texto()` e `formatar_json()` recebem
essa estrutura. Assim os dois formatos provam que mostram os mesmos números, e o teste da
agregação não precisa ler texto.

**Filtro por tópico comparado em minúsculas, preservando o texto original na saída.**
Quem digitou `sdd` deve encontrar as sessões de `SDD`, mas o relatório mostra o tópico como
foi gravado.

## Complexity Tracking

Nada a registrar. Nenhuma exceção à constituição foi necessária.
