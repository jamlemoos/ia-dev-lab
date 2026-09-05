# F1 — Registro de sessões de estudo (`estudo add`)

Especificação escrita seguindo o fluxo de SDD: user story, requisitos, critérios de aceite
e plano de tarefas. Ferramenta usada para estruturar: **OpenSpec** (ver
`openspec/changes/add-registro-sessoes/`).

## 1. Prompt inicial (user story)

> Como alguém que estuda por conta própria, quero anotar cada sessão de estudo que eu faço,
> dizendo o dia, a hora em que comecei, quanto tempo durou e o assunto, para depois conseguir
> olhar para trás e saber onde meu tempo foi parar. Se eu me atrapalhar e tentar anotar uma
> sessão em cima de outra que já registrei, quero ser avisado na hora e saber com qual delas
> bateu, em vez de descobrir o problema semanas depois com o histórico já bagunçado. Anotar
> uma sessão tem que ser rápido, senão eu simplesmente paro de anotar.

Nenhuma decisão técnica aqui de propósito: nada de formato de arquivo, biblioteca ou
estrutura de pastas. Isso é decidido só no design.

## 2. Requisitos (PRD)

**Funcionais**

- RF1. O sistema deve permitir registrar uma sessão informando data, hora de início,
  duração em minutos e tópico.
- RF2. Cada sessão registrada recebe um identificador numérico único e crescente, devolvido
  ao usuário na confirmação.
- RF3. As sessões devem ser guardadas de forma persistente, sobrevivendo ao fim do processo.
- RF4. O sistema deve recusar uma sessão cujo intervalo se sobreponha ao de outra sessão já
  registrada, informando o id e o horário da sessão conflitante.
- RF5. Duas sessões que apenas se encostam (uma termina exatamente quando a outra começa)
  não são consideradas conflito.
- RF6. O sistema deve recusar data no futuro em relação ao dia corrente.
- RF7. A duração deve estar entre 5 e 480 minutos, sendo 5 e 480 valores aceitos; qualquer
  valor fora dessa faixa é recusado.
- RF8. O sistema deve recusar tópico vazio ou composto só de espaços.
- RF9. O sistema deve recusar uma sessão que não termine no mesmo dia em que começou.
- RF10. Qualquer recusa deve deixar o arquivo de dados exatamente como estava antes.
- RF11. Cada recusa deve ter uma mensagem própria, que diga qual regra foi violada.

**Não funcionais**

- RNF1. Sem dependências externas: só a biblioteca padrão do Python 3.
- RNF2. O comando deve terminar com código de saída 0 em sucesso e diferente de 0 em erro,
  para poder ser usado em script.
- RNF3. As regras de validação devem ser testáveis sem tocar no disco real.

**Fora de escopo**

- Editar ou apagar sessões já registradas.
- Sessões que atravessam a meia-noite.
- Qualquer relatório ou agregação (isso é a F2).
- Múltiplos usuários ou sincronização.

## 3. Critérios de aceite

**CA1 — Registro válido**
- **Given** que não existe nenhuma sessão registrada no dia 2026-09-03
- **When** eu executo `estudo add --data 2026-09-03 --inicio 14:00 --dur 90 --topico SDD`
- **Then** a sessão é gravada, o comando responde com o id gerado e termina com código 0.

**CA2 — Conflito de horário**
- **Given** que já existe a sessão de id 1 em 2026-09-03 das 14:00 às 15:30
- **When** eu executo `estudo add --data 2026-09-03 --inicio 14:30 --dur 30 --topico Git`
- **Then** nada é gravado, a mensagem cita o id 1 e o intervalo 14:00-15:30, e o código de
  saída é diferente de 0.

**CA3 — Caso de borda: sessões encostadas**
- **Given** que já existe a sessão de id 1 em 2026-09-03 das 14:00 às 15:00
- **When** eu executo `estudo add --data 2026-09-03 --inicio 15:00 --dur 30 --topico Git`
- **Then** a sessão é aceita e gravada, porque encostar não é sobrepor.

**CA4 — Duração fora da faixa**
- **Given** qualquer estado do arquivo de sessões
- **When** eu executo `estudo add --data 2026-09-03 --inicio 09:00 --dur 4 --topico SDD`
- **Then** nada é gravado e a mensagem diz que a duração precisa estar entre 5 e 480 minutos.

**CA5 — Data no futuro**
- **Given** que hoje é 2026-09-04
- **When** eu executo `estudo add --data 2026-09-05 --inicio 09:00 --dur 60 --topico SDD`
- **Then** nada é gravado e a mensagem diz que não dá para registrar uma sessão futura.

## 4. Plano de tarefas proposto pelo agente (versão bruta)

Plano gerado a partir da especificação acima, antes de qualquer revisão minha:

1. Criar o pacote `src/estudo/` com `__init__.py`.
2. Criar o comando de linha `estudo add` com `argparse`, aceitando os quatro argumentos.
3. Criar a camada de persistência que lê e escreve `data/sessoes.json`.
4. Implementar a validação de data, duração e tópico.
5. Implementar a detecção de conflito de horário.
6. Gerar o id incremental da sessão.
7. Escrever testes para o caminho feliz e para os erros.
8. Adicionar suporte a tags e a um campo de anotação livre na sessão.
9. Atualizar o README com o novo comando.

## 5. Revisão do plano (o que mudei e por quê)

**Removi a tarefa 8 (tags e anotação livre).** Nada disso aparece na user story nem nos
requisitos. O agente inventou escopo por conta própria, e é justamente o tipo de coisa que a
spec existe para barrar.

**Reordenei: as regras vêm antes da CLI.** No plano original a interface de linha de comando
era a tarefa 2, antes de existir qualquer regra. Isso levaria a validação para dentro do
`argparse` e quebraria o RNF3, que pede regras testáveis sem depender da interface. As regras
puras passam a ser as primeiras, e a CLI vira só uma casca fina em cima delas.

**Juntei as tarefas 4, 5 e 6 em uma etapa só de regras**, porque as três mexem no mesmo
módulo e não fazem sentido separadas: um id sem validação não serve para nada.

**Separei os testes em duas tarefas**, uma para as regras e outra para a CLI ponta a ponta.
No plano original havia uma tarefa única de testes no fim, o que na prática vira "escrever
todos os testes depois", e o caso de borda do CA3 é exatamente o que costuma ficar de fora
nessa hora.

**Acrescentei uma tarefa de definição do formato do arquivo JSON.** A F2 vai ler esses
mesmos dados, então o formato precisa ser decidido e escrito de propósito, não sair como
efeito colateral de como o `json.dump` foi chamado.

### Plano revisado

1. Definir e documentar o formato de `data/sessoes.json` (contrato com a F2).
2. Criar `src/estudo/regras.py`: validação de data, duração e tópico, detecção de conflito e
   geração do id, sem tocar em disco.
3. Escrever os testes das regras, incluindo o caso de borda das sessões encostadas.
4. Criar `src/estudo/armazenamento.py`: leitura e escrita do JSON, com gravação atômica para
   garantir o RF10.
5. Criar `src/estudo/cli.py` com `argparse`, mapeando cada erro de regra para uma mensagem e
   um código de saída.
6. Escrever os testes da CLI ponta a ponta, usando um arquivo temporário.
7. Atualizar README e CLAUDE.md com o novo comando.
