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
# Fuentes: PartDesign_LinearPattern.txt, PartDesign_Mirrored.txt,
#   PartDesign_PolarPattern.txt, PartDesign_MultiTransform.txt,
#   PartDesign_Scaled.txt
# Revisión:
#   - LinearPattern, Mirrored, PolarPattern, MultiTransform: usan Gui.runCommand.
#   - Scaled: el ticket indica explícitamente que NO tiene comando independiente.
#     Solo accesible desde el panel de Multi-Transform > clic derecho.
#     Se OMITE del diccionario; documentado en ayuda().
# ─────────────────────────────────────────────────────────────────────────────

import FreeCADGui as Gui
from .ayuda import ayuda

patrones = {
    'lineal':         lambda: Gui.runCommand('PartDesign_LinearPattern', 0),
    'espejo':         lambda: Gui.runCommand('PartDesign_Mirrored', 0),
    'polar':          lambda: Gui.runCommand('PartDesign_PolarPattern', 0),
    'multitransform': lambda: Gui.runCommand('PartDesign_MultiTransform', 0),
    'help':           ayuda,
}
