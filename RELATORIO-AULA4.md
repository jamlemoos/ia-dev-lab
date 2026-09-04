# Relatório — Prática Assíncrona da Aula 4: De Spec a Código

**Projeto:** [jamlemoos/ia-dev-lab](https://github.com/jamlemoos/ia-dev-lab) — PR aberto:
[#2](https://github.com/jamlemoos/ia-dev-lab/pull/2) · 17 commits · 70 testes passando

## As funcionalidades escolhidas e por que eram um bom caso para SDD

Continuei o repositório da Aula 2, que só tinha uma função de saudação sem estado, e
acrescentei duas funcionalidades: `estudo add`, que registra uma sessão de estudo (data, hora
de início, duração e tópico) em um arquivo JSON, e `estudo resumo`, que agrega essas sessões
por semana ou mês, com filtro por tópico e saída em texto ou JSON.

Elas eram um bom caso para SDD porque quase tudo que importa nelas é decisão, não código. A
faixa válida de duração, o que conta como sobreposição de horário, se a semana começa na
segunda, o que fazer quando os percentuais arredondados não somam 100%: nada disso estava no
projeto e nada disso o agente tinha como adivinhar. Além disso, o resumo lê exatamente o que o
registro grava, então o formato do arquivo precisava ser decidido de propósito e não sair como
efeito colateral de uma chamada de `json.dump`. Foram os casos de borda que provaram o ponto:
sessão que começa no minuto exato em que a anterior termina, período totalmente vazio, empate
de tempo entre dois tópicos, virada de ano na contagem da semana.

## As abordagens de especificação e como se comportaram

Usei duas ferramentas sobre o mesmo domínio: **OpenSpec 1.12** para o registro e **SpecKit**
para o resumo. O OpenSpec é dirigido pelo CLI: `openspec status` diz qual artefato está
pronto para ser escrito e qual está bloqueado, `openspec instructions` entrega o template e as
regras de cada um, e `openspec validate --strict` reprova uma spec estruturalmente incompleta.
Ele produziu `proposal.md`, um delta de spec com requisitos SHALL e cenários, `design.md` e
`tasks.md`. O forte dele é o modelo de delta: a spec da mudança é o que muda, e ao arquivar
vira spec permanente do sistema.

O SpecKit é mais opinativo sobre o conteúdo. O template obriga a priorizar as user stories,
declarar como cada uma é testável sozinha, listar casos de borda numa seção própria e definir
critérios de sucesso mensuráveis. E tem a `constitution.md`, princípios permanentes do projeto
que o plano precisa checar um a um. Foi o artefato que mais mudou decisão de código: a
separação entre regras puras e interface, que na F1 eu tinha decidido caso a caso no
`design.md`, na F2 veio imposta pelo princípio II e verificada no Constitution Check.

A diferença apareceu no resultado. A F1 saiu com 33 testes e dois defeitos escaparam. A F2
saiu com 36 testes já na primeira execução, cobrindo virada de mês, virada de ano, fevereiro
bissexto e empate alfabético. Não foi o agente que melhorou: foi a seção obrigatória de casos
de borda no meio do template. Resumindo, o OpenSpec valida a forma da spec, o SpecKit força a
qualidade do conteúdo. A comparação completa está em `docs/comparacao-ferramentas.md`.

## Dificuldades reais enfrentadas

**A técnica: as ferramentas não batem com a própria documentação.** O comando
`openspec change new`, citado no enunciado, não existe mais na versão 1.12; virou
`openspec new change`, e a criação dos artefatos passou a ser feita pelo agente por skills.
No SpecKit, o `--ai claude` documentado virou `--integration claude`, e o
`setup-tasks.sh` terminou com código de erro 2 sem criar o `tasks.md`, apenas devolvendo o
template dentro de um JSON, então escrevi o arquivo à mão. Nenhuma das duas falhas impediu o
trabalho, mas as duas custaram tempo e mostraram que ferramenta de SDD nova ainda é terreno
instável.

**A conceitual, e a mais importante: teste verde não prova que o código está certo.** Os dois
defeitos reais desta atividade passaram pela suíte inteira. O primeiro foi um envelope inicial
declarado como constante de módulo, com uma lista dentro, que qualquer cópia rasa
compartilhava. Todos os testes passavam porque cada um roda uma chamada só. O segundo foi um
arquivo de dados editado à mão, com a versão certa mas sem a chave `sessoes`, que derrubava o
comando com stack trace. Achei o primeiro lendo o diff linha a linha e o segundo no checkpoint
humano, executando o comando à mão em cenários que ninguém tinha pedido. O que aprendi é que
pedir mais testes ao agente não teria resolvido: ele escreveria mais testes para os cenários
em que já pensou. A contribuição humana não foi revisar sintaxe nem contar cobertura, foi
trazer o cenário que não estava na spec. Por isso o checkpoint que defini para o projeto é a
revisão do diff completo antes do merge, e por isso este PR está aberto sem merge.
