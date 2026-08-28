from src.saudacao.hello import saudacao


def test_padrao():
    assert saudacao() == "Olá, mundo!"


def test_com_nome():
    assert saudacao("Maria") == "Olá, Maria!"


def test_vazio_usa_padrao():
    assert saudacao("   ") == "Olá, mundo!"
