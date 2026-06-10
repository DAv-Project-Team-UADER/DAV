# trigger_capture.py
# Envía señales a la macro y asegura que esté instalada

import os
import json
import time
import shutil

def ensure_macro_installed():
    """
    Asegura que la macro 'capture_tree.FCMacro' esté instalada en FreeCAD.
    Si no existe, la copia desde la carpeta del proyecto.
    """
    # Ruta de la macro en el proyecto
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_macro = os.path.join(project_dir, "capture_tree.FCMacro")
    
    # Eliminar imagen de captura y archivo de señal anteriores para iniciar limpio
    stale_image = os.path.join(project_dir, "tree_capture.png")
    if os.path.exists(stale_image):
        try:
            os.remove(stale_image)
            print("[INFO] Imagen de captura anterior eliminada para iniciar limpio")
        except Exception as e:
            print(f"[WARNING] No se pudo eliminar la imagen anterior: {e}")
            
    stale_signal = os.path.join(project_dir, "capture_signal.json")
    if os.path.exists(stale_signal):
        try:
            os.remove(stale_signal)
        except:
            pass
            
    # Verificar que existe en el proyecto
    if not os.path.exists(project_macro):
        print(f"[ERROR] Macro no encontrada en el proyecto: {project_macro}")
        print("   Asegúrese de que 'capture_tree.FCMacro' esté en la carpeta del proyecto")
        return False
    
    # Detectar carpeta de macros de FreeCAD
    appdata = os.environ.get("APPDATA", "")
    if not appdata:
        appdata = os.path.expanduser("~")
    
    # Buscar la versión de FreeCAD instalada
    freecad_paths = [
        r"C:\Program Files\FreeCAD 1.1\bin\FreeCAD.exe",
        r"C:\Program Files\FreeCAD\bin\FreeCAD.exe",
        r"C:\Program Files\FreeCAD 1.0\bin\FreeCAD.exe",
    ]
    
    installed_version = None
    for path in freecad_paths:
        if os.path.exists(path):
            if "1.1" in path:
                installed_version = "1.1"
            elif "1.0" in path:
                installed_version = "1.0"
            else:
                installed_version = "default"
            break
    
    # Determinar carpeta de macros
    if installed_version == "1.1":
        macro_folder = os.path.join(appdata, "FreeCAD", "v1-1", "Macro")
    elif installed_version == "1.0":
        macro_folder = os.path.join(appdata, "FreeCAD", "v1-0", "Macro")
    else:
        macro_folder = os.path.join(appdata, "FreeCAD", "Macro")
    
    # Crear carpeta si no existe
    if not os.path.exists(macro_folder):
        try:
            os.makedirs(macro_folder, exist_ok=True)
            print(f"[INFO] Carpeta de macros creada: {macro_folder}")
        except Exception as e:
            print(f"[WARNING] No se pudo crear carpeta de macros: {e}")
            return False
    
    # Escribir archivo de configuración dav_paths.json
    try:
        config_dir = os.path.join(appdata, "FreeCAD")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "dav_paths.json")
        paths = {
            "signal_file": os.path.abspath(os.path.join(project_dir, "capture_signal.json")),
            "image_path": os.path.abspath(os.path.join(project_dir, "tree_capture.png"))
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(paths, f, indent=4, ensure_ascii=False)
        print(f"[OK] Archivo de configuración escrito: {config_path}")
    except Exception as e:
        print(f"[WARNING] No se pudo escribir archivo de configuración: {e}")
    
    installed_macro = os.path.join(macro_folder, "capture_tree.FCMacro")
    
    # Verificar si la macro ya está instalada
    if os.path.exists(installed_macro):
        # Comparar fechas para ver si hay que actualizar
        project_time = os.path.getmtime(project_macro)
        installed_time = os.path.getmtime(installed_macro)
        
        if installed_time >= project_time:
            print("[OK] Macro ya instalada y actualizada")
            return True
        else:
            print("[UPDATE] Actualizando macro...")
    
    # Copiar la macro
    try:
        shutil.copy2(project_macro, installed_macro)
        print(f"[OK] Macro instalada en: {installed_macro}")
        return True
    except Exception as e:
        print(f"[WARNING] No se pudo instalar la macro: {e}")
        return False

def trigger_capture(timeout=5):
    """
    Envía una señal a la macro en FreeCAD (que ya está ejecutándose)
    """
    signal_file = os.path.join(os.path.dirname(__file__), "capture_signal.json")
    
    # Limpiar señal anterior
    if os.path.exists(signal_file):
        try:
            os.remove(signal_file)
        except:
            pass
    
    # Crear archivo de señal
    with open(signal_file, 'w') as f:
        json.dump({"command": "capture"}, f)
    
    # Esperar resultado
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(signal_file):
            try:
                with open(signal_file, 'r') as f:
                    data = json.load(f)
                    if data.get("status") == "done":
                        return data.get("result", {}).get("success", False)
            except:
                pass
        time.sleep(0.2)
    
    return False


if __name__ == "__main__":
    success = trigger_capture()
    print(f"Captura exitosa: {success}")