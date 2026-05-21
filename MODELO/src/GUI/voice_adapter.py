import queue
from PySide6.QtCore import QObject, Slot


class VoiceCommandAdapter(QObject):
  
    def __init__(self, parent=None):
        super().__init__(parent)
        self._phrase_queue: queue.Queue[str] = queue.Queue()
        self._active = True

    def connect_worker(self, voice_worker) -> None:
        voice_worker.final_result.connect(self._on_final_result)

    def disconnect_worker(self, voice_worker) -> None:
        try:
            voice_worker.final_result.disconnect(self._on_final_result)
        except RuntimeError:
            pass

    @Slot(str)
    def _on_final_result(self, text: str) -> None:
        if self._active and text.strip():
            self._phrase_queue.put(text.strip())

    @Slot(str)
    def receive_gui_phrase(self, text: str) -> None:
        self._on_final_result(text)

    def escuchar_una_palabra(self, timeout: float = 30.0) -> str:
        try:
            return self._phrase_queue.get(timeout=0.5)
        except queue.Empty:
            return None

    def flush(self) -> None:
        while not self._phrase_queue.empty():
            try:
                self._phrase_queue.get_nowait()
            except queue.Empty:
                break

    def stop(self) -> None:
    
        self._active = False
        self._phrase_queue.put("") 