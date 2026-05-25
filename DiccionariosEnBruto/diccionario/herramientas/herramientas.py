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
# Fuentes: PartDesign_Body.txt, PartDesign_NewSketch.txt, PartDesign_Boolean.txt,
#   PartDesign_Clone.txt, PartDesign_WizardShaft.txt, PartDesign_MoveTip.txt,
#   PartDesign_MoveFeature.txt, PartDesign_MoveFeatureInTree.txt,
#   PartDesign_SubShapeBinder.txt
# Revisión:
#   - Body, NewSketch, Boolean, Clone, WizardShaft, MoveTip, MoveFeature,
#     MoveFeatureInTree: usan Gui.runCommand correctamente.
#   - SubShapeBinder: el ticket usa scripting API (body.newObject).
#     Se expone como función Python; requiere objeto fuente y subforma como args.
# ─────────────────────────────────────────────────────────────────────────────

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda


def _binder(source_obj, subshape='Face1', name='SubShapeBinder', bind_mode=0):
    """PartDesign_SubShapeBinder — Referencia geométrica externa en el Body activo.
    bind_mode: 0 = Synchronized (auto-update), 1 = Frozen (copia fija).
    """
    doc  = App.ActiveDocument
    body = doc.getObject('Body')
    if body is None:
        raise ValueError('No hay Body activo. Crea o activa un Body primero.')
    binder = body.newObject('PartDesign::SubShapeBinder', name)
    binder.Support   = [(source_obj, (subshape,))]
    binder.BindMode  = bind_mode
    doc.recompute()
    return binder


herramientas = {
    'body':           lambda: Gui.runCommand('PartDesign_Body', 0),
    'nuevocroquis':   lambda: Gui.runCommand('PartDesign_NewSketch', 0),
    'booleana':       lambda: Gui.runCommand('PartDesign_Boolean', 0),
    'clonar':         lambda: Gui.runCommand('PartDesign_Clone', 0),
    'eje':            lambda: Gui.runCommand('PartDesign_WizardShaft', 0),
    'movertip':       lambda: Gui.runCommand('PartDesign_MoveTip', 0),
    'moverfeature':   lambda: Gui.runCommand('PartDesign_MoveFeature', 0),
    'moverarbolfeat': lambda: Gui.runCommand('PartDesign_MoveFeatureInTree', 0),
    'binder':         _binder,
    'help':           ayuda,
}
