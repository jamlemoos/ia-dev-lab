## Purpose

Permitir que a pessoa registre suas sessões de estudo de forma confiável, guardando data,
horário, duração e tópico, e impedindo que o histórico fique inconsistente com sessões
sobrepostas ou com dados inválidos.

## ADDED Requirements

### Requirement: Registro de uma sessão de estudo

O sistema SHALL permitir registrar uma sessão de estudo informando data, hora de início,
duração em minutos e tópico. Cada sessão registrada SHALL receber um identificador numérico
único e crescente, devolvido na confirmação, e SHALL ser persistida de modo a sobreviver ao
fim do processo.

#### Scenario: Sessão válida em horário livre
- **WHEN** a pessoa registra uma sessão em 2026-09-03 às 14:00 com duração de 90 minutos e
  tópico "SDD", e não há nenhuma outra sessão nesse dia
- **THEN** a sessão é gravada, a confirmação informa o identificador atribuído e o comando
  termina com código de saída 0

#### Scenario: Identificadores crescentes
- **WHEN** a pessoa registra duas sessões válidas em sequência
- **THEN** a segunda recebe um identificador maior que o da primeira, e nenhum identificador
  é reaproveitado

### Requirement: Recusa de sessões sobrepostas

O sistema SHALL recusar uma sessão cujo intervalo se sobreponha ao de qualquer sessão já
registrada no mesmo dia. A mensagem de recusa SHALL informar o identificador e o intervalo
da sessão conflitante. Dois intervalos que apenas se tocam nos extremos NÃO são considerados
sobreposição.

#### Scenario: Sobreposição parcial
- **WHEN** já existe a sessão 1 em 2026-09-03 das 14:00 às 15:30 e a pessoa tenta registrar
  uma sessão nesse dia às 14:30 com 30 minutos
- **THEN** nada é gravado, a mensagem cita a sessão 1 e o intervalo 14:00-15:30, e o código
  de saída é diferente de 0

#### Scenario: Sessões que se encostam
- **WHEN** já existe a sessão 1 em 2026-09-03 das 14:00 às 15:00 e a pessoa registra uma
  sessão nesse dia às 15:00 com 30 minutos
- **THEN** a sessão é aceita e gravada

#### Scenario: Mesmo horário em dias diferentes
- **WHEN** já existe a sessão 1 em 2026-09-03 das 14:00 às 15:00 e a pessoa registra uma
  sessão em 2026-09-04 das 14:00 às 15:00
- **THEN** a sessão é aceita, porque o conflito só existe dentro do mesmo dia

### Requirement: Validação dos dados da sessão

O sistema SHALL recusar uma sessão quando a data for posterior ao dia corrente, quando a
duração estiver fora do intervalo de 5 a 480 minutos (5 e 480 são aceitos), quando o tópico
for vazio ou composto apenas de espaços, ou quando a sessão não terminar no mesmo dia em que
começou. Cada recusa SHALL ter uma mensagem própria que identifique a regra violada.

#### Scenario: Data no futuro
- **WHEN** hoje é 2026-09-04 e a pessoa tenta registrar uma sessão em 2026-09-05
- **THEN** nada é gravado e a mensagem informa que não é possível registrar uma sessão futura

#### Scenario: Duração abaixo do mínimo
- **WHEN** a pessoa tenta registrar uma sessão com duração de 4 minutos
- **THEN** nada é gravado e a mensagem informa que a duração precisa estar entre 5 e 480 minutos

#### Scenario: Duração exatamente no limite
- **WHEN** a pessoa registra uma sessão válida com duração de 5 minutos e outra com 480 minutos
- **THEN** ambas são aceitas

#### Scenario: Tópico em branco
- **WHEN** a pessoa tenta registrar uma sessão cujo tópico contém apenas espaços
- **THEN** nada é gravado e a mensagem informa que o tópico é obrigatório

#### Scenario: Sessão que atravessa a meia-noite
- **WHEN** a pessoa tenta registrar uma sessão às 23:00 com duração de 90 minutos
- **THEN** nada é gravado e a mensagem informa que a sessão precisa terminar no mesmo dia

### Requirement: Preservação dos dados em caso de recusa

Quando uma sessão for recusada por qualquer motivo, o sistema SHALL deixar os dados
persistidos exatamente como estavam antes da tentativa.

#### Scenario: Arquivo intacto após recusa
- **WHEN** existem três sessões registradas e uma quarta é recusada por conflito de horário
- **THEN** o conteúdo persistido continua com as mesmas três sessões, sem alteração
