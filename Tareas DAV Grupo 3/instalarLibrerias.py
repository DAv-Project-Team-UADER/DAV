import subprocess, sys, os, FreeCAD

additional_dir = os.path.join(FreeCAD.getUserAppDataDir(), 'AdditionalPythonPackages')
os.makedirs(additional_dir, exist_ok=True)

# CORRECCIÓN: usar python.exe en lugar de freecad.exe
python_exe = os.path.join(os.path.dirname(sys.executable), 'python.exe')

packages_to_install = ['flask', 'pyaudio', 'sounddevice', 'SpeechRecognition', 'playsound3', 'pydub', 'vosk']

for package in packages_to_install:
    try:
        subprocess.check_call([python_exe, '-m', 'pip', 'install', '--target=' + additional_dir, package])
        print(f'{package} instalado correctamente.')
    except Exception as e:
        print(f'Error instalando {package}: {e}')

print('Proceso terminado. Reiniciá FreeCAD si es la primera vez que se creó AdditionalPythonPackages.')

