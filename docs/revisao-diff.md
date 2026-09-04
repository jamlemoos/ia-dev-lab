# Revisão dos diffs gerados (Etapa 3, tarefa 12)

## O que eu teria deixado passar

No primeiro diff das regras, o envelope inicial era uma constante de módulo:

```python
ENVELOPE_VAZIO = {"versao": 1, "proximo_id": 1, "sessoes": []}
```

Passa em todos os testes e parece inofensivo. O problema é a lista dentro do dicionário:
qualquer cópia rasa (`dict(ENVELOPE_VAZIO)`) continua apontando para a **mesma** lista, e
quem depois desse `append` está mexendo no estado global do módulo. Eu tinha escrito
exatamente essa cópia rasa em um dos testes, sem perceber.

Reproduzi o problema fora dos testes:

```
$ python -c "..."
ENVELOPE_VAZIO virou: {'versao': 1, 'proximo_id': 1, 'sessoes': [{'id': 1, ...}]}
```

O envelope "vazio" deixou de ser vazio para o resto do processo. Nenhum teste pegava isso
porque cada teste roda uma chamada só; apareceria como sessão fantasma na segunda chamada
dentro do mesmo processo, que é justamente o cenário que a F2 vai criar quando ler e escrever
na mesma execução. Foi um caso em que o código estava verde e mesmo assim errado.

Correção aplicada: a constante virou a função `envelope_vazio()`, que devolve uma estrutura
nova a cada chamada, mais um teste de regressão (`test_envelope_vazio_nao_e_compartilhado`).

## Outras coisas conferidas no diff, e que estavam certas

- **A comparação de conflito.** `comeco < outro_fim and outro_comeco < fim` é o intervalo
  semiaberto que a spec pediu. Testei os dois lados do encosto (a sessão nova depois e antes
  da existente) e o caso em que uma engloba a outra, porque um `<=` trocado por engano passa
  no teste do meio e falha só nas bordas.
- **A gravação atômica.** O arquivo temporário é criado no mesmo diretório do destino, senão
  `os.replace` poderia cruzar sistemas de arquivos e deixar de ser atômico.
- **A ordem das validações.** Todas acontecem antes de qualquer escrita, então uma recusa
  nunca chega a abrir o arquivo. O teste `test_arquivo_intacto_apos_recusa` compara o
  conteúdo byte a byte antes e depois.
