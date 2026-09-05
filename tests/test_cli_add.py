"""Testes ponta a ponta do comando `estudo add`, cobrindo os critérios de aceite da spec."""

import json

import pytest

from src.estudo.cli import main


@pytest.fixture
def arquivo(tmp_path):
    return tmp_path / "sessoes.json"


def add(arquivo, data="2026-09-03", inicio="14:00", dur="90", topico="SDD"):
    return main(
        ["--arquivo", str(arquivo), "add",
         "--data", data, "--inicio", inicio, "--dur", dur, "--topico", topico]
    )


def sessoes(arquivo):
    return json.loads(arquivo.read_text(encoding="utf-8"))["sessoes"]


def test_ca1_registro_valido(arquivo, capsys):
    assert add(arquivo) == 0
    assert "sessão 1" in capsys.readouterr().out
    assert sessoes(arquivo) == [
        {"id": 1, "data": "2026-09-03", "inicio": "14:00", "duracao_min": 90, "topico": "SDD"}
    ]


def test_ca2_conflito_de_horario(arquivo, capsys):
    add(arquivo, inicio="14:00", dur="90")
    capsys.readouterr()
    assert add(arquivo, inicio="14:30", dur="30", topico="Git") == 1
    erro = capsys.readouterr().err
    assert "sessão 1" in erro and "14:00-15:30" in erro
    assert len(sessoes(arquivo)) == 1


def test_ca3_sessoes_encostadas(arquivo):
    add(arquivo, inicio="14:00", dur="60")
    assert add(arquivo, inicio="15:00", dur="30", topico="Git") == 0
    assert [s["id"] for s in sessoes(arquivo)] == [1, 2]


def test_ca4_duracao_fora_da_faixa(arquivo, capsys):
    assert add(arquivo, inicio="09:00", dur="4") == 1
    assert "entre 5 e 480" in capsys.readouterr().err
    assert not arquivo.exists()


def test_ca5_data_no_futuro(arquivo, capsys):
    assert add(arquivo, data="2099-01-01") == 1
    assert "futura" in capsys.readouterr().err
    assert not arquivo.exists()


def test_arquivo_intacto_apos_recusa(arquivo):
    add(arquivo, inicio="08:00", dur="60")
    add(arquivo, inicio="10:00", dur="60", topico="Git")
    add(arquivo, inicio="12:00", dur="60", topico="Testes")
    antes = arquivo.read_text(encoding="utf-8")

    assert add(arquivo, inicio="10:30", dur="15", topico="Conflito") == 1
    assert arquivo.read_text(encoding="utf-8") == antes


def test_id_nao_e_reaproveitado_apos_remocao_manual(arquivo):
    add(arquivo, inicio="08:00", dur="60")
    add(arquivo, inicio="10:00", dur="60", topico="Git")
    dados = json.loads(arquivo.read_text(encoding="utf-8"))
    dados["sessoes"].pop()  # alguém apagou a sessão 2 na mão
    arquivo.write_text(json.dumps(dados), encoding="utf-8")

    add(arquivo, inicio="12:00", dur="60", topico="Testes")
    assert [s["id"] for s in sessoes(arquivo)] == [1, 3]


def test_arquivo_de_versao_desconhecida_e_recusado(arquivo, capsys):
    arquivo.write_text(json.dumps({"versao": 99, "proximo_id": 1, "sessoes": []}), encoding="utf-8")
    assert add(arquivo) == 1
    assert "versão" in capsys.readouterr().err


def test_arquivo_corrompido_e_recusado(arquivo, capsys):
    arquivo.write_text("{ isso não é json", encoding="utf-8")
    assert add(arquivo) == 1
    assert "corrompido" in capsys.readouterr().err


def test_arquivo_com_envelope_incompleto_e_recusado(arquivo, capsys):
    """Achado no checkpoint humano: sem essa checagem, o comando quebrava com stack trace."""
    arquivo.write_text(json.dumps({"versao": 1}), encoding="utf-8")
    assert add(arquivo) == 1
    erro = capsys.readouterr().err
    assert "incompleto" in erro and "Traceback" not in erro
