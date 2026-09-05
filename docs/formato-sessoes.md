# Formato de `data/sessoes.json`

Contrato de dados entre o registro de sessões (F1, que escreve) e o resumo (F2, que lê).
Quem mudar este formato precisa subir o campo `versao` e atualizar as duas funcionalidades.

## Envelope

| Campo | Tipo | Descrição |
|---|---|---|
| `versao` | inteiro | Versão do formato. Hoje é `1`. Um arquivo com outra versão é recusado na leitura. |
| `proximo_id` | inteiro | Id que a próxima sessão vai receber. Nunca diminui, mesmo que uma sessão seja removida à mão. |
| `sessoes` | lista | Sessões registradas, na ordem em que foram gravadas. |

## Sessão

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | inteiro | Identificador único e crescente. |
| `data` | texto `AAAA-MM-DD` | Dia da sessão. |
| `inicio` | texto `HH:MM` | Hora de início, 24 horas. |
| `duracao_min` | inteiro | Duração em minutos, entre 5 e 480. |
| `topico` | texto | Assunto estudado, sem espaços nas pontas e nunca vazio. |

O horário de término não é gravado: ele é sempre `inicio + duracao_min`, e a sessão termina
obrigatoriamente no mesmo dia.

## Exemplo

```json
{
  "versao": 1,
  "proximo_id": 3,
  "sessoes": [
    {"id": 1, "data": "2026-09-03", "inicio": "14:00", "duracao_min": 90, "topico": "SDD"},
    {"id": 2, "data": "2026-09-03", "inicio": "15:30", "duracao_min": 45, "topico": "Git"}
  ]
}
```

## Arquivo ausente

Se `data/sessoes.json` não existir, vale o envelope vazio
`{"versao": 1, "proximo_id": 1, "sessoes": []}`. O arquivo só é criado na primeira gravação
bem-sucedida.
