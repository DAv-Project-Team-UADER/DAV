import sys
import os
import threading
from PySide6.QtWidgets import QApplication

from MODELO.src.VoskModel.voskModel import VoskModel  # If wrapper usage is enforced
from MODELO.src.Command.command import Command

def run_exclusive_listening_pipeline(command_service: Command) -> None:
    """
    Spawns the exclusive listening lifecycle in a non-blocking dedicated worker thread.
    """
    command_service.print_test(vector_index=0)

def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    voice_adapter = VoiceCommandAdapter()

    window.voice_worker.final_result.connect(voice_adapter.receive_gui_phrase)
    
    command_processor = Command(voice_model=voice_adapter)
    
    engine_thread = threading.Thread(
        target=run_exclusive_listening_pipeline, 
        args=(command_processor,), 
        daemon=True
    )
    engine_thread.start()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()