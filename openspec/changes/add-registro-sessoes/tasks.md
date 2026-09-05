## 1. Contrato de dados

- [x] 1.1 Documentar em `docs/formato-sessoes.md` o envelope de `data/sessoes.json`
      (`versao`, `proximo_id`, `sessoes`) e os campos de cada sessão, com um exemplo
      completo. Verificação: o exemplo do documento é carregável por `json.loads` sem erro.
- [x] 1.2 Adicionar `data/` ao `.gitignore`. Verificação: `git status` não mostra
      `data/sessoes.json` depois de rodar o comando.

## 2. Regras de negócio

- [x] 2.1 Criar `src/estudo/__init__.py` e `src/estudo/regras.py` com a exceção de domínio
      `ErroDeRegra`. Verificação: `python -c "from src.estudo.regras import ErroDeRegra"`
      roda sem erro.
- [x] 2.2 Implementar a validação de tópico, duração (5 a 480, limites aceitos), data no
      futuro e término no mesmo dia, cada uma com mensagem própria. Verificação: os testes
      da tarefa 3.1 passam.
- [x] 2.3 Implementar a detecção de conflito usando intervalo semiaberto e a atribuição do
      próximo id, sem tocar em disco. Verificação: os testes da tarefa 3.2 passam.

## 3. Testes das regras

- [x] 3.1 Escrever `tests/test_regras.py` cobrindo os cinco motivos de recusa e o caminho
      feliz. Verificação: `python -m pytest tests/test_regras.py -q` passa.
- [x] 3.2 Acrescentar os testes de conflito: sobreposição parcial, sessões encostadas (caso
      de borda), mesmo horário em dias diferentes e duração exatamente nos limites 5 e 480.
      Verificação: `python -m pytest tests/test_regras.py -q` passa.

## 4. Persistência

- [x] 4.1 Implementar `src/estudo/armazenamento.py` com leitura (arquivo ausente devolve
      envelope vazio; arquivo mal formado ou de versão desconhecida levanta erro com
      mensagem) e escrita atômica via arquivo temporário e `os.replace`. Verificação: teste
      que grava em `tmp_path` e relê o mesmo conteúdo.

## 5. Interface de linha de comando

- [x] 5.1 Implementar `src/estudo/cli.py` com `argparse` para o subcomando `add`
      (`--data`, `--inicio`, `--dur`, `--topico`), imprimindo a confirmação com o id em
      `stdout` e saindo com 0. Verificação: `python -m src.estudo.cli add ...` grava e
      imprime o id.
- [x] 5.2 Mapear `ErroDeRegra` para mensagem em `stderr` e código de saída 1, sem stack
      trace. Verificação: `echo $?` devolve 1 depois de um comando recusado.

## 6. Testes ponta a ponta

- [x] 6.1 Escrever `tests/test_cli_add.py` usando um arquivo temporário, cobrindo os cinco
      critérios de aceite da spec, inclusive os códigos de saída e a garantia de que o
      arquivo fica intacto após uma recusa. Verificação:
      `python -m pytest -q` passa com toda a suíte, incluindo os testes antigos da saudação.

## 7. Documentação

- [x] 7.1 Atualizar `README.md` e `CLAUDE.md` com o comando `estudo add`, a faixa de duração
      e o caminho do arquivo de dados. Verificação: os comandos citados no README rodam como
      descrito.
