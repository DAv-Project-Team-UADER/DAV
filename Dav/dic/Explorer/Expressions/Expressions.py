# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from _lenient import LenientDict

def _safe_run_expr(idx: int):
    doc = App.ActiveDocument if hasattr(App, "ActiveDocument") else None
    if doc is None and idx in (0, 1):
        print("[DAV] Aviso: No hay documento activo para copiar expresiones.")
        return
    try:
        Gui.runCommand('Std_Expressions', idx)
    except Exception as e:
        print(f"[DAV] Expresiones: {e}")

expressions = {
    'copyactdoc': lambda: _safe_run_expr(1),
    'copyalldoc': lambda: _safe_run_expr(2),
    'copyselected': lambda: _safe_run_expr(0),
    'pasteexpr': lambda: _safe_run_expr(3),
    'help': ayuda
}

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
expressions = LenientDict(expressions)