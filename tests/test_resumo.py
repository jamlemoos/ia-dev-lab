from datetime import date

import pytest

from src.estudo.regras import ErroDeRegra
from src.estudo.resumo import (
    agregar,
    formatar_duracao,
    formatar_json,
    formatar_texto,
    periodo,
    periodo_do_mes,
    periodo_da_semana,
)

SEXTA = date(2026, 9, 4)


def sessao(data, topico, duracao):
    return {"id": 1, "data": data, "inicio": "14:00", "duracao_min": duracao, "topico": topico}


# --- período ---------------------------------------------------------------


def test_semana_vai_de_segunda_a_domingo():
    assert periodo_da_semana(SEXTA) == ("2026-08-31", "2026-09-06")


def test_semana_de_uma_segunda_comeca_nela_mesma():
    assert periodo_da_semana(date(2026, 8, 31))[0] == "2026-08-31"


def test_semana_de_um_domingo_termina_nele_mesmo():
    assert periodo_da_semana(date(2026, 9, 6)) == ("2026-08-31", "2026-09-06")


def test_semana_que_vira_o_mes():
    assert periodo_da_semana(date(2026, 4, 1)) == ("2026-03-30", "2026-04-05")


def test_semana_que_vira_o_ano():
    assert periodo_da_semana(date(2027, 1, 1)) == ("2026-12-28", "2027-01-03")


def test_mes_vai_do_dia_1_ao_ultimo():
    assert periodo_do_mes(SEXTA) == ("2026-09-01", "2026-09-30")


def test_mes_de_fevereiro_bissexto():
    assert periodo_do_mes(date(2028, 2, 10)) == ("2028-02-01", "2028-02-29")


def test_periodo_invalido():
    with pytest.raises(ErroDeRegra, match="período inválido"):
        periodo("trimestre", SEXTA)


# --- agregação -------------------------------------------------------------


def test_total_e_percentuais():
    r = agregar([sessao("2026-09-03", "SDD", 180), sessao("2026-09-04", "Git", 90)],
                periodo_da_semana(SEXTA))
    assert r["total_min"] == 270
    assert r["topicos"] == [
        {"topico": "SDD", "minutos": 180, "percentual": 67},
        {"topico": "Git", "minutos": 90, "percentual": 33},
    ]


def test_sessoes_do_mesmo_topico_sao_somadas():
    r = agregar([sessao("2026-09-01", "SDD", 60), sessao("2026-09-02", "SDD", 30)],
                periodo_da_semana(SEXTA))
    assert r["topicos"][0]["minutos"] == 90


def test_empate_resolvido_em_ordem_alfabetica():
    r = agregar([sessao("2026-09-01", "Testes", 60), sessao("2026-09-02", "Git", 60)],
                periodo_da_semana(SEXTA))
    assert [t["topico"] for t in r["topicos"]] == ["Git", "Testes"]


def test_sessoes_fora_do_periodo_sao_ignoradas():
    r = agregar([sessao("2026-08-30", "SDD", 60), sessao("2026-09-03", "Git", 30)],
                periodo_da_semana(SEXTA))
    assert r["total_min"] == 30


def test_limites_do_periodo_sao_inclusivos():
    r = agregar([sessao("2026-08-31", "SDD", 60), sessao("2026-09-06", "Git", 60)],
                periodo_da_semana(SEXTA))
    assert r["total_min"] == 120


def test_periodo_vazio():
    r = agregar([], periodo_da_semana(SEXTA))
    assert r == {"inicio": "2026-08-31", "fim": "2026-09-06", "total_min": 0, "topicos": []}


def test_percentuais_podem_nao_somar_100():
    """Três terços de 100% viram 33+33+33=99, e isso é aceito pela spec."""
    sessoes = [sessao("2026-09-01", t, 60) for t in ("A", "B", "C")]
    r = agregar(sessoes, periodo_da_semana(SEXTA))
    assert sum(t["percentual"] for t in r["topicos"]) == 99


# --- filtro por tópico -----------------------------------------------------


def test_filtro_ignora_maiusculas_e_minusculas():
    r = agregar([sessao("2026-09-03", "SDD", 60), sessao("2026-09-03", "Git", 30)],
                periodo_da_semana(SEXTA), topico="sdd")
    assert r["total_min"] == 60
    assert r["topicos"][0]["percentual"] == 100


def test_filtro_sem_resultado():
    r = agregar([sessao("2026-09-03", "Git", 30)], periodo_da_semana(SEXTA), topico="SDD")
    assert r["total_min"] == 0 and r["topicos"] == []


# --- formatação ------------------------------------------------------------


@pytest.mark.parametrize("minutos,esperado", [(0, "0h00"), (5, "0h05"), (90, "1h30"), (270, "4h30")])
def test_formatar_duracao(minutos, esperado):
    assert formatar_duracao(minutos) == esperado


def test_texto_lista_topicos_do_maior_para_o_menor():
    r = agregar([sessao("2026-09-03", "SDD", 180), sessao("2026-09-04", "Git", 90)],
                periodo_da_semana(SEXTA))
    linhas = formatar_texto(r).splitlines()
    assert linhas[0] == "Período 2026-08-31..2026-09-06   total: 4h30"
    assert linhas[1].strip().startswith("SDD  3h00  (67%)")
    assert linhas[2].strip().startswith("Git  1h30  (33%)")


def test_texto_de_periodo_vazio_avisa():
    texto = formatar_texto(agregar([], periodo_da_semana(SEXTA)))
    assert "Nenhuma sessão" in texto


def test_texto_de_filtro_vazio_cita_o_topico():
    texto = formatar_texto(agregar([], periodo_da_semana(SEXTA), topico="SDD"), topico="SDD")
    assert "'SDD'" in texto


def test_json_traz_os_mesmos_numeros_do_texto():
    import json

    r = agregar([sessao("2026-09-03", "SDD", 180), sessao("2026-09-04", "Git", 90)],
                periodo_da_semana(SEXTA))
    assert json.loads(formatar_json(r)) == r


def test_json_de_periodo_vazio_continua_valido():
    import json

    dados = json.loads(formatar_json(agregar([], periodo_da_semana(SEXTA))))
    assert dados["total_min"] == 0 and dados["topicos"] == []
