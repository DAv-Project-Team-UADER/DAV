# Cómo instalar DAV en FreeCAD (carpeta Mod)

Tu amigo tiene razón: en FreeCAD los workbenches viven en una carpeta **`Mod`**, junto a `Part`, `Sketcher`, etc.

## Dos ubicaciones posibles

| Ubicación | Ruta en tu PC (ejemplo) | Cuándo |
|-----------|-------------------------|--------|
| **Mod del sistema** (recomendado) | `L:\Programas\Freecad\Mod\DAV\` | Instalación normal de FreeCAD |
| **Mod del usuario** (respaldo) | `%APPDATA%\FreeCAD\v1-1\Mod\DAV\` | Sin permisos de admin en `L:\` |

Cada módulo es una carpeta con al menos:

```
DAV/
  Init.py
  InitGui.py
  package.xml
  scr/
  ...
```

**GUIFreeCad** no va dentro de `Mod`: sigue en `Repositorio DAVFreeCad\GUIFreeCad`. DAV solo enlaza a esa carpeta para preferencias y voz.

---

## Instalación automática (recomendada)

Desde PowerShell:

```powershell
cd "...\DAV-Luigi\scripts"
.\run_freecad_dav.ps1
```

El script:

1. Crea un **enlace** `Mod\DAV` → tu carpeta `DAV-Luigi\Dav` (cambios en el repo se ven al instante).
2. Intenta primero **`L:\Programas\Freecad\Mod\DAV`** (Mod del sistema).
3. Si no hay permisos, usa **`AppData\...\Mod\DAV`**.
4. Abre FreeCAD con `DAV_GUI_FREECAD_ROOT` y preferencias.

Solo instalar sin abrir FreeCAD:

```powershell
.\install_dav_mod.ps1
```

Si falla el Mod del sistema, ejecutá PowerShell **como administrador** una vez.

---

## Instalación manual (como te dijo tu amigo)

1. Cerrá FreeCAD.
2. Copiá o enlazá la carpeta del repo:

   **Origen:** `DAV-Luigi\Dav`  
   **Destino:** `L:\Programas\Freecad\Mod\DAV`

   Enlace (cmd como admin):

   ```cmd
   mklink /J "L:\Programas\Freecad\Mod\DAV" "C:\Users\Luigi\OneDrive\Escritorio\Facultad\Yo\PET\Repositorio DAVFreeCad\DAVFreecad-Pruebas\DAV-Luigi\Dav"
   ```

3. Definí variable de usuario (opcional pero útil):

   `DAV_GUI_FREECAD_ROOT` = ruta a `GUIFreeCad`

4. Abrí FreeCAD → workbench **DAV** → **Preferencias DAV**.

---

## Si compilás FreeCAD desde `FREECAD/`

Al compilar, CMake puede copiar `Dav` a `build\Mod\DAV`. Mientras desarrollás, el enlace en `L:\Programas\Freecad\Mod\DAV` o el script `run_freecad_dav.ps1` alcanzan.

---

## Dependencias de voz (una vez)

```powershell
& "L:\Programas\Freecad\bin\python.exe" -m pip install vosk sounddevice numpy requests
```

---

## Problemas frecuentes

| Síntoma | Solución |
|---------|----------|
| FreeCAD “normal”, sin DAV | Verificá que exista `Mod\DAV\InitGui.py` |
| Error `__file__` | Actualizá `Dav\InitGui.py` del repo |
| DAV cargado dos veces | No uses `-M` y enlace a la vez; usá solo `Mod\DAV` |
| Sin voz | `pip install` en el **python de FreeCAD**, no en Python 3.13 del sistema |
