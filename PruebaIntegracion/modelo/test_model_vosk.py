import pytest
from unittest.mock import patch, MagicMock
from VoskModel import VoskModel

# Usamos el nombre exacto de la carpeta que tienes en tu directorio
RUTA_MODELO = "vosk-model-small-es-0.42"

@patch('VoskModel.vosk.Model')
def test_inicializacion(mock_vosk_model):
    """Prueba que la clase se instancie correctamente y guarde sus variables"""
    modelo = VoskModel(model_path=RUTA_MODELO, debug=True)
    
    # Verificamos que Vosk reciba la ruta exacta de tu carpeta
    mock_vosk_model.assert_called_once_with(RUTA_MODELO)
    assert modelo._samplerate == 16000
    assert modelo._debug is True

@patch('VoskModel.sd.RawInputStream')
@patch('VoskModel.vosk.KaldiRecognizer')
@patch('VoskModel.vosk.Model')
def test_escuchar_una_palabra(mock_model, mock_recognizer, mock_stream):
    """Prueba que el método procese el texto si el reconocedor de Vosk lo detecta"""
    
    mock_rec_instance = MagicMock()
    mock_rec_instance.AcceptWaveform.return_value = True
    mock_rec_instance.Result.return_value = '{"text": "hola mundo"}'
    mock_recognizer.return_value = mock_rec_instance

    modelo = VoskModel(model_path=RUTA_MODELO)
    
    mock_callback = MagicMock()
    modelo.set_callback_texto(mock_callback)

    modelo._q.put(b"bytes_de_audio_falsos")

    resultado = modelo.escuchar_una_palabra()

    assert resultado == "hola mundo"
    mock_callback.assert_called_once_with("hola mundo")


@patch('VoskModel.sd.RawInputStream')
@patch('VoskModel.vosk.KaldiRecognizer')
@patch('VoskModel.vosk.Model')
def test_escuchar_latente(mock_model, mock_recognizer, mock_stream):
    """Prueba que la escucha continua se detenga al escuchar la frase de despertar"""
    
    mock_rec_instance = MagicMock()
    mock_rec_instance.AcceptWaveform.return_value = True
    mock_rec_instance.Result.return_value = '{"text": "por favor cerrar el programa"}'
    mock_recognizer.return_value = mock_rec_instance

    modelo = VoskModel(model_path=RUTA_MODELO)
    
    modelo._q.put(b"bytes_de_audio_falsos")

    modelo.escuchar_latente(frase_despertar="cerrar")
    
    # Si la ejecución llega hasta aquí y no se queda trabada, el break funcionó.
    assert True