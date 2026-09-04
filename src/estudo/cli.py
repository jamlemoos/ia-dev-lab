"""Interface de linha de comando do registro de sessões de estudo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import armazenamento
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        envelope = armazenamento.carregar(args.arquivo)
        sessao = criar_sessao(envelope, args.data, args.inicio, args.dur, args.topico)
        armazenamento.acrescentar(envelope, sessao, args.arquivo)
    except ErroDeRegra as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    print(f"ok: sessão {sessao['id']} registrada ({sessao['data']} {sessao['inicio']}, "
          f"{sessao['duracao_min']} min, {sessao['topico']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
