# Feature Specification: Resumo agregado de sessões de estudo

**Feature Branch**: `001-resumo-sessoes`

**Created**: 2026-09-04

**Status**: Draft

**Input**: User description: "Resumo agregado de sessões de estudo por período, com filtro por tópico e saída em texto ou JSON"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver para onde foi o tempo da semana (Priority: P1)

Depois de algumas semanas anotando sessões, a pessoa quer parar de olhar para uma lista crua
de registros e ver o quadro geral: quantas horas estudou no período e como esse tempo se
dividiu entre os assuntos. Ela roda um comando e recebe o total do período e a lista de
tópicos, do que consumiu mais tempo para o que consumiu menos, com o percentual de cada um.

**Why this priority**: É a razão de existir do registro. Sem esta visão, as sessões gravadas
não respondem a nenhuma pergunta, e a F1 sozinha é só um arquivo que cresce.

**Independent Test**: Registrar algumas sessões em dias diferentes da semana corrente e rodar
o resumo; o total precisa bater com a soma das durações e os percentuais com a divisão por
tópico.

**Acceptance Scenarios**:

1. **Given** que há sessões de 180 minutos em "SDD" e 90 minutos em "Git" na semana corrente,
   **When** a pessoa pede o resumo da semana, **Then** o resumo mostra o total de 4h30, o
   intervalo de datas do período, e os tópicos na ordem SDD (3h00, 67%) e Git (1h30, 33%).
2. **Given** que existem sessões dentro e fora da semana corrente, **When** a pessoa pede o
   resumo da semana, **Then** apenas as sessões da semana corrente entram na conta.
3. **Given** o mesmo conjunto de sessões, **When** a pessoa pede o resumo do mês,
   **Then** o período considerado passa a ser o mês corrente, do dia 1 ao último dia do mês.

---

### User Story 2 - Acompanhar um assunto específico (Priority: P2)

A pessoa está se preparando para uma entrega e quer saber quanto tempo dedicou a um assunto
só, sem o ruído dos outros. Ela pede o mesmo resumo, restrito a um tópico.

**Why this priority**: Agrega valor real, mas depende do resumo geral já existir. Se só a
User Story 1 for entregue, a funcionalidade já é útil.

**Independent Test**: Com sessões de dois tópicos no período, pedir o resumo filtrado por um
deles e conferir que o total corresponde só àquele tópico.

**Acceptance Scenarios**:

1. **Given** sessões de "SDD" e de "Git" na semana corrente, **When** a pessoa pede o resumo
   filtrado por "SDD", **Then** o total e a lista consideram apenas as sessões de "SDD", e o
   percentual desse tópico é 100%.
2. **Given** sessões apenas de "Git" no período, **When** a pessoa filtra por "SDD",
   **Then** o resumo informa que não há sessões para esse filtro no período.

---

### User Story 3 - Usar o resumo em outro programa (Priority: P3)

A pessoa quer levar os números para uma planilha ou um script, em vez de ler o relatório na
tela. Ela pede a mesma informação em JSON.

**Why this priority**: Conveniência. Nada do valor central se perde sem ela.

**Independent Test**: Rodar o resumo com saída JSON e conferir que o texto produzido é
carregável por um leitor de JSON e traz os mesmos números da saída em texto.

**Acceptance Scenarios**:

1. **Given** sessões no período, **When** a pessoa pede o resumo em JSON, **Then** a saída é
   um documento JSON válido com o intervalo do período, o total em minutos e a lista de
   tópicos com minutos e percentual.
2. **Given** um período sem sessões, **When** a pessoa pede o resumo em JSON, **Then** a saída
   ainda é um JSON válido, com total zero e lista de tópicos vazia.

---

### Edge Cases

- **Período sem nenhuma sessão**: em texto, o resumo diz explicitamente que não há sessões no
  período, em vez de imprimir um relatório com zeros ou falhar. Em JSON, devolve a estrutura
  completa com total zero.
- **Empate de total entre dois tópicos**: a ordem de desempate é alfabética, para que a saída
  seja sempre a mesma independentemente da ordem de gravação.
- **Percentuais que não somam 100%**: cada percentual é arredondado para inteiro de forma
  independente, então a soma pode dar 99% ou 101%. Isso é aceito e não é corrigido.
- **Filtro por tópico com caixa diferente**: o filtro compara sem diferenciar maiúsculas de
  minúsculas, porque "SDD" e "sdd" são o mesmo assunto para quem digitou.
- **Arquivo de dados ausente**: equivale a um período sem sessões, não a um erro.
- **Arquivo de dados de versão desconhecida ou malformado**: erro com mensagem clara, sem
  produzir um resumo possivelmente errado.
- **Sessão exatamente no primeiro ou no último dia do período**: entra no resumo; os limites
  do período são inclusivos nas duas pontas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST oferecer um comando de resumo que aceite o período `semana` ou
  `mes`, sendo `semana` o padrão quando nada for informado.
- **FR-002**: O período `semana` MUST corresponder à semana corrente de segunda a domingo, e
  o período `mes` ao mês corrente, do dia 1 ao último dia. Os dois limites são inclusivos.
- **FR-003**: O sistema MUST considerar apenas as sessões cuja data esteja dentro do período.
- **FR-004**: O sistema MUST apresentar o total de tempo do período e o total por tópico.
- **FR-005**: Os tópicos MUST ser ordenados do maior total para o menor, com desempate por
  ordem alfabética.
- **FR-006**: O sistema MUST apresentar, para cada tópico, o percentual do tempo do período,
  arredondado para inteiro, sem forçar que a soma seja 100%.
- **FR-007**: O sistema MUST aceitar um filtro opcional por tópico, comparado sem diferenciar
  maiúsculas de minúsculas.
- **FR-008**: O sistema MUST oferecer saída em texto legível e em JSON, sendo o texto o padrão.
- **FR-009**: Quando não houver nenhuma sessão no período, a saída em texto MUST informar isso
  explicitamente, e a saída em JSON MUST trazer total zero e lista de tópicos vazia.
- **FR-010**: O sistema MUST tratar a ausência do arquivo de dados como período sem sessões.
- **FR-011**: O sistema MUST recusar, com mensagem clara e sem stack trace, um arquivo de
  dados malformado ou de versão desconhecida.
- **FR-012**: O comando MUST terminar com código de saída 0 quando produzir um resumo,
  inclusive um resumo vazio, e diferente de 0 apenas em caso de erro.
- **FR-013**: O sistema MUST apresentar as durações em horas e minutos no formato `4h30` na
  saída em texto, e em minutos inteiros na saída em JSON.
- **FR-014**: O comando MUST ser somente leitura: nunca altera o arquivo de dados.

### Key Entities

- **Sessão**: um registro de estudo com data, hora de início, duração em minutos e tópico.
  Produzida pela funcionalidade de registro e descrita em `docs/formato-sessoes.md`.
- **Período**: intervalo de datas com início e fim inclusivos, derivado do dia corrente e do
  tipo de período escolhido.
- **Resumo**: o resultado da agregação, contendo o período, o total de minutos e uma lista de
  tópicos, cada um com seu total de minutos e seu percentual.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A pessoa descobre quanto estudou na semana e em quais assuntos com um único
  comando, sem abrir o arquivo de dados.
- **SC-002**: O total apresentado é igual à soma das durações das sessões do período em 100%
  dos casos, incluindo os dias que caem exatamente nos limites do período.
- **SC-003**: A mesma base de dados produz sempre a mesma ordem de tópicos, inclusive quando
  há empate de tempo.
- **SC-004**: A saída em JSON é carregável por um leitor de JSON padrão em 100% dos casos,
  inclusive quando o período está vazio.

## Assumptions

- O resumo lê os dados gravados pela funcionalidade de registro, no formato versão 1 descrito
  em `docs/formato-sessoes.md`. Não existe outra fonte de dados.
- Todas as datas são interpretadas no fuso local da máquina. O projeto é de uso pessoal em uma
  máquina só, então não há tratamento de fuso.
- Períodos personalizados (intervalo de datas arbitrário), comparação entre períodos e metas
  de estudo estão fora do escopo desta funcionalidade.
- Como a sessão sempre termina no mesmo dia em que começa, nenhuma sessão precisa ser dividida
  entre dois períodos.
