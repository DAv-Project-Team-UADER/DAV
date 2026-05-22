import json
import queue
import sounddevice as sd
import vosk
from PySide6.QtCore import Signal, QObject

class VoiceWorker(QObject):
    finished = Signal()
    partial_result = Signal(str)
    final_result = Signal(str)
    status_signal = Signal(str)

    def __init__(self, model_path="vosk-model-small-es-0.42"):
        super().__init__()
        self.model_path = model_path
        self.running = True
        self.audio_queue = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(bytes(indata))

    def run(self):
        try:
            self.status_signal.emit("active")
            model = vosk.Model(self.model_path)
            recognizer = vosk.KaldiRecognizer(model, 16000)
            stream = sd.RawInputStream(
                samplerate=16000, blocksize=8000, channels=1, dtype='int16',
                callback=self.audio_callback
            )
            with stream:
                while self.running:
                    try:
                        data = self.audio_queue.get(timeout=0.5)
                        if recognizer.AcceptWaveform(data):
                            result = json.loads(recognizer.Result())
                            text = result.get("text", "")
                            if text:
                                self.final_result.emit(text)
                        else:
                            partial = json.loads(recognizer.PartialResult())
                            partial_text = partial.get("partial", "")
                            if partial_text:
                                self.partial_result.emit(partial_text)
                    except queue.Empty:
                        continue
                    except Exception as e:
                        self.status_signal.emit(f"error:{e}")
        except Exception as e:
            self.status_signal.emit(f"error:{e}")
        finally:
            self.finished.emit()

    def stop(self):
        self.running = False