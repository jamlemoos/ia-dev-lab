# Comparação entre OpenSpec e SpecKit (Etapa 5)

As duas funcionalidades do mesmo projeto foram especificadas e implementadas com ferramentas
diferentes: o registro de sessões (F1) com **OpenSpec 1.12.0** e o resumo agregado (F2) com
**SpecKit** (`specify`, commit 4a7341a). Mesmo domínio, mesmo agente, mesma pessoa revisando.
Isso deixa a diferença entre as ferramentas visível sem o ruído de comparar projetos
diferentes.

## Artefatos gerados

| | OpenSpec (F1) | SpecKit (F2) |
|---|---|---|
| Onde vive | `openspec/changes/<mudança>/` | `specs/NNN-<funcionalidade>/` + `.specify/` |
| Arquivos | `proposal.md`, `specs/<capability>/spec.md`, `design.md`, `tasks.md` | `spec.md`, `plan.md`, `tasks.md`, e a `constitution.md` do projeto |
| Linhas de spec | 247 | 449 (mais 50 da constitution) |
| Unidade central | a **mudança** (change), que depois é arquivada e vira spec permanente | a **funcionalidade**, numerada e permanente desde o começo |
| Validação automática | `openspec validate --strict` | nenhuma; existe `/speckit-analyze`, que é outro passo de agente |
| Como se dirige o fluxo | CLI (`openspec new change`, `status`, `instructions`) | scripts em `.specify/scripts/bash` mais skills do agente |

## Como cada uma se comportou na prática

**OpenSpec.** O CLI é o dono do processo. `openspec status --change X --json` diz quais
artefatos existem, quais estão prontos para escrever e o que cada um depende, e
`openspec instructions <artefato>` devolve o template e as regras daquele artefato. Isso deixa
pouco espaço para o agente pular etapa: enquanto `specs` não existe, `tasks` aparece como
`blocked`. O formato de cenário é rígido (`#### Scenario:` com exatamente quatro `#`, senão
falha em silêncio) e `validate --strict` reprova coisas como um `## Purpose` curto demais. Foi
o mais rigoroso dos dois com a **estrutura** da spec.

O ponto forte é o modelo de delta: a spec da mudança não é a spec do sistema, é o que muda
(`## ADDED Requirements`). Quando a mudança é arquivada, o delta é incorporado à spec
permanente. Isso responde a uma pergunta que o SpecKit deixa em aberto, que é o que acontece
com a spec depois que a funcionalidade foi entregue.

O ponto fraco apareceu logo no começo: o comando `openspec change new` do enunciado da
atividade **não existe mais** na versão 1.12. Mudou para `openspec new change`, e a criação
dos artefatos passou a ser feita pelo agente através de skills, não pelo CLI.

**SpecKit.** É mais opinativo sobre o **conteúdo**. O template de spec obriga a priorizar as
user stories (P1, P2, P3), a declarar para cada uma um "Independent Test" e a justificar a
prioridade, e ainda exige "Success Criteria" mensuráveis e independentes de tecnologia. Ele
também tem uma seção `[NEEDS CLARIFICATION]` para marcar decisão que falta, e um passo
opcional (`/speckit-clarify`) para resolver isso antes do plano. A `constitution.md` é o
recurso que o OpenSpec não tem: princípios permanentes do projeto que o `plan.md` precisa
checar um a um numa tabela de Constitution Check, o que transformou "regras isoladas da
interface" em algo verificável em vez de intenção.

O ponto fraco: a estrutura vem de scripts em bash mais frágeis. O `setup-tasks.sh` saiu com
código de erro 2, não criou o `tasks.md` e apenas devolveu o template dentro de um JSON, então
o arquivo teve que ser escrito na mão. O `--ai claude` documentado em vários lugares virou
`--integration claude`. E o `create-new-feature.sh` quer criar uma branch por funcionalidade,
o que atrapalha quem já está numa branch de trabalho. Também não há validação: nada impede
uma spec com `[FEATURE NAME]` ainda por preencher.

## Positivos e negativos, em resumo

| | OpenSpec | SpecKit |
|---|---|---|
| Positivo | Validação real e automática; modelo de delta com arquivamento; CLI que impede pular etapa; artefatos enxutos | Templates que forçam priorização, testabilidade independente e critérios mensuráveis; constitution como regra permanente do projeto; marca explicitamente o que falta esclarecer |
| Negativo | Nenhum conceito de princípios permanentes; formato rígido que falha em silêncio; documentação desatualizada em relação ao CLI | Sem validação automática; scripts de scaffolding frágeis; muito mais texto para manter; empurra uma branch por funcionalidade |

## Comparação do código gerado

A F1 (OpenSpec) produziu `regras.py`, `armazenamento.py` e `cli.py`; a F2 (SpecKit) produziu
`resumo.py` e um segundo subcomando em `cli.py`. As duas chegaram na mesma arquitetura, com
regras puras separadas de I/O e da interface, mas por caminhos diferentes.

No caso do OpenSpec, a separação veio do `design.md`, onde ela foi decidida como uma escolha
técnica com alternativa considerada. No caso do SpecKit, veio de cima: o princípio II da
constitution exige regras isoladas da interface, e o Constitution Check do `plan.md` obrigou a
dizer, por escrito, como a funcionalidade atendia a esse princípio antes de escrever qualquer
linha. O resultado é parecido, mas o segundo caminho é mais difícil de esquecer numa próxima
funcionalidade, porque a regra não depende de alguém lembrar de repetir a decisão.

A cobertura de testes ficou notavelmente diferente. A F1 terminou com 33 testes, e dois casos
de borda importantes só apareceram depois, na revisão do diff e no checkpoint humano. A F2
começou com 36 testes já na primeira execução, cobrindo virada de mês, virada de ano,
fevereiro bissexto, empate alfabético e percentual que não soma 100%. A diferença não é do
agente: é que a seção "Edge Cases" do template do SpecKit é obrigatória e fica no meio da
spec, enquanto no OpenSpec os casos de borda entram como cenários se alguém pensar neles.

Quanto ao atendimento aos requisitos, as duas funcionalidades fazem o que a spec diz, e os
critérios de aceite viraram testes com nome reconhecível (`test_ca3_sessoes_encostadas`,
`test_limites_do_periodo_sao_inclusivos`). O que mudou foi a rastreabilidade: no SpecKit dá
para ir de FR-005 até o teste `test_empate_resolvido_em_ordem_alfabetica` porque as tarefas
citam o requisito; no OpenSpec a ligação existe pelo cenário, mas o `tasks.md` não referencia
os requisitos, então a ponte é mental.

## O que eu aprendi

Escrever a mesma coisa duas vezes, com duas ferramentas, mostrou que a parte cara do SDD não é
a ferramenta: é decidir as regras. As perguntas difíceis foram sempre as mesmas, se encostar
conta como sobreposição, se a semana começa na segunda, o que fazer quando o percentual não
fecha 100%. Nenhuma das duas ferramentas responde isso; as duas só garantem que a pergunta
seja feita antes do código, e cada uma faz isso de um jeito. O OpenSpec valida a forma e me
impede de entregar uma spec estruturalmente incompleta. O SpecKit valida a intenção, me
obrigando a priorizar, a dizer como cada história é testável sozinha e a confrontar a
funcionalidade com os princípios do projeto. Se eu tivesse que escolher uma só para continuar,
levaria a constitution do SpecKit para dentro do fluxo do OpenSpec, porque foi o artefato que
mais mudou decisão de código, e ficaria com a validação automática do OpenSpec, porque foi o
que evitou que a spec virasse texto solto.
