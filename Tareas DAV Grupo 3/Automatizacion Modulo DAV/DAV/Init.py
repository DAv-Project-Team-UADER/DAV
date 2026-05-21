# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os, sys, subprocess, urllib.request, zipfile, ssl, FreeCAD

print("DAV: Configurando rutas...")
MODULE_DIR = os.path.join(FreeCAD.getHomePath(), 'Mod', 'DAV')
PACKAGES_DIR = os.path.join(MODULE_DIR, 'packages')
MODELS_DIR = os.path.join(MODULE_DIR, 'models')

print("MODULE_DIR:", MODULE_DIR)
print("PACKAGES_DIR:", PACKAGES_DIR)
print("MODELS_DIR:", MODELS_DIR)

if PACKAGES_DIR not in sys.path:
    sys.path.insert(0, PACKAGES_DIR)

os.makedirs(PACKAGES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# --- Instalación de librerías (código directo) ---
print("DAV: Verificando librerías...")
required = [
    'flask',
    'pyaudio',
    'sounddevice',
    'SpeechRecognition',
    'playsound3',
    'pydub',
    'vosk'
]
python_exe = os.path.join(os.path.dirname(sys.executable), 'python.exe')

for package in required:
    try:
        __import__(package)
        print(f"DAV: {package} ya está instalado.")
    except ImportError:
        print(f"DAV: Instalando {package} en {PACKAGES_DIR}...")
        try:
            subprocess.check_call([
                python_exe, '-m', 'pip', 'install',
                '--target=' + PACKAGES_DIR,
                package
            ])
            print(f"DAV: {package} instalado correctamente.")
        except Exception as e:
            print(f"DAV: Error instalando {package}: {e}")

# --- Descarga del modelo Vosk (código directo) ---
MODELO_ELEGIDO = "vosk-model-small-es-0.42"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODELO_ELEGIDO}.zip"
model_path = os.path.join(MODELS_DIR, MODELO_ELEGIDO)

if os.path.exists(model_path):
    print(f"DAV: Modelo {MODELO_ELEGIDO} ya existe.")
else:
    zip_path = os.path.join(MODELS_DIR, f"{MODELO_ELEGIDO}.zip")
    print(f"DAV: Descargando modelo {MODELO_ELEGIDO} (puede demorar)...")
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(MODEL_URL, context=ctx) as response:
            with open(zip_path, 'wb') as f:
                f.write(response.read())
        print("DAV: Extrayendo modelo...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(MODELS_DIR)
        os.remove(zip_path)
        print("DAV: Modelo instalado correctamente.")
    except Exception as e:
        print(f"DAV: Error descargando modelo: {e}")
        if os.path.exists(zip_path):
            os.remove(zip_path)

print("DAV: Módulo inicializado completamente.")