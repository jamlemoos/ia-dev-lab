---

description: "Plano de tarefas do resumo agregado de sessões de estudo"
---

# Tasks: Resumo agregado de sessões de estudo

**Input**: Design documents from `/specs/001-resumo-sessoes/`

**Prerequisites**: plan.md, spec.md

**Tests**: incluídos. O princípio IV da constituição exige teste para cada caso de borda.

**Organization**: tarefas agrupadas por user story, para que cada uma possa ser entregue e
testada sozinha.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: pode rodar em paralelo (arquivos diferentes, sem dependência)
- **[Story]**: a que user story a tarefa pertence

---

## Phase 1: Foundational (bloqueia todas as user stories)

**Purpose**: a base compartilhada pelas três histórias.

- [ ] T001 Criar `src/estudo/resumo.py` com `periodo_da_semana(hoje)` e `periodo_do_mes(hoje)`,
      devolvendo o par de datas ISO com limites inclusivos. Recebem a data de referência por
      parâmetro, nunca chamam `date.today()`.
- [ ] T002 [P] Criar `tests/test_resumo.py` com os testes de período: semana de segunda a
      domingo, mês do dia 1 ao último dia, e virada de mês e de ano.
- [ ] T003 Implementar `agregar(sessoes, periodo, topico=None)` em `src/estudo/resumo.py`,
      devolvendo `{"inicio", "fim", "total_min", "topicos": [{"topico", "minutos",
      "percentual"}]}`, com filtro de período inclusivo e filtro opcional de tópico sem
      diferenciar maiúsculas.

**Checkpoint**: a agregação existe e é testável sem tocar em disco.

---

## Phase 2: User Story 1 - Ver para onde foi o tempo da semana (P1) 🎯 MVP

**Goal**: total do período e divisão por tópico, ordenada, na saída em texto.

**Independent Test**: registrar sessões na semana corrente e rodar `estudo resumo`; o total
precisa bater com a soma das durações.

- [ ] T004 [US1] Ordenar os tópicos por `(-minutos, topico)` e calcular o percentual inteiro
      de cada um em `agregar()`.
- [ ] T005 [P] [US1] Testes de agregação em `tests/test_resumo.py`: total correto, ordem por
      tempo, **empate resolvido em ordem alfabética** e sessões fora do período ignoradas.
- [ ] T006 [P] [US1] Teste dos limites do período: sessão exatamente na segunda-feira e
      exatamente no domingo entram no resumo.
- [ ] T007 [US1] Implementar `formatar_texto(resumo)` em `src/estudo/resumo.py`, com o total
      no formato `4h30` e uma linha por tópico com minutos e percentual.
- [ ] T008 [US1] Acrescentar o subcomando `resumo` ao `argparse` de `src/estudo/cli.py`, com
      `--periodo` (padrão `semana`), sem alterar o subcomando `add`.
- [ ] T009 [US1] Escrever `tests/test_cli_resumo.py` cobrindo o resumo da semana e o do mês
      ponta a ponta, com arquivo temporário e código de saída 0.

**Checkpoint**: a funcionalidade já é útil sozinha.

---

## Phase 3: User Story 2 - Acompanhar um assunto específico (P2)

**Goal**: o mesmo resumo, restrito a um tópico.

**Independent Test**: com dois tópicos no período, filtrar por um e conferir o total.

- [ ] T010 [US2] Acrescentar `--topico` ao subcomando `resumo` em `src/estudo/cli.py`.
- [ ] T011 [P] [US2] Testes do filtro: comparação sem diferenciar maiúsculas, percentual de
      100% quando sobra um tópico só, e mensagem própria quando o filtro não encontra nada.

---

## Phase 4: User Story 3 - Usar o resumo em outro programa (P3)

**Goal**: a mesma informação em JSON.

**Independent Test**: rodar com `--formato json` e carregar a saída com um leitor de JSON.

- [ ] T012 [US3] Implementar `formatar_json(resumo)` e o argumento `--formato`
      (`texto` por padrão, `json` opcional) em `src/estudo/cli.py`.
- [ ] T013 [P] [US3] Testes: a saída é JSON válido, traz os mesmos números da saída em texto,
      e continua válida com o período vazio (total zero, lista vazia).

---

## Phase 5: Casos de borda e erros

- [ ] T014 Tratar o período sem sessões: mensagem explícita em texto, estrutura zerada em
      JSON, código de saída 0 nos dois casos.
- [ ] T015 [P] Testes de erro reaproveitando `armazenamento.carregar`: arquivo ausente é
      tratado como período vazio; arquivo malformado ou de versão desconhecida devolve
      mensagem clara e código 1, sem stack trace.
- [ ] T016 Teste que garante que o comando `resumo` não altera o arquivo de dados: comparar o
      conteúdo antes e depois.

---

## Phase 6: Polish

- [ ] T017 Atualizar `README.md`, `CLAUDE.md` e `docs/escopo.md` com o comando `estudo resumo`.
- [ ] T018 Rodar `python -m pytest -q` com a suíte inteira e conferir que os testes da F1
      continuam passando.

---

## Dependencies & Execution Order

- Phase 1 bloqueia todas as histórias: sem `agregar()` e sem o recorte de período, nenhuma
  história funciona.
- US1 (P1) é o MVP. US2 e US3 dependem de US1 apenas por reaproveitarem `agregar()` e a
  estrutura de saída; nenhuma das duas mexe no que a US1 entregou.
- Phase 5 pode ser feita logo depois da US1, mas fica no fim para não interromper a entrega
  incremental.
- Phase 6 depende de tudo.

### Parallel Opportunities

- T002 pode ser escrito junto com T001 (arquivos diferentes).
- T005, T006, T011, T013 e T015 são testes em arquivos separados da implementação e podem ser
  escritos em paralelo com ela.

## Notes

- Commit ao fim de cada fase.
- Cada caso de borda da spec tem uma tarefa de teste correspondente: T005 (empate), T006
  (limites do período), T011 (caixa do filtro e filtro vazio), T013 (JSON vazio), T014 e T015
  (período sem sessões e arquivo problemático).
