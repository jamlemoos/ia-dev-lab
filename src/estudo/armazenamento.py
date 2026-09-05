"""Leitura e escrita de data/sessoes.json. Só I/O, nenhuma regra de negócio."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .regras import VERSAO_DO_FORMATO, ErroDeRegra, envelope_vazio

VERSAO = VERSAO_DO_FORMATO
CAMINHO_PADRAO = Path("data/sessoes.json")


def carregar(caminho: Path = CAMINHO_PADRAO) -> dict:
    """Devolve o envelope guardado, ou um envelope vazio se o arquivo ainda não existe."""
    if not caminho.exists():
        return envelope_vazio()

    try:
        envelope = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        raise ErroDeRegra(f"{caminho} está corrompido e não foi lido ({erro.msg})") from None

    if not isinstance(envelope, dict):
        raise ErroDeRegra(f"{caminho} não tem o formato esperado (deveria ser um objeto JSON)")
    if envelope.get("versao") != VERSAO:
        raise ErroDeRegra(
            f"{caminho} está na versão {envelope.get('versao')!r}, "
            f"e esta versão do programa só lê a {VERSAO}"
        )
    if not isinstance(envelope.get("proximo_id"), int) or not isinstance(
        envelope.get("sessoes"), list
    ):
        raise ErroDeRegra(
            f"{caminho} está incompleto: faltam 'proximo_id' e/ou 'sessoes' "
            f"(veja docs/formato-sessoes.md)"
        )
    return envelope


def gravar(envelope: dict, caminho: Path = CAMINHO_PADRAO) -> None:
    """Grava o envelope de forma atômica: arquivo temporário vizinho e os.replace."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=caminho.parent, delete=False, suffix=".tmp"
    ) as tmp:
        json.dump(envelope, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
        temporario = Path(tmp.name)
    os.replace(temporario, caminho)


def acrescentar(envelope: dict, sessao: dict, caminho: Path = CAMINHO_PADRAO) -> None:
    """Adiciona a sessão já validada ao envelope e persiste."""
    envelope["sessoes"].append(sessao)
    envelope["proximo_id"] = sessao["id"] + 1
    gravar(envelope, caminho)
