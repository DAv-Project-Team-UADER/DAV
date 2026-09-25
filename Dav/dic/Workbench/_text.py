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

"""Flat text made by voice, shared by the Sketcher and Draft text commands.

Reemplaza al dialogo nativo de ``Draft_ShapeString`` (que pide texto, tamano y
fuente con teclado y mouse): el texto se deletrea, la altura y la posicion se
dicen, y se crea un ShapeString plano, sin extruir.
"""

from __future__ import annotations

import FreeCAD as App

_TITLE = "Texto"


def voiceShapeString() -> None:
    """Ask a text, its height and its position by voice and draw it flat.

    El texto se crea como ``Draft.make_shapestring`` sobre el plano XY, sin
    cambiar de banco de trabajo. Cancelar en cualquier pregunta no crea nada.

    Example::

        voiceShapeString()   # "hola" -> ShapeString de 10 mm en (0, 0)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return

    # imports diferidos: _prompts y engrave.py traen medio banco de Sketcher y
    # PartDesign al cargarse, y este modulo lo importan los dos bancos
    from ._prompts import askNumber, askText
    from .PartDesign.modify.engrave import _findFont

    fontFile = _findFont()
    if not fontFile:
        print("[DAV] Error: no se encontró una tipografía TrueType; elegí una en las preferencias de Draft.")
        return

    text = askText(_TITLE, "Deletreá el texto letra por letra")
    if text is None or not text.strip():
        print("[DAV] Texto cancelado.")
        return

    height = askNumber(_TITLE, "Decí la altura de las letras en mm")
    if height is None or height <= 0:
        print("[DAV] Texto cancelado: la altura tiene que ser mayor que cero.")
        return

    x = askNumber(_TITLE, "Decí la posición X en mm")
    if x is None:
        print("[DAV] Texto cancelado.")
        return

    y = askNumber(_TITLE, "Decí la posición Y en mm")
    if y is None:
        print("[DAV] Texto cancelado.")
        return

    import Draft

    from .DraftWork._parametric import _finish, _placement

    shape = Draft.make_shapestring(text, fontFile, height)
    shape.Placement = _placement(x, y)
    _finish(doc, shape, "texto")
