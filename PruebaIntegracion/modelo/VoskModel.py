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
import sys
import vosk
import sounddevice as sd

class VoskModel:
    """
    Vosk wrapper to handle speech recognition.
    """

    def __init__(self, model_path: str, debug: bool = False):
        vosk.SetLogLevel(-1)
        self._debug = debug
        self._model_path = model_path
        
        try:
            self._model = vosk.Model(model_path)
        except Exception as e:
            print(f"Error loading Vosk model: {e}")
            sys.exit(1)
            
        self._q = queue.Queue()
        self._samplerate = 16000
        self._text_callback = None
        if self._debug:
            print(f"[VoskModel] model loaded from: {model_path}")
        
    def set_text_callback(self, callback):
        """Assigns a function that will receive the detected text in real-time."""
        self._text_callback = callback

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
            if self._debug:
                print(f"[VoskModel] callback status: {status}")
        self._q.put(bytes(indata))

    def listen_for_one_word(self) -> str:
        """
        Listens from the microphone until a phrase is detected and returns it cleaned.
        """
        if self._debug:
            print("[VoskModel] waiting for microphone audio")
        rec = vosk.KaldiRecognizer(self._model, self._samplerate)
        with sd.RawInputStream(samplerate=self._samplerate, blocksize=4000,
                               dtype='int16', channels=1, callback=self._callback):
            if self._debug:
                print("[VoskModel] audio stream opened")
            block = 0
            while True:
                data = self._q.get()
                block += 1
                if self._debug and block % 20 == 0:
                    print(f"[VoskModel] audio block received: {len(data)} bytes (#{block})")
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip().lower()
                    if self._debug:
                        print(f"[VoskModel] raw final result: {result}")
                    if text:
                        # If a UI callback is configured, send the text
                        if self._text_callback:
                            self._text_callback(text)
                        if self._debug:
                            print(f"[VoskModel] returned text: {text!r}")
                        return text

    def listen_continuously(self, wake_phrase: str = "cerrar", text_callback=None) -> None:
        """
        Continuous execution until the wake phrase is spoken.
        """
        print(f"\n--- STARTING CONTINUOUS LISTENING ('{wake_phrase}' to exit) ---")
        if self._debug:
            print(f"[VoskModel] continuous mode started with wake phrase={wake_phrase!r}")
        cb = text_callback or self._text_callback
        rec = vosk.KaldiRecognizer(self._model, self._samplerate)

        with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000,
                               dtype='int16', channels=1, callback=self._callback):
            if self._debug:
                print("[VoskModel] continuous stream opened")
            block = 0
            while True:
                data = self._q.get()
                block += 1
                if self._debug and block % 20 == 0:
                    print(f"[VoskModel] continuous block received: {len(data)} bytes (#{block})")
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if self._debug:
                        print(f"[VoskModel] raw continuous result: {result}")
                    if text:
                        print(f"Detected: {text}")
                        if cb:
                            cb(text)
                        if wake_phrase in text:
                            print("\nWake phrase detected! Exiting...")
                            break