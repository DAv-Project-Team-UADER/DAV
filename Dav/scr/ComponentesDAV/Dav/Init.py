# DAV (UADER) — App module (logic / document objects go here later).

import os
import sys

# Linux: iniciar_dav.sh instala sounddevice/vosk en una carpeta aparte
# (GUIFreeCad/.freecad_deps) porque el Python de FreeCAD (AppImage) no ve el
# .venv de GUIFreeCad. Se agrega AL FINAL de sys.path para que los paquetes
# que ya trae FreeCAD (PySide6, numpy, ...) sigan teniendo prioridad.
_deps = os.environ.get("DAV_FC_DEPS_DIR", "").strip()
if _deps and os.path.isdir(_deps) and _deps not in sys.path:
    sys.path.append(_deps)
