import FreeCAD
import sys
import os

# Esto le dice a Python que mire qué hay en la carpeta donde está este archivo
ruta_actual = os.path.dirname(__file__)
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

# Ahora importamos los archivos directo
try:
    from DraftWorkbench import DraftWorkbench as dw
    from TechDrawWorkbench import TechDrawWorkbench as tw
    import ayuda
except ImportError:
    # Si falla, intentamos la ruta por carpetas
    from .DraftWorkbench import DraftWorkbench as dw
    from .TechDrawWorkbench import TechDrawWorkbench as tw
    from . import ayuda

explorer = {
    'draft': dw.draft_workbench,
    'techdraw': tw.techdraw_workbench,
    'help': ayuda.ayuda
}