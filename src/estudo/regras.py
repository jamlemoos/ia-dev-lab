"""Regras de negócio do registro de sessões de estudo.

Funções puras: recebem o envelope de dados já carregado e devolvem o resultado.
Nada aqui toca em disco, para que as regras possam ser testadas sozinhas.
"""

from __future__ import annotations

from datetime import date, datetime

DURACAO_MINIMA = 5
DURACAO_MAXIMA = 480
MINUTOS_NO_DIA = 24 * 60

VERSAO_DO_FORMATO = 1


def envelope_vazio() -> dict:
    """Envelope inicial. É uma função, e não uma constante, porque um dicionário de módulo
    com uma lista dentro seria compartilhado por todo mundo que o copiasse de forma rasa."""
    return {"versao": VERSAO_DO_FORMATO, "proximo_id": 1, "sessoes": []}


class ErroDeRegra(Exception):
    """Entrada recusada por uma regra de negócio. A mensagem já vai pronta para o usuário."""


def _data(texto: str) -> date:
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        raise ErroDeRegra(f"data inválida: {texto!r} (use AAAA-MM-DD)") from None


def _minutos(texto: str) -> int:
    try:
        hora = datetime.strptime(texto, "%H:%M")
    except ValueError:
        raise ErroDeRegra(f"hora inválida: {texto!r} (use HH:MM)") from None
    return hora.hour * 60 + hora.minute


def _formatar(minutos: int) -> str:
    return f"{minutos // 60:02d}:{minutos % 60:02d}"


def criar_sessao(
    envelope: dict,
    data: str,
    inicio: str,
    duracao_min: int,
    topico: str,
    hoje: date | None = None,
) -> dict:
    """Valida os dados e devolve a sessão pronta, com id, ou levanta ErroDeRegra.

    Não altera o envelope recebido: quem grava é a camada de armazenamento.
    """
    hoje = hoje or date.today()

    topico = topico.strip()
    if not topico:
        raise ErroDeRegra("o tópico é obrigatório")

    dia = _data(data)
    if dia > hoje:
        raise ErroDeRegra(f"não dá para registrar uma sessão futura ({data})")

    if not DURACAO_MINIMA <= duracao_min <= DURACAO_MAXIMA:
        raise ErroDeRegra(
            f"a duração precisa estar entre {DURACAO_MINIMA} e {DURACAO_MAXIMA} minutos "
            f"(recebi {duracao_min})"
        )

    comeco = _minutos(inicio)
    fim = comeco + duracao_min
    if fim > MINUTOS_NO_DIA:
        raise ErroDeRegra(
            f"a sessão precisa terminar no mesmo dia (começa {inicio} e dura {duracao_min} min)"
        )

    for outra in envelope["sessoes"]:
        if outra["data"] != data:
            continue
        outro_comeco = _minutos(outra["inicio"])
        outro_fim = outro_comeco + outra["duracao_min"]
        # Intervalo semiaberto: sessões que só se encostam não são conflito.
        if comeco < outro_fim and outro_comeco < fim:
            raise ErroDeRegra(
                f"conflito com a sessão {outra['id']} "
                f"({outra['inicio']}-{_formatar(outro_fim)})"
            )

    return {
        "id": envelope["proximo_id"],
        "data": data,
        "inicio": inicio,
        "duracao_min": duracao_min,
        "topico": topico,
    }
