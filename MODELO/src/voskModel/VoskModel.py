import json
import queue
import sys
import vosk
import sounddevice as sd

class VoskModel:
    """
    Wrapper de Vosk para manejar el reconocimiento de voz.
    """

    def __init__(self, model_path: str):
        vosk.SetLogLevel(-1)
        
        try:
            self._model = vosk.Model(model_path)
        except Exception as e:
            print(f"Error al cargar el modelo Vosk: {e}")
            sys.exit(1)
            
        self._q = queue.Queue()
        self._samplerate = 16000
        self._callback_texto = None
        
    def set_callback_texto(self, callback):
        """Asigna una función a la que se le pasará el texto detectado en tiempo real."""
        self._callback_texto = callback

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self._q.put(bytes(indata))

    def escuchar_una_palabra(self) -> str:
        """
        Escucha el micrófono hasta detectar una frase y la devuelve limpia.
        """
        rec = vosk.KaldiRecognizer(self._model, self._samplerate)
        with sd.RawInputStream(samplerate=self._samplerate, blocksize=4000,
                               dtype='int16', channels=1, callback=self._callback):
            while True:
                data = self._q.get()
                if rec.AcceptWaveform(data):
                    resultado = json.loads(rec.Result())
                    texto = resultado.get("text", "").strip().lower()
                    if texto:
                        # Si hay un callback de UI configurado, mandamos el texto
                        if self._callback_texto:
                            self._callback_texto(texto)
                        return texto

    def escuchar_latente(self, frase_despertar: str = "cerrar", callback_texto=None) -> None:
        """
        Ejecución continua hasta que se dice la frase clave.
        """
        print(f"\n--- INICIANDO ESCUCHA LATENTE ('{frase_despertar}' para salir) ---")
        cb = callback_texto or self._callback_texto
        rec = vosk.KaldiRecognizer(self._model, self._samplerate)

        with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000,
                               dtype='int16', channels=1, callback=self._callback):
            while True:
                data = self._q.get()
                if rec.AcceptWaveform(data):
                    resultado = json.loads(rec.Result())
                    texto = resultado.get("text", "")
                    if texto:
                        print(f"Detectado: {texto}")
                        if cb:
                            cb(texto)
                        if frase_despertar in texto:
                            print("\n¡Frase detectada! Saliendo...")
                            break
