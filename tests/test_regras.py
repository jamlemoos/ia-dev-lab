from datetime import date

import pytest

from src.estudo.regras import ENVELOPE_VAZIO, ErroDeRegra, criar_sessao

HOJE = date(2026, 9, 4)


def envelope(*sessoes):
    return {"versao": 1, "proximo_id": len(sessoes) + 1, "sessoes": list(sessoes)}


def sessao(id_, data="2026-09-03", inicio="14:00", duracao=90, topico="SDD"):
    return {"id": id_, "data": data, "inicio": inicio, "duracao_min": duracao, "topico": topico}


def test_sessao_valida_recebe_id():
    nova = criar_sessao(dict(ENVELOPE_VAZIO), "2026-09-03", "14:00", 90, "SDD", hoje=HOJE)
    assert nova == sessao(1)


def test_topico_ganha_id_seguinte():
    nova = criar_sessao(envelope(sessao(1)), "2026-09-02", "09:00", 60, "Git", hoje=HOJE)
    assert nova["id"] == 2


def test_topico_em_branco():
    with pytest.raises(ErroDeRegra, match="tópico"):
        criar_sessao(envelope(), "2026-09-03", "14:00", 60, "   ", hoje=HOJE)


def test_topico_tem_espacos_removidos():
    nova = criar_sessao(envelope(), "2026-09-03", "14:00", 60, "  SDD  ", hoje=HOJE)
    assert nova["topico"] == "SDD"


def test_data_no_futuro():
    with pytest.raises(ErroDeRegra, match="futura"):
        criar_sessao(envelope(), "2026-09-05", "09:00", 60, "SDD", hoje=HOJE)


def test_data_de_hoje_e_aceita():
    assert criar_sessao(envelope(), "2026-09-04", "09:00", 60, "SDD", hoje=HOJE)["id"] == 1


def test_duracao_abaixo_do_minimo():
    with pytest.raises(ErroDeRegra, match="entre 5 e 480"):
        criar_sessao(envelope(), "2026-09-03", "09:00", 4, "SDD", hoje=HOJE)


def test_duracao_acima_do_maximo():
    with pytest.raises(ErroDeRegra, match="entre 5 e 480"):
        criar_sessao(envelope(), "2026-09-03", "09:00", 481, "SDD", hoje=HOJE)


@pytest.mark.parametrize("duracao", [5, 480])
def test_duracao_nos_limites_e_aceita(duracao):
    assert criar_sessao(envelope(), "2026-09-03", "00:00", duracao, "SDD", hoje=HOJE)


def test_sessao_que_atravessa_a_meia_noite():
    with pytest.raises(ErroDeRegra, match="mesmo dia"):
        criar_sessao(envelope(), "2026-09-03", "23:00", 90, "SDD", hoje=HOJE)


def test_sessao_que_termina_exatamente_a_meia_noite_e_aceita():
    assert criar_sessao(envelope(), "2026-09-03", "23:00", 60, "SDD", hoje=HOJE)


def test_conflito_por_sobreposicao_parcial():
    existente = sessao(1, inicio="14:00", duracao=90)  # 14:00-15:30
    with pytest.raises(ErroDeRegra, match=r"conflito com a sessão 1 \(14:00-15:30\)"):
        criar_sessao(envelope(existente), "2026-09-03", "14:30", 30, "Git", hoje=HOJE)


def test_sessao_encostada_e_aceita():
    """Caso de borda: encostar não é sobrepor (intervalo semiaberto)."""
    existente = sessao(1, inicio="14:00", duracao=60)  # 14:00-15:00
    nova = criar_sessao(envelope(existente), "2026-09-03", "15:00", 30, "Git", hoje=HOJE)
    assert nova["id"] == 2


def test_sessao_que_termina_quando_a_outra_comeca_e_aceita():
    existente = sessao(1, inicio="15:00", duracao=60)  # 15:00-16:00
    assert criar_sessao(envelope(existente), "2026-09-03", "14:00", 60, "Git", hoje=HOJE)


def test_sessao_que_engloba_outra_e_conflito():
    existente = sessao(1, inicio="14:00", duracao=30)  # 14:00-14:30
    with pytest.raises(ErroDeRegra, match="conflito"):
        criar_sessao(envelope(existente), "2026-09-03", "13:00", 180, "Git", hoje=HOJE)


def test_mesmo_horario_em_dia_diferente_nao_e_conflito():
    existente = sessao(1, data="2026-09-03", inicio="14:00", duracao=60)
    assert criar_sessao(envelope(existente), "2026-09-02", "14:00", 60, "Git", hoje=HOJE)


def test_data_mal_formada():
    with pytest.raises(ErroDeRegra, match="data inválida"):
        criar_sessao(envelope(), "03/09/2026", "14:00", 60, "SDD", hoje=HOJE)


def test_hora_mal_formada():
    with pytest.raises(ErroDeRegra, match="hora inválida"):
        criar_sessao(envelope(), "2026-09-03", "14h", 60, "SDD", hoje=HOJE)
