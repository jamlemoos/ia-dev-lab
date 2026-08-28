"""Saudação simples — funcionalidade inicial da Etapa 1."""


def saudacao(nome: str = "mundo") -> str:
    nome = nome.strip() or "mundo"
    return f"Olá, {nome}!"


if __name__ == "__main__":
    print(saudacao())
