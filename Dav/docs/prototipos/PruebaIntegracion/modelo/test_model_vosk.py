#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.
import pytest
from unittest.mock import patch, MagicMock
from VoskModel import VoskModel

# Using the exact folder name you have in your directory
MODEL_PATH = "vosk-model-small-es-0.42"

@patch('VoskModel.vosk.Model')
def test_initialization(mock_vosk_model):
    """Test that the class is instantiated correctly and saves its variables"""
    model = VoskModel(model_path=MODEL_PATH, debug=True)
    
    # Verify that Vosk receives the exact path of your folder
    mock_vosk_model.assert_called_once_with(MODEL_PATH)
    assert model._samplerate == 16000
    assert model._debug is True

@patch('VoskModel.sd.RawInputStream')
@patch('VoskModel.vosk.KaldiRecognizer')
@patch('VoskModel.vosk.Model')
def test_listen_for_one_word(mock_model, mock_recognizer, mock_stream):
    """Test that the method processes text if the Vosk recognizer detects it"""
    
    mock_rec_instance = MagicMock()
    mock_rec_instance.AcceptWaveform.return_value = True
    mock_rec_instance.Result.return_value = '{"text": "hello world"}'
    mock_recognizer.return_value = mock_rec_instance

    model = VoskModel(model_path=MODEL_PATH)
    
    mock_callback = MagicMock()
    model.set_text_callback(mock_callback)

    model._q.put(b"fake_audio_bytes")

    result = model.listen_for_one_word()

    assert result == "hello world"
    mock_callback.assert_called_once_with("hello world")


@patch('VoskModel.sd.RawInputStream')
@patch('VoskModel.vosk.KaldiRecognizer')
@patch('VoskModel.vosk.Model')
def test_continuous_listening(mock_model, mock_recognizer, mock_stream):
    """Test that continuous listening stops when the wake phrase is heard"""
    
    mock_rec_instance = MagicMock()
    mock_rec_instance.AcceptWaveform.return_value = True
    mock_rec_instance.Result.return_value = '{"text": "please close the program"}'
    mock_recognizer.return_value = mock_rec_instance

    model = VoskModel(model_path=MODEL_PATH)
    
    model._q.put(b"fake_audio_bytes")

    model.listen_continuously(wake_phrase="close")
    
    # If execution reaches here and doesn't hang, the break worked.
    assert True