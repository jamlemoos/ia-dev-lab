# ia-dev-lab Constitution

## Core Principles

### I. Spec antes de código
Nenhuma funcionalidade começa pelo editor. Primeiro existe uma especificação com
comportamento observável, requisitos e critérios de aceite; o código vem depois e serve à
spec. Quando o código discorda da spec, um dos dois está errado e isso é resolvido por
escrito, não no commit.

### II. Regras de negócio isoladas da interface
As regras vivem em funções puras, sem tocar em disco, rede ou `argparse`. A interface de
linha de comando é uma casca fina que traduz argumentos e erros. Toda regra precisa ser
testável sem I/O.

### III. Só a biblioteca padrão
O projeto não adiciona dependências de runtime. `pytest` é a única exceção, e só para
desenvolvimento. Uma dependência nova exige justificativa escrita do que ela resolve e do
que seria preciso escrever à mão sem ela.

### IV. Cada caso de borda vira teste
Um caso de borda descoberto durante a especificação ou a revisão entra na suíte como teste
nomeado, e não como comentário. Se um bug passou pelos testes, o conserto inclui o teste que
teria pegado.

### V. Revisão humana antes do merge
Nenhum Pull Request entra na `main` sem revisão humana do diff completo, mesmo com a suíte
verde. O agente propõe, o humano decide.

## Compatibilidade de dados

O formato de `data/sessoes.json` é contrato entre funcionalidades e está descrito em
`docs/formato-sessoes.md`. Qualquer mudança nesse formato exige subir o campo `versao`,
atualizar o documento e tratar a leitura da versão antiga ou recusá-la com mensagem clara.
Um arquivo de formato desconhecido nunca é sobrescrito em silêncio.

## Qualidade

Todo comando termina com código de saída 0 em sucesso e diferente de 0 em erro. Erro de uso
vai para `stderr` com mensagem em português, sem stack trace. A suíte inteira precisa passar
antes de qualquer commit de funcionalidade.

## Governance

Esta constituição vale para as duas abordagens de especificação usadas no projeto (OpenSpec e
SpecKit) e prevalece sobre a preferência de qualquer ferramenta. Emendas são feitas por
commit próprio, explicando o que mudou e por quê. Complexidade extra precisa ser justificada
na seção de decisões do plano.

**Version**: 1.0.0 | **Ratified**: 2026-09-04 | **Last Amended**: 2026-09-04
