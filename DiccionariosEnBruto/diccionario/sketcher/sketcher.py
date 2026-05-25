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

# ─────────────────────────────────────────────────────────────────────────────
# Fuentes: PartDesign_Preferences.txt, Part_CheckGeometry.txt,
#   Sketcher_EditSketch.txt, Sketcher_MapSketch.txt, Sketcher_ValidateSketch.txt
# Revisión:
#   - Preferences: usa Gui.runCommand('PartDesign_Preferences', 0).
#   - Part_CheckGeometry: el ticket usa scripting API Python (obj.Shape.check).
#     Se expone como función Python que recibe el objeto como argumento.
#   - EditSketch, MapSketch, ValidateSketch: requieren objetos como argumento,
#     no pueden ser lambdas sin args. Se documentan en ayuda.py únicamente.
# ─────────────────────────────────────────────────────────────────────────────

import FreeCADGui as Gui
from .ayuda import ayuda


def _verificar(obj):
    """Part_CheckGeometry — Verifica la geometría de un sólido.
    Imprime si el Shape es válido, su volumen y la lista de errores.
    """
    print(f'Objeto: {obj.Name}')
    print(f'  Válido : {obj.Shape.isValid()}')
    print(f'  Volumen: {obj.Shape.Volume:.4f} mm³')
    errors = obj.Shape.check(True)
    if errors:
        print(f'  Errores ({len(errors)}):')
        for e in errors:
            print(f'    - {e}')
    else:
        print('  Sin errores geométricos.')


sketcher = {
    'preferencias': lambda: Gui.runCommand('PartDesign_Preferences', 0),
    'verificar':    _verificar,
    'help':         ayuda,
}
