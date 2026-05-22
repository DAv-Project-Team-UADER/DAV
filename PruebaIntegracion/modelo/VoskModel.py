import json
import queue
import sys
import vosk
import sounddevice as sd

class VoskModel:
    """
    Wrapper de Vosk para manejar el reconocimiento de voz.
    """

    def __init__(self, model_path: str, debug: bool = False):
        vosk.SetLogLevel(-1)
        self._debug = debug
        self._model_path = model_path
        
        try:
            self._model = vosk.Model(model_path)
        except Exception as e:
            print(f"Error al cargar el modelo Vosk: {e}")
            sys.exit(1)
            
        self._q = queue.Queue()
        self._samplerate = 16000
        self._callback_texto = None
        if self._debug:
            print(f"[VoskModel] modelo cargado desde: {model_path}")
        
    def set_callback_texto(self, callback):
        """Asigna una función a la que se le pasará el texto detectado en tiempo real."""
        self._callback_texto = callback

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
            if self._debug:
                print(f"[VoskModel] status callback: {status}")
        self._q.put(bytes(indata))

    def escuchar_una_palabra(self) -> str:
        """
        Escucha el micrófono hasta detectar una frase y la devuelve limpia.
        """
        if self._debug:
            print("[VoskModel] esperando audio del micrófono")
        rec = vosk.KaldiRecognizer(self._model, self._samplerate)
        with sd.RawInputStream(samplerate=self._samplerate, blocksize=4000,
                               dtype='int16', channels=1, callback=self._callback):
            if self._debug:
                print("[VoskModel] stream de audio abierto")
            bloque = 0
            while True:
                data = self._q.get()
                bloque += 1
                if self._debug and bloque % 20 == 0:
                    print(f"[VoskModel] bloque de audio recibido: {len(data)} bytes (#{bloque})")
                if rec.AcceptWaveform(data):
                    resultado = json.loads(rec.Result())
                    texto = resultado.get("text", "").strip().lower()
                    if self._debug:
                        print(f"[VoskModel] resultado final crudo: {resultado}")
                    if texto:
                        # Si hay un callback de UI configurado, mandamos el texto
                        if self._callback_texto:
                            self._callback_texto(texto)
                        if self._debug:
                            print(f"[VoskModel] texto devuelto: {texto!r}")
                        return texto

    def escuchar_latente(self, frase_despertar: str = "cerrar", callback_texto=None) -> None:
        """
        Ejecución continua hasta que se dice la frase clave.
        """
        print(f"\n--- INICIANDO ESCUCHA LATENTE ('{frase_despertar}' para salir) ---")
        if self._debug:
            print(f"[VoskModel] modo latente iniciado con despertar={frase_despertar!r}")
        cb = callback_texto or self._callback_texto
        rec = vosk.KaldiRecognizer(self._model, self._samplerate)

        with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000,
                               dtype='int16', channels=1, callback=self._callback):
            if self._debug:
                print("[VoskModel] stream latente abierto")
            bloque = 0
            while True:
                data = self._q.get()
                bloque += 1
                if self._debug and bloque % 20 == 0:
                    print(f"[VoskModel] bloque latente recibido: {len(data)} bytes (#{bloque})")
                if rec.AcceptWaveform(data):
                    resultado = json.loads(rec.Result())
                    texto = resultado.get("text", "")
                    if self._debug:
                        print(f"[VoskModel] resultado latente crudo: {resultado}")
                    if texto:
                        print(f"Detectado: {texto}")
                        if cb:
                            cb(texto)
                        if frase_despertar in texto:
                            print("\n¡Frase detectada! Saliendo...")
                            break
