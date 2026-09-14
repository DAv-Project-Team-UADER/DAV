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
from unittest.mock import MagicMock

# Import the actual classes from your project
from PruebaIntegracion.core.ContextNode import ContextNode
from PruebaIntegracion.core.Navigator import Navigator
from PruebaIntegracion.core.ParamSpec import ParamSpec
from PruebaIntegracion.core.VoiceExplorer import VoiceExplorer


def test_parse_number():
    """Test that spoken text to number conversion works correctly."""
    nav = Navigator(ContextNode("root"))
    # We mock the voice model because we won't use it here
    exp = VoiceExplorer(voice_model=MagicMock(), navigator=nav)
    
    assert exp._parse_number("uno punto cinco") == 1.5
    assert exp._parse_number("dos coma cinco") == 2.5
    assert exp._parse_number("diez") == 10.0
    assert exp._parse_number("cero") == 0.0
    assert exp._parse_number("uno dos tres") == 123.0
    # Invalid texts should return None
    assert exp._parse_number("palabra_rara") is None


def test_vocabulary_and_translations():
    """Test that the explorer collects vocabulary from the current node and its parents."""
    root = ContextNode("root")
    child = ContextNode("child")
    root.add_subcontext("child", child)
    
    # Add translations at different levels
    root.add_translation("volver", "return_command")
    child.add_translation("dibujar", "draw_command")
    
    nav = Navigator(root)
    nav.set_context(child)  # We place ourselves in the child
    
    exp = VoiceExplorer(voice_model=MagicMock(), navigator=nav)
    
    # 1. Ascending translation test
    assert exp._get_real_name_ascending("dibujar") == "draw_command"   # Found in child
    assert exp._get_real_name_ascending("volver") == "return_command"  # Found in root
    assert exp._get_real_name_ascending("unknown") == "unknown"        # Does not exist
    
    # 2. Active vocabulary test
    vocab = exp._navigation_vocabulary()
    assert "volver" in vocab
    assert "dibujar" in vocab
    assert "child" in vocab        # The key of the subcontext in the root
    assert "cancelar" in vocab     # Default word added by VoiceExplorer


def test_process_parameters_successful():
    """Test voice parameter collection and execution."""
    root = ContextNode("root")
    nav = Navigator(root)
    
    # Simulate the Command object to return what the user would say
    mock_command = MagicMock()
    # Make it so that when the system asks for the parameter, it hears "cinco"
    mock_command.exclusive_listen.return_value = "cinco"
    
    exp = VoiceExplorer(voice_model=MagicMock(), navigator=nav, command=mock_command)
    
    # Simulate a function (FunctionWrapper) that requires 1 parameter (radius)
    mock_wrapper = MagicMock()
    mock_wrapper.name = "draw_circle"
    mock_wrapper.param_specs = (ParamSpec(name="radius", param_type=int),)
    
    # Mock the navigator's call method so it doesn't actually execute anything
    nav.call = MagicMock(return_value="Circle drawn successfully")
    
    # Prepare the explorer in parameter mode
    exp.start_parameters(mock_wrapper)
    
    # Run the processing
    result = exp.process_parameters()
    
    # Verifications
    assert result is True
    # It should have converted "cinco" to an integer (5) and called the function
    nav.call.assert_called_once_with("draw_circle", 5, context_keys=["root"])
    assert exp.parameter_mode is False  # Should have been reset


def test_command_loop_navigation_and_cancellation():
    """Test the main flow: entering a subcontext and then cancelling."""
    root = ContextNode("root")
    child = ContextNode("Geometry")
    root.add_subcontext("Geometry", child)
    
    nav = Navigator(root)
    mock_command = MagicMock()
    
    # Simulate the user saying first "Geometry" and then "cancel"
    # side_effect allows returning a different value on each call
    mock_command.exclusive_listen.side_effect = ["Geometry", False]
    
    exp = VoiceExplorer(voice_model=MagicMock(), navigator=nav, command=mock_command)
    
    # Run the loop (it will stop automatically on "cancel")
    exp.command_loop()
    
    # Verify that the context was indeed changed to the child
    assert nav.current_context.name == "Geometry"
    # Verify that it listened exactly 2 times before exiting
    assert mock_command.exclusive_listen.call_count == 2