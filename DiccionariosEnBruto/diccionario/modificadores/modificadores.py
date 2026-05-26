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
# Fuentes: PartDesign_Chamfer.txt, PartDesign_Draft.txt, PartDesign_Fillet.txt,
#   PartDesign_Thickness.txt
# Revisión:
#   - Chamfer, Draft, Fillet: usan Gui.runCommand correctamente.
#   - Thickness: el ticket usa scripting API (body.newObject + .Base + .Value).
#     Se expone como función Python; requiere el objeto base y la cara como args.
# ─────────────────────────────────────────────────────────────────────────────

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda


def _grosor(base_feature_name, face_name='Face6', value=1.5, name='Thickness'):
    """PartDesign_Thickness — Vacía un sólido dejando paredes de grosor uniforme.
    base_feature_name: nombre del objeto Pad/Pocket base (str).
    face_name:         nombre de la cara a eliminar (apertura), ej: 'Face6'.
    value:             grosor de pared en mm.
    """
    doc  = App.ActiveDocument
    body = doc.getObject('Body')
    if body is None:
        raise ValueError('No hay Body activo.')
    base = doc.getObject(base_feature_name)
    if base is None:
        raise ValueError(
            f"El objeto '{base_feature_name}' no existe en el documento."
        )
    thickness = body.newObject('PartDesign::Thickness', name)
    thickness.Base  = (base, [face_name])
    thickness.Value = value
    doc.recompute()
    return thickness


modificadores = {
    'chaflan':   lambda: Gui.runCommand('PartDesign_Chamfer', 0),
    'desmoldeo': lambda: Gui.runCommand('PartDesign_Draft', 0),
    'redondeo':  lambda: Gui.runCommand('PartDesign_Fillet', 0),
    'grosor':    _grosor,
    'help':      ayuda,
}
