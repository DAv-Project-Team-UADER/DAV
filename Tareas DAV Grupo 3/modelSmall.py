import os
import sys
import urllib.request
import zipfile
import ssl

# --- Configuración ---
PROJECT_DIR = r"D:\Facultad\PET DAV\1er Tarea"
MODELS_DIR = os.path.join(PROJECT_DIR, "modelos_vosk")
os.makedirs(MODELS_DIR, exist_ok=True)

# Elegí el modelo pequeño (podés cambiarlo al grande si querés)
MODELO_ELEGIDO = "vosk-model-small-es-0.42"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODELO_ELEGIDO}.zip"
MODEL_PATH = os.path.join(MODELS_DIR, MODELO_ELEGIDO)

def descargar_zip(url, destino):
    """Descarga un archivo de forma segura, ignorando verificación SSL si es necesario."""
    try:
        # Contexto sin verificación SSL (solo para evitar errores en redes con proxy o certificados)
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=ctx) as response:
            with open(destino, 'wb') as f:
                f.write(response.read())
    except Exception as e:
        raise Exception(f"Fallo la descarga: {e}")

def descargar_y_extraer_modelo():
    if os.path.exists(MODEL_PATH):
        print(f"DAV: El modelo '{MODELO_ELEGIDO}' ya existe en {MODEL_PATH}")
        return

    zip_path = os.path.join(MODELS_DIR, f"{MODELO_ELEGIDO}.zip")
    try:
        print(f"DAV: Descargando {MODELO_ELEGIDO} (puede tardar unos minutos)...")
        descargar_zip(MODEL_URL, zip_path)

        print(f"DAV: Extrayendo el modelo en {MODELS_DIR}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MODELS_DIR)

        os.remove(zip_path)
        print(f"DAV: ¡Modelo {MODELO_ELEGIDO} instalado exitosamente en {MODEL_PATH}!")

    except Exception as e:
        print(f"DAV: Error durante la descarga o extracción: {e}")
        if os.path.exists(zip_path):
            os.remove(zip_path)

# Ejecutar la función
descargar_y_extraer_modelo()