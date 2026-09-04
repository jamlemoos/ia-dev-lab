## Context

O projeto hoje tem um único módulo sem estado (`src/saudacao/hello.py`), organizado por
domínio dentro de `src/`, com testes em `tests/` e a regra do `CLAUDE.md` de não adicionar
dependências externas. Este é o primeiro comando que grava dados em disco, então é aqui que
o formato do arquivo e a fronteira entre regra e interface ficam definidos. A funcionalidade
de resumo (F2) vai ler exatamente esses dados. Motivação em `proposal.md`.

## Goals / Non-Goals

**Goals:**

- Deixar as regras de negócio em funções puras, testáveis sem tocar no disco.
- Fixar um formato de arquivo estável, que a F2 possa consumir sem adivinhação.
- Garantir que uma recusa nunca corrompa nem altere o arquivo de dados.

**Non-Goals:**

- Banco de dados, índice ou qualquer otimização para volume grande de sessões.
- Acesso concorrente de vários processos ao mesmo arquivo.
- Edição e remoção de sessões.

## Decisions

**Um arquivo JSON único em `data/sessoes.json`, com envelope versionado.**
Formato: `{"versao": 1, "proximo_id": 4, "sessoes": [...]}`, e cada sessão como
`{"id": 1, "data": "2026-09-03", "inicio": "14:00", "duracao_min": 90, "topico": "SDD"}`.
Datas e horas como texto em ISO, que ordena corretamente por comparação de string e é legível
por quem abrir o arquivo. O campo `versao` existe para que a F2 possa recusar um arquivo de
formato desconhecido em vez de interpretar errado. Considerei SQLite, que resolveria
concorrência e consultas, mas para um CLI de uso pessoal com dezenas de registros por mês ele
só acrescenta cerimônia; o JSON ainda pode ser inspecionado e corrigido à mão.

**`proximo_id` guardado no arquivo, em vez de `max(id) + 1`.**
Calcular pelo máximo parece mais simples, mas reaproveita o id de uma sessão apagada, e o
requisito diz que nenhum identificador é reaproveitado. Guardar o contador custa um campo.

**Três módulos: `regras.py`, `armazenamento.py` e `cli.py`.**
`regras.py` recebe a lista de sessões já existentes e os dados novos e devolve a sessão
validada ou levanta um erro de domínio, sem saber que existe arquivo. `armazenamento.py` só
lê e escreve. `cli.py` traduz argumentos e erros para texto e código de saída. Isso atende ao
requisito de testar as regras sem tocar no disco. A alternativa de um arquivo só seria mais
curta, mas colaria a validação no `argparse` e tornaria o caso de borda das sessões
encostadas difícil de testar isoladamente.

**Sobreposição com intervalo semiaberto `[inicio, fim)`.**
Dois intervalos conflitam quando `inicio_a < fim_b and inicio_b < fim_a`. Com essa
comparação, sessões que se encostam passam naturalmente, sem caso especial no código. A
comparação é feita em minutos desde a meia-noite, dentro do mesmo dia; como a spec proíbe
sessão que atravessa o dia, não existe intervalo partido.

**Gravação atômica: escrever em arquivo temporário no mesmo diretório e depois `os.replace`.**
Uma escrita interrompida no meio deixaria o JSON truncado e o histórico perdido. `os.replace`
é atômico no mesmo sistema de arquivos. As validações também acontecem todas antes de
qualquer escrita, então uma recusa nem chega a abrir o arquivo para gravação.

**Erros de domínio como uma exceção própria com mensagem pronta.**
Uma exceção `ErroDeRegra` carregando a mensagem em português deixa o `cli.py` fino: ele
captura, imprime em `stderr` e sai com código 1. A alternativa de devolver tuplas de erro
espalharia `if` por todas as camadas.

## Risks / Trade-offs

- Dois processos gravando ao mesmo tempo podem perder um registro, porque não há trava →
  aceito conscientemente: é um CLI de uso pessoal. Se virar problema, a saída é um lock de
  arquivo, sem mudar o formato dos dados.
- Ler o arquivo inteiro na memória a cada comando não escala para dezenas de milhares de
  sessões → aceito: são poucas dezenas por mês, e o `versao` no envelope abre caminho para
  migrar de formato depois.
- Arquivo editado à mão pode ficar inválido → a leitura recusa um arquivo mal formado ou de
  versão desconhecida com mensagem explícita, em vez de gravar por cima.
