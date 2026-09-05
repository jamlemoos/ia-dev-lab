"""Testes ponta a ponta do comando `estudo resumo`.

As sessões são posicionadas em relação ao dia de hoje, para que a suíte não dependa da data
em que roda.
"""

import json
from datetime import date, timedelta

import pytest

from src.estudo.cli import main

HOJE = date.today()
SEGUNDA = HOJE - timedelta(days=HOJE.weekday())


def envelope(*sessoes):
    return {"versao": 1, "proximo_id": len(sessoes) + 1, "sessoes": list(sessoes)}


def sessao(id_, dia: date, topico, duracao):
    return {"id": id_, "data": dia.isoformat(), "inicio": "14:00",
            "duracao_min": duracao, "topico": topico}


@pytest.fixture
def arquivo(tmp_path):
    caminho = tmp_path / "sessoes.json"
    caminho.write_text(
        json.dumps(envelope(
            sessao(1, SEGUNDA, "SDD", 180),
            sessao(2, SEGUNDA + timedelta(days=1), "Git", 90),
            sessao(3, SEGUNDA - timedelta(days=7), "Antiga", 300),  # semana passada
        )),
        encoding="utf-8",
    )
    return caminho


def resumo(arquivo, *extras):
    return main(["--arquivo", str(arquivo), "resumo", *extras])


def test_resumo_da_semana(arquivo, capsys):
    assert resumo(arquivo) == 0
    saida = capsys.readouterr().out
    assert "total: 4h30" in saida
    assert "SDD" in saida and "Git" in saida
    assert "Antiga" not in saida  # ficou fora do período


def test_resumo_do_mes_inclui_o_que_a_semana_deixou_de_fora(arquivo, capsys):
    assert resumo(arquivo, "--periodo", "mes") == 0
    saida = capsys.readouterr().out
    sessoes_do_mes = [s for s in json.loads(arquivo.read_text())["sessoes"]
                      if s["data"][:7] == HOJE.isoformat()[:7]]
    total = sum(s["duracao_min"] for s in sessoes_do_mes)
    assert f"total: {total // 60}h{total % 60:02d}" in saida


def test_filtro_por_topico_sem_diferenciar_caixa(arquivo, capsys):
    assert resumo(arquivo, "--topico", "sdd") == 0
    saida = capsys.readouterr().out
    assert "total: 3h00" in saida and "(100%)" in saida and "Git" not in saida


def test_filtro_sem_resultado_avisa_e_sai_com_zero(arquivo, capsys):
    assert resumo(arquivo, "--topico", "Tricô") == 0
    assert "Nenhuma sessão" in capsys.readouterr().out


def test_formato_json_e_carregavel(arquivo, capsys):
    assert resumo(arquivo, "--formato", "json") == 0
    dados = json.loads(capsys.readouterr().out)
    assert dados["total_min"] == 270
    assert [t["topico"] for t in dados["topicos"]] == ["SDD", "Git"]


def test_arquivo_ausente_e_periodo_vazio(tmp_path, capsys):
    assert resumo(tmp_path / "nao-existe.json") == 0
    assert "Nenhuma sessão" in capsys.readouterr().out


def test_arquivo_ausente_em_json_continua_valido(tmp_path, capsys):
    assert resumo(tmp_path / "nao-existe.json", "--formato", "json") == 0
    assert json.loads(capsys.readouterr().out)["total_min"] == 0


def test_arquivo_corrompido_e_recusado(tmp_path, capsys):
    caminho = tmp_path / "sessoes.json"
    caminho.write_text("{ não é json", encoding="utf-8")
    assert resumo(caminho) == 1
    erro = capsys.readouterr().err
    assert "corrompido" in erro and "Traceback" not in erro


def test_versao_desconhecida_e_recusada(tmp_path, capsys):
    caminho = tmp_path / "sessoes.json"
    caminho.write_text(json.dumps({"versao": 99, "proximo_id": 1, "sessoes": []}), encoding="utf-8")
    assert resumo(caminho) == 1
    assert "versão" in capsys.readouterr().err


def test_resumo_nao_altera_o_arquivo(arquivo):
    antes = arquivo.read_text(encoding="utf-8")
    resumo(arquivo)
    resumo(arquivo, "--formato", "json")
    assert arquivo.read_text(encoding="utf-8") == antes


def test_periodo_invalido_e_recusado_pelo_argparse(arquivo):
    with pytest.raises(SystemExit) as saida:
        resumo(arquivo, "--periodo", "trimestre")
    assert saida.value.code == 2
