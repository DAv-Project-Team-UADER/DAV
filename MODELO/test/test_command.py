import sys
import os
import pytest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.Command.command import Command
# --- Mock to simulate voice recognition without using the microphone ---
class MockVoiceModel:
    def __init__(self, mocked_words):
        self.mocked_words = mocked_words
        self.index = 0

    def escuchar_una_palabra(self):
        if self.index < len(self.mocked_words):
            word = self.mocked_words[self.index]
            self.index += 1
            return word
        return None 

# --- Test Cases ---

@patch('builtins.print')
def test_t0_print_test(mock_print):
    mock_voice_model = MockVoiceModel(["linea fina", "enter", "enviar"])
    command_instance = Command(mock_voice_model)
    
    command_instance.print_test(1)
    
    mock_print.assert_any_call(">>> w = 'linea fina'")


def test_t1_continuous_input():
    mock_voice_model = MockVoiceModel(["uno", "dos", "enviar"])
    command_instance = Command(mock_voice_model)
    
    result = command_instance.exclusive_listen(0)
    
    assert result == "12", f"Expected '12', but got '{result}'"


def test_t2_cancel_midway():
    mock_voice_model = MockVoiceModel(["linea normal", "enter", "cancelar"])
    command_instance = Command(mock_voice_model)

    result = command_instance.exclusive_listen(1)
    
    assert result is False, "Result should be False after canceling the command"


def test_t3_ignore_garbage_tokens():

    mock_voice_model = MockVoiceModel(["uno", "hola", "dos", "enviar"])
    command_instance = Command(mock_voice_model)
    
    result = command_instance.exclusive_listen(0)
    
    assert result == "12", f"Expected '12' (ignoring 'hola'), but got '{result}'"