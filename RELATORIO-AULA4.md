# Relatório — Prática Assíncrona da Aula 4: De Spec a Código

**Projeto:** [jamlemoos/ia-dev-lab](https://github.com/jamlemoos/ia-dev-lab) · PR aberto:
[#2](https://github.com/jamlemoos/ia-dev-lab/pull/2) · 18 commits · 70 testes passando

## As funcionalidades e por que eram um bom caso para SDD

Continuei o repositório da Aula 2, que só tinha uma saudação sem estado, e acrescentei
`estudo add`, que registra uma sessão de estudo (data, início, duração, tópico) em um arquivo
JSON, e `estudo resumo`, que agrega essas sessões por semana ou mês, com filtro por tópico e
saída em texto ou JSON.

Quase tudo que importa nelas é decisão, não código. A faixa válida de duração, o que conta
como sobreposição de horário, se a semana começa na segunda, o que fazer quando os percentuais
arredondados não somam 100%: nada disso estava no projeto e nada disso o agente tinha como
adivinhar. E como o resumo lê exatamente o que o registro grava, o formato do arquivo precisava
ser decidido de propósito, não sair como efeito colateral de uma chamada de `json.dump`. Os
casos de borda provaram o ponto: sessão que começa no minuto em que a anterior termina, período
vazio, empate de tempo entre tópicos, virada de ano na contagem da semana.

## As abordagens de especificação e como se comportaram

Usei duas ferramentas sobre o mesmo domínio: **OpenSpec 1.12** no registro e **SpecKit** no
resumo. O OpenSpec é dirigido pelo CLI, que diz qual artefato está pronto e qual está
bloqueado, entrega o template de cada um e reprova spec estruturalmente incompleta em
`validate --strict`. O forte dele é o modelo de delta: a spec da mudança é o que muda, e ao
arquivar vira spec permanente do sistema.

O SpecKit é opinativo sobre o conteúdo. O template obriga a priorizar user stories, dizer como
cada uma é testável sozinha, listar casos de borda em seção própria e definir critérios de
sucesso mensuráveis. E tem a `constitution.md`, princípios permanentes que o plano precisa
checar um a um. Foi o artefato que mais mudou decisão de código: a separação entre regras puras
e interface, que na primeira funcionalidade eu decidi caso a caso no `design.md`, na segunda
veio imposta pelo princípio e verificada no Constitution Check.

A diferença apareceu no resultado. A primeira saiu com 33 testes e dois defeitos escaparam; a
segunda saiu com 36 já de primeira, cobrindo virada de ano e fevereiro bissexto. Não foi o
agente que melhorou, foi a seção obrigatória de casos de borda no template. O OpenSpec valida a
forma da spec; o SpecKit força a qualidade do conteúdo. Comparação completa em
`docs/comparacao-ferramentas.md`.

## Dificuldades enfrentadas

**Técnica: as ferramentas não batem com a própria documentação.** O `openspec change new` do
enunciado não existe mais na versão 1.12, e no SpecKit o `--ai` virou `--integration` e o
`setup-tasks.sh` terminou com erro sem criar o `tasks.md`, que escrevi à mão. Nada disso
impediu o trabalho, mas mostrou que ferramenta de SDD ainda é terreno instável.

**Conceitual, e a que mais importou: teste verde não prova que o código está certo.** Os dois
defeitos reais da atividade passaram pela suíte inteira. Um foi um envelope inicial declarado
como constante de módulo, com uma lista dentro, que qualquer cópia rasa compartilhava; todos os
testes passavam porque cada um roda uma chamada só. O outro foi um arquivo de dados editado à
mão que derrubava o comando com stack trace. Achei o primeiro lendo o diff e o segundo no
checkpoint, executando o comando em cenários que ninguém tinha pedido. Pedir mais testes ao
agente não resolveria: ele escreveria mais testes para os cenários em que já pensou. A
contribuição humana não foi revisar sintaxe, foi trazer o cenário que não estava na spec. Por
isso o checkpoint do projeto é a revisão do diff completo antes do merge, e por isso o PR está
aberto sem merge.
