# Comparação de prompts (Etapa 4)

Funcionalidade: função de saudação em Python (`src/saudacao/hello.py`).

## Prompt fraco
> "faz uma função de saudação"

**Resposta típica da IA:**
```python
def saudacao(nome):
    print("Olá " + nome)
```
Sem type hints, usa `print` em vez de `return`, quebra se `nome` for `None`/vazio,
sem testes, nome de arquivo/local indefinido.

## Prompt eficaz
> **Contexto:** No projeto `ia-dev-lab`, no módulo `src/saudacao/`, preciso de uma função de
> saudação em Python 3.
> **Exemplo de padrão:** assinatura `def saudacao(nome: str = "mundo") -> str:` retornando
> `"Olá, <nome>!"`.
> **Restrições:** type hints; nunca retornar string vazia (fallback `"mundo"`); mensagem em
> português; não usar `print` dentro da função (só sob `__main__`).
> **Validação:** incluir `tests/test_hello.py` com pytest cobrindo padrão, nome informado e
> entrada vazia.

**Resposta típica da IA:** exatamente o código de `hello.py` + `test_hello.py` deste repositório.

## Diferenças observadas (3–5 frases)
1. O prompt eficaz produziu código com type hints e valor de retorno, diretamente testável.
2. As restrições eliminaram o bug de entrada vazia/None que o prompt fraco ignorava.
3. A validação pedida gerou testes automatizados junto com a função, sem uma segunda rodada.
4. O contexto de caminho fez a IA colocar o arquivo no lugar certo da estrutura por domínio.

## Modelos usados
- Alta performance: Claude Opus 4.8 — seguiu todas as restrições e gerou testes.
- Menor performance: modelo pequeno (ex.: Haiku) — gerou a função, mas tendeu a omitir o
  fallback de entrada vazia e os testes, exigindo prompt de correção.
