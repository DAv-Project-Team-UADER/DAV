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
        # Configuramos Vosk para que no sature la consola con logs internos
        vosk.SetLogLevel(-1)
        
        try:
            self._model = vosk.Model(model_path)
        except Exception as e:
            print(f"Error al cargar el modelo de Vosk en la ruta '{model_path}': {e}")
            sys.exit(1)
            
        self._q = queue.Queue()
        self._samplerate = 16000 # Frecuencia estándar para modelos Vosk pequeños
        
    def _callback(self, indata, frames, time, status):
        """Función interna que recibe el audio de sounddevice."""
        if status:
            print(status, file=sys.stderr)
        self._q.put(bytes(indata))

    def escuchar_latente(self, frase_despertar: str = "cerrar", callback_texto=None) -> None:
        """
        Ejecución continua hasta que se dice la frase de activación/despertar.
        """
        print("\n--- INICIANDO ESCUCHA LATENTE ---")
        print(f"Diga la frase clave '{frase_despertar}' para terminar el bucle.")
        
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
                        
                        # Le mandamos el texto detectado a la ventana (si existe el callback)
                        if callback_texto:
                            callback_texto(texto)
                        
                        if frase_despertar in texto:
                            print(f"\n¡Frase '{frase_despertar}' detectada! Saliendo de la escucha latente...")
                            break
