## Why

Hoje o `ia-dev-lab` não guarda nada: a única funcionalidade é uma saudação sem estado. Quem
estuda por conta própria não tem como saber depois onde o tempo foi parar, e anotar em
caderno ou planilha some rápido. O primeiro passo é conseguir registrar uma sessão de estudo
de forma confiável, sem deixar o histórico bagunçado com horários que se atropelam.

## What Changes

- Novo comando `estudo add`, que registra uma sessão com data, hora de início, duração em
  minutos e tópico.
- Nova persistência local em `data/sessoes.json`, com formato documentado, porque a
  funcionalidade de resumo (F2) vai ler esses mesmos dados.
- Novas regras de validação: data no futuro, duração fora de 5 a 480 minutos, tópico vazio,
  sessão que não termina no mesmo dia e sobreposição com uma sessão já registrada.
- Sessões que apenas se encostam (uma termina no minuto em que a outra começa) continuam
  válidas.
- Nenhuma mudança em comportamento existente. A saudação segue igual.

## Capabilities

### New Capabilities

- `registro-sessoes`: registrar sessões de estudo, com validação de entrada, detecção de
  conflito de horário e persistência local.

### Modified Capabilities

Nenhuma. Este é o primeiro comando com estado do projeto.

## Impact

- Código novo em `src/estudo/` (regras, armazenamento e interface de linha de comando).
- Testes novos em `tests/`.
- Arquivo de dados `data/sessoes.json`, que entra no `.gitignore`.
- Sem dependências externas: só a biblioteca padrão do Python 3.
- `README.md` e `CLAUDE.md` passam a citar o novo comando.
