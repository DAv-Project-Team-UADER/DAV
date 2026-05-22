from PruebaIntegracion.core.Idioma import Idioma


def test_idioma_es_normaliza_numeros_y_comandos():
    idioma = Idioma(modelo="pequeno", idioma="ES")

    assert idioma.idioma == "ES"
    assert idioma.lista_numeros_hablados[0] == "cero"
    assert idioma.lista_digitos == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert "cancelar" in idioma.lista_comandos
    assert "enviar" in idioma.lista_comandos
    assert "enter" in idioma.lista_comandos
    assert idioma.normalizar_texto("uno dos tres") == "1 2 3"


def test_idioma_en_fallback_basico():
    idioma = Idioma(modelo="small", idioma="EN")

    assert idioma.idioma == "EN"
    assert idioma.lista_numeros_hablados[0] == "zero"
    assert idioma.normalizar_texto("one two three") == "1 2 3"