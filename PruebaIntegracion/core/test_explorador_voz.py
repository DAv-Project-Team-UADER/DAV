import pytest
from unittest.mock import MagicMock

# Importamos las clases reales de tu proyecto
from PruebaIntegracion.core.NodoContexto import NodoContexto
from PruebaIntegracion.core.Navegador import Navegador
from PruebaIntegracion.core.ParamSpec import ParamSpec
from PruebaIntegracion.core.ExploradorVoz import ExploradorVoz


def test_parse_number():
    """Prueba que la conversión de texto hablado a números funcione correctamente."""
    nav = Navegador(NodoContexto("raiz"))
    # Mockeamos el modelo de voz porque no lo usaremos aquí
    exp = ExploradorVoz(voice_model=MagicMock(), navegador=nav)
    
    assert exp._parse_number("uno punto cinco") == 1.5
    assert exp._parse_number("dos coma cinco") == 2.5
    assert exp._parse_number("diez") == 10.0
    assert exp._parse_number("cero") == 0.0
    assert exp._parse_number("uno dos tres") == 123.0
    # Textos inválidos deberían devolver None
    assert exp._parse_number("palabra_rara") is None


def test_vocabulario_y_traducciones():
    """Prueba que el explorador recolecte vocabulario del nodo actual y sus padres."""
    raiz = NodoContexto("raiz")
    hijo = NodoContexto("hijo")
    raiz.agregar_subcontexto("hijo", hijo)
    
    # Agregamos traducciones en distintos niveles
    raiz.agregar_traduccion("volver", "comando_volver")
    hijo.agregar_traduccion("dibujar", "comando_dibujar")
    
    nav = Navegador(raiz)
    nav.establecer_contexto(hijo)  # Nos situamos en el hijo
    
    exp = ExploradorVoz(voice_model=MagicMock(), navegador=nav)
    
    # 1. Prueba de traducción ascendente
    assert exp._obtener_nombre_real_ascendente("dibujar") == "comando_dibujar" # Encontrado en hijo
    assert exp._obtener_nombre_real_ascendente("volver") == "comando_volver"   # Encontrado en raíz
    assert exp._obtener_nombre_real_ascendente("desconocido") == "desconocido" # No existe
    
    # 2. Prueba de vocabulario activo
    vocab = exp._vocabulario_navegacion()
    assert "volver" in vocab
    assert "dibujar" in vocab
    assert "hijo" in vocab       # La clave del subcontexto en la raíz
    assert "cancelar" in vocab   # Palabra por defecto añadida por ExploradorVoz


def test_procesar_parametros_exitoso():
    """Prueba la recolección de parámetros por voz y su ejecución."""
    raiz = NodoContexto("raiz")
    nav = Navegador(raiz)
    
    # Simulamos el objeto Command para que devuelva lo que diría el usuario
    mock_command = MagicMock()
    # Hacemos que cuando el sistema pida el parámetro, escuche "cinco"
    mock_command.exclusive_listen.return_value = "cinco"
    
    exp = ExploradorVoz(voice_model=MagicMock(), navegador=nav, command=mock_command)
    
    # Simulamos una función (EnvoltorioFuncion) que requiere 1 parámetro (radio)
    mock_envoltorio = MagicMock()
    mock_envoltorio.nombre = "dibujar_circulo"
    mock_envoltorio.param_specs = (ParamSpec(nombre="radio", tipo=int),)
    
    # Mockeamos el método llamar del navegador para que no intente ejecutar nada real
    nav.llamar = MagicMock(return_value="Circulo dibujado con exito")
    
    # Preparamos el explorador en modo parámetros
    exp.iniciar_parametros(mock_envoltorio)
    
    # Ejecutamos el procesamiento
    resultado = exp.procesar_parametros()
    
    # Verificaciones
    assert resultado is True
    # Debería haber convertido "cinco" a un entero (5) y llamado a la función
    nav.llamar.assert_called_once_with("dibujar_circulo", 5, context_keys=["raiz"])
    assert exp.modo_parametros is False # Debería haberse reseteado


def test_bucle_comando_navegacion_y_cancelacion():
    """Prueba el flujo principal: entrar a un subcontexto y luego cancelar."""
    raiz = NodoContexto("raiz")
    hijo = NodoContexto("Geometria")
    raiz.agregar_subcontexto("Geometria", hijo)
    
    nav = Navegador(raiz)
    mock_command = MagicMock()
    
    # Simulamos que el usuario dice primero "Geometria" y luego "cancelar"
    # side_effect permite devolver un valor distinto en cada llamada
    mock_command.exclusive_listen.side_effect = ["Geometria", False]
    
    exp = ExploradorVoz(voice_model=MagicMock(), navegador=nav, command=mock_command)
    
    # Ejecutamos el bucle (se detendrá solo por el "cancelar")
    exp.bucle_comando()
    
    # Verificamos que efectivamente se cambió el contexto al hijo
    assert nav.contexto_actual.nombre == "Geometria"
    # Verificamos que escuchó exactamente 2 veces antes de salir
    assert mock_command.exclusive_listen.call_count == 2