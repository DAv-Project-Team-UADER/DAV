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