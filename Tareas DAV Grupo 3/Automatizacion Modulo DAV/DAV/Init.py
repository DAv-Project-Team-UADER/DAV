# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import urllib.request
import zipfile
import ssl
import FreeCAD

class DAVInstaller:
    """Clase que centraliza la instalación de dependencias y modelos de Vosk."""
    
    # Atributos de clase (evitan problemas de ámbito con exec)
    MODULE_DIR = os.path.join(FreeCAD.getHomePath(), 'Mod', 'DAV')
    PACKAGES_DIR = os.path.join(MODULE_DIR, 'packages')
    MODELS_DIR = os.path.join(MODULE_DIR, 'models')
    
    REQUIRED_PACKAGES = [
        'flask',
        'pyaudio',
        'sounddevice',
        'SpeechRecognition',
        'playsound3',
        'pydub',
        'vosk'
    ]
    
    MODEL_NAME = "vosk-model-small-es-0.42"
    MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"
    
    @staticmethod
    def configure_paths():
        """Configura las rutas y añade el directorio de paquetes al sys.path."""
        print("DAV: Configurando rutas...")
        print("MODULE_DIR:", DAVInstaller.MODULE_DIR)
        print("PACKAGES_DIR:", DAVInstaller.PACKAGES_DIR)
        print("MODELS_DIR:", DAVInstaller.MODELS_DIR)
        
        if DAVInstaller.PACKAGES_DIR not in sys.path:
            sys.path.insert(0, DAVInstaller.PACKAGES_DIR)
        
        os.makedirs(DAVInstaller.PACKAGES_DIR, exist_ok=True)
        os.makedirs(DAVInstaller.MODELS_DIR, exist_ok=True)
    
    @staticmethod
    def install_libraries():
        """Verifica e instala las librerías requeridas."""
        print("DAV: Verificando librerías...")
        python_exe = os.path.join(os.path.dirname(sys.executable), 'python.exe')
        
        for package in DAVInstaller.REQUIRED_PACKAGES:
            try:
                __import__(package)
                print(f"DAV: {package} ya está instalado.")
            except ImportError:
                print(f"DAV: Instalando {package} en {DAVInstaller.PACKAGES_DIR}...")
                try:
                    subprocess.check_call([
                        python_exe, '-m', 'pip', 'install',
                        '--target=' + DAVInstaller.PACKAGES_DIR,
                        package
                    ])
                    print(f"DAV: {package} instalado correctamente.")
                except Exception as e:
                    print(f"DAV: Error instalando {package}: {e}")
    
    @staticmethod
    def download_model():
        """Descarga y extrae el modelo Vosk si no existe."""
        model_path = os.path.join(DAVInstaller.MODELS_DIR, DAVInstaller.MODEL_NAME)
        
        if os.path.exists(model_path):
            print(f"DAV: Modelo {DAVInstaller.MODEL_NAME} ya existe.")
            return
        
        zip_path = os.path.join(DAVInstaller.MODELS_DIR, f"{DAVInstaller.MODEL_NAME}.zip")
        print(f"DAV: Descargando modelo {DAVInstaller.MODEL_NAME} (puede demorar)...")
        try:
            ctx = ssl._create_unverified_context()
            with urllib.request.urlopen(DAVInstaller.MODEL_URL, context=ctx) as response:
                with open(zip_path, 'wb') as f:
                    f.write(response.read())
            print("DAV: Extrayendo modelo...")
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(DAVInstaller.MODELS_DIR)
            os.remove(zip_path)
            print("DAV: Modelo instalado correctamente.")
        except Exception as e:
            print(f"DAV: Error descargando modelo: {e}")
            if os.path.exists(zip_path):
                os.remove(zip_path)
    
    @staticmethod
    def initialize():
        """Ejecuta toda la inicialización del módulo."""
        DAVInstaller.configure_paths()
        DAVInstaller.install_libraries()
        DAVInstaller.download_model()
        print("DAV: Módulo inicializado completamente.")

# Ejecutar la inicialización automáticamente al cargar el módulo
DAVInstaller.initialize()