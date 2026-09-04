# Escopo — Prática Assíncrona da Aula 4 (De Spec a Código)

**Projeto:** `ia-dev-lab`, o mesmo repositório que comecei na prática da Aula 2.
**Estado atual:** só existe a função `saudacao` em `src/saudacao/hello.py` e três testes.

## Funcionalidades escolhidas

### F1 — Registro de sessões de estudo (`estudo add`)

Um comando de terminal para anotar uma sessão de estudo: data, hora de início, duração em
minutos e tópico. Os registros ficam salvos em um arquivo JSON local.

Cenários de uso:

1. **Registro válido.** Anoto uma sessão em um horário livre e recebo de volta o id gerado.
2. **Conflito de horário.** Tento anotar uma sessão que se sobrepõe a outra do mesmo dia. O
   comando recusa e diz com qual sessão houve o conflito.
3. **Entrada inválida.** Data no futuro, duração fora da faixa permitida (5 a 480 minutos)
   ou tópico em branco. O comando recusa com uma mensagem específica e não grava nada.

### F2 — Resumo agregado (`estudo resumo`)

Um comando que soma as sessões já registradas por período (semana ou mês), com filtro
opcional por tópico e saída em texto ou em JSON.

Cenários de uso:

1. **Resumo da semana.** Mostra o total de horas do período e quanto cada tópico representa,
   do maior para o menor.
2. **Filtro por tópico.** O mesmo resumo, restrito a um tópico, para acompanhar um assunto
   de perto.
3. **Período sem sessões.** Em vez de imprimir um relatório vazio ou quebrar, o comando
   avisa que não há dados naquele período.

## Por que são um bom caso para SDD

Escolhi essas duas porque elas obrigam a decidir várias regras antes de escrever código.
Qual é a duração mínima e máxima de uma sessão, o que exatamente conta como sobreposição de
horário, se a semana começa no domingo ou na segunda, como arredondar os percentuais do
resumo: nada disso está no código de hoje e nada disso o agente tem como adivinhar. Junto
com isso vêm casos de borda que só aparecem quando a gente para para pensar, como uma sessão
que começa no minuto exato em que a anterior termina, um período sem nenhum registro e um
empate de percentual entre dois tópicos. A implementação também não cabe em um arquivo só,
porque precisa de persistência, das regras de validação e da interface de linha de comando,
além dos testes, então a ordem das tarefas passa a importar de verdade. E como a F2 lê os
dados que a F1 grava, a especificação precisa fechar o formato desses dados antes, senão as
duas partes saem incompatíveis.

## Divisão por ferramenta (Etapas 2 e 5)

| Funcionalidade | Ferramenta de especificação |
|---|---|
| F1 — `estudo add` | OpenSpec |
| F2 — `estudo resumo` | SpecKit |

As duas foram implementadas. A comparação entre as ferramentas está em
[docs/comparacao-ferramentas.md](comparacao-ferramentas.md).
