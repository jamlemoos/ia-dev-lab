"""Interface de linha de comando do registro de sessões de estudo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from datetime import date

from . import armazenamento, resumo as resumo_mod
from .regras import ErroDeRegra, criar_sessao


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="estudo", description="Registro de sessões de estudo")
    parser.add_argument(
        "--arquivo",
        type=Path,
        default=armazenamento.CAMINHO_PADRAO,
        help="caminho do arquivo de dados (padrão: data/sessoes.json)",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    add = sub.add_parser("add", help="registra uma sessão de estudo")
    add.add_argument("--data", required=True, help="dia da sessão, no formato AAAA-MM-DD")
    add.add_argument("--inicio", required=True, help="hora de início, no formato HH:MM")
    add.add_argument("--dur", required=True, type=int, help="duração em minutos (5 a 480)")
    add.add_argument("--topico", required=True, help="assunto estudado")

    resumo = sub.add_parser("resumo", help="resume as sessões de um período")
    resumo.add_argument(
        "--periodo",
        choices=resumo_mod.PERIODOS,
        default="semana",
        help="período considerado (padrão: semana corrente, de segunda a domingo)",
    )
    resumo.add_argument("--topico", help="considera apenas as sessões deste tópico")
    resumo.add_argument(
        "--formato", choices=("texto", "json"), default="texto", help="formato da saída"
    )
    return parser


def _add(args) -> str:
    envelope = armazenamento.carregar(args.arquivo)
    sessao = criar_sessao(envelope, args.data, args.inicio, args.dur, args.topico)
    armazenamento.acrescentar(envelope, sessao, args.arquivo)
    return (f"ok: sessão {sessao['id']} registrada ({sessao['data']} {sessao['inicio']}, "
            f"{sessao['duracao_min']} min, {sessao['topico']})")


def _resumo(args, hoje: date | None = None) -> str:
    envelope = armazenamento.carregar(args.arquivo)
    intervalo = resumo_mod.periodo(args.periodo, hoje or date.today())
    dados = resumo_mod.agregar(envelope["sessoes"], intervalo, args.topico)
    if args.formato == "json":
        return resumo_mod.formatar_json(dados)
    return resumo_mod.formatar_texto(dados, args.topico)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        saida = _add(args) if args.comando == "add" else _resumo(args)
    except ErroDeRegra as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    print(saida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
