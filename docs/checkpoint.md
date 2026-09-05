# Checkpoint humano obrigatório (Etapa 4)

## O checkpoint definido

**Nenhum Pull Request entra na `main` sem revisão humana do diff completo.** O agente pode
propor a spec, escrever o código, rodar os testes e abrir o PR, mas o merge é sempre
manual. A regra está escrita no `CLAUDE.md`, na seção "Não fazer", para valer também nas
próximas sessões.

O que a pessoa precisa conferir antes de aprovar:

1. O diff inteiro, arquivo por arquivo, e não só o resumo do agente.
2. Se apareceu algum arquivo, dependência ou funcionalidade que a spec não pedia.
3. Se a suíte de testes está verde e se os testes realmente cobrem os critérios de aceite.
4. Se o comportamento bate com o que está na spec quando executado à mão, não só nos testes.

Escolhi o merge como ponto de parada porque é o último momento em que o custo de dizer "não"
ainda é baixo. Depois que entra na `main`, o código vira base para a F2 e para qualquer coisa
que venha depois, e desfazer sai muito mais caro do que revisar.

## A simulação

Parei antes do merge e revisei o que entraria. Além dos testes verdes, executei o comando à
mão em alguns cenários que os testes não cobriam. Um deles quebrou:

```
$ echo '{"versao": 1}' > /tmp/meio-editado.json
$ python -m src.estudo.cli --arquivo /tmp/meio-editado.json add --data 2026-09-03 \
    --inicio 14:00 --dur 60 --topico SDD
Traceback (most recent call last):
  ...
KeyError: 'sessoes'
```

Um arquivo de dados editado à mão, com a versão certa mas sem a chave `sessoes`, derrubava o
comando com stack trace. A leitura só conferia o campo `versao` e confiava no resto do
formato. Isso contraria a tarefa 5.2 do plano, que diz explicitamente "sem stack trace", e o
requisito RF11, que pede mensagem própria para cada recusa. Os testes não pegaram porque eu
tinha testado o arquivo corrompido (JSON inválido) e o de versão desconhecida, mas não o
arquivo com JSON válido e formato incompleto.

## Decisão tomada

**Editar antes de aprovar.** Não voltei à especificação, porque a spec já cobria o caso: o
requisito de mensagem própria por recusa existia e a implementação é que estava incompleta.
Não era caso de rejeitar tudo, porque o problema era pontual e não afetava o desenho.

A edição: a leitura passa a conferir também o tipo do envelope e a presença de `proximo_id` e
`sessoes`, com mensagem que aponta para `docs/formato-sessoes.md`. Foi acrescentado o teste
`test_arquivo_com_envelope_incompleto_e_recusado`, que garante a mensagem e a ausência de
stack trace. Depois disso, 33 testes passando, e aí sim o PR foi liberado para merge.

## O papel humano assumido

Revisora de código com poder de veto, não copiloto. Concretamente: eu decidi as regras de
negócio antes da spec existir (faixa de duração, o que conta como sobreposição, o que fazer
com sessão que atravessa a meia-noite), revisei o plano de tarefas que o agente propôs e
cortei escopo que ele tinha inventado, e no fim testei à mão em vez de aceitar "os testes
passaram" como prova.

Esse papel faz sentido justamente porque o agente é rápido demais para o meu ritmo de leitura.
Ele produziu spec, código e testes em poucos minutos, todos plausíveis e todos verdes. As duas
falhas reais desta atividade, a lista compartilhada entre chamadas e o stack trace no arquivo
incompleto, passaram pela suíte inteira sem serem notadas. Nenhuma das duas seria pega
aumentando o número de testes gerados pelo próprio agente, porque ele testaria os mesmos
cenários em que já pensou. O humano aqui não está conferindo sintaxe: está trazendo os
cenários que ninguém pediu.
