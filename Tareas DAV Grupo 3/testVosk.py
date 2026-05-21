import json
import vosk
import pyaudio

# Ruta al modelo (ajustala si cambiaste la carpeta)
MODEL_PATH = r"D:\Facultad\PET DAV\1er Tarea\modelos_vosk\vosk-model-small-es-0.42"

# Cargar el modelo
print("DAV: Cargando modelo Vosk...")
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Configurar PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000)
stream.start_stream()

print("DAV: Modelo cargado. ¡Hablá ahora! (esperando hasta 5 segundos)")
# Escucha durante ~5 segundos (podés modificar el rango)
for i in range(0, 25):  # 25 bloques de 4000 muestras a 16000 Hz ≈ 6.25 segundos
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        texto = result.get("text", "")
        if texto:
            print("DAV: Texto reconocido =>", texto)
            break
else:
    # Si no se detectó nada, mostramos el resultado parcial final
    result = json.loads(recognizer.FinalResult())
    print("DAV: Resultado final =>", result.get("text", "(nada)"))

# Limpiar
stream.stop_stream()
stream.close()
p.terminate()
print("DAV: Prueba finalizada.")