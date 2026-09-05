"""Agregação das sessões de estudo por período.

Funções puras: recebem as sessões já carregadas e a data de referência, e devolvem
estruturas de dados. Quem lê o arquivo é o armazenamento; quem imprime é a CLI.
"""

from __future__ import annotations

import calendar
import json
from datetime import date, timedelta

from .regras import ErroDeRegra

PERIODOS = ("semana", "mes")


def periodo_da_semana(hoje: date) -> tuple[str, str]:
    """Semana corrente, de segunda a domingo, com os dois limites inclusivos."""
    segunda = hoje - timedelta(days=hoje.weekday())
    return segunda.isoformat(), (segunda + timedelta(days=6)).isoformat()


def periodo_do_mes(hoje: date) -> tuple[str, str]:
    """Mês corrente, do dia 1 ao último dia, com os dois limites inclusivos."""
    ultimo = calendar.monthrange(hoje.year, hoje.month)[1]
    return hoje.replace(day=1).isoformat(), hoje.replace(day=ultimo).isoformat()


def periodo(nome: str, hoje: date) -> tuple[str, str]:
    if nome == "semana":
        return periodo_da_semana(hoje)
    if nome == "mes":
        return periodo_do_mes(hoje)
    raise ErroDeRegra(f"período inválido: {nome!r} (use {' ou '.join(PERIODOS)})")


def agregar(sessoes: list[dict], intervalo: tuple[str, str], topico: str | None = None) -> dict:
    """Soma as sessões do intervalo, por tópico, do maior total para o menor.

    As datas estão gravadas em ISO, que ordena por comparação de texto, então o recorte do
    período dispensa converter tudo para date.
    """
    inicio, fim = intervalo
    filtro = topico.strip().lower() if topico else None

    minutos_por_topico: dict[str, int] = {}
    for sessao in sessoes:
        if not inicio <= sessao["data"] <= fim:
            continue
        if filtro and sessao["topico"].lower() != filtro:
            continue
        nome = sessao["topico"]
        minutos_por_topico[nome] = minutos_por_topico.get(nome, 0) + sessao["duracao_min"]

    total = sum(minutos_por_topico.values())
    topicos = [
        {
            "topico": nome,
            "minutos": minutos,
            # Percentual arredondado de forma independente: a soma pode dar 99% ou 101%.
            "percentual": round(minutos * 100 / total) if total else 0,
        }
        for nome, minutos in sorted(minutos_por_topico.items(), key=lambda par: (-par[1], par[0]))
    ]
    return {"inicio": inicio, "fim": fim, "total_min": total, "topicos": topicos}


def formatar_duracao(minutos: int) -> str:
    return f"{minutos // 60}h{minutos % 60:02d}"


def formatar_texto(resumo: dict, topico: str | None = None) -> str:
    periodo_str = f"{resumo['inicio']}..{resumo['fim']}"
    if not resumo["topicos"]:
        alvo = f" para o tópico {topico!r}" if topico else ""
        return f"Nenhuma sessão registrada em {periodo_str}{alvo}."

    linhas = [f"Período {periodo_str}   total: {formatar_duracao(resumo['total_min'])}"]
    largura = max(len(t["topico"]) for t in resumo["topicos"])
    linhas += [
        f"  {t['topico']:<{largura}}  {formatar_duracao(t['minutos'])}  ({t['percentual']}%)"
        for t in resumo["topicos"]
    ]
    return "\n".join(linhas)


def formatar_json(resumo: dict) -> str:
    return json.dumps(resumo, ensure_ascii=False, indent=2)
