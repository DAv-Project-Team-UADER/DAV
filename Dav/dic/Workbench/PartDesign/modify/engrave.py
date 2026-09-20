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

"""Engrave or emboss a spelled text on a face or plane of a PartDesign solid.

Grabado / serigrafía por voz: se elige la cara o el plano de referencia con el
mismo selector de "nuevo boceto", se elige si el texto va en relieve o hundido,
se deletrea letra por letra y se dictan el tamaño y la profundidad. El texto se
dibuja en un boceto sobre la superficie y se extruye (Pad) o se vacía (Pocket).
"""

from __future__ import annotations

import math
import os

import FreeCAD as App
import Part

from ..._prompts import askChoice, askNumber, askText
from ...Sketcher.Geometry._sketch import shapeToSketchGeometry
from ...Sketcher.new_sketch._faces import findSolid, listPlanarFaces
from ...Sketcher.new_sketch.new_sketch import _ask_plane, _unique_sketch_name
from ..base.new_sketch import _activeBody, createSketchOnChoice

# (clave, texto que ve el usuario, palabras que lo eligen al decirlas)
_MODES = [
    ("emboss", "Relieve (sobresale)", ("relieve", "saliente", "relief", "emboss", "relevo")),
    ("engrave", "Perforación (hundido)",
     ("perforación", "hundido", "grabado", "engrave", "perfuração", "rebaixo")),
]

# Tipografías gruesas primero: con trazos finos el relieve queda frágil.
_FONT_CANDIDATES = (
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
)


def _findFont() -> str:
    """Return the path of a TrueType font to draw the text with, or ''.

    Looks first at the font chosen in FreeCAD's Draft preferences, then at
    common system fonts and finally at the font FreeCAD ships with TechDraw.
    """
    try:
        preferred = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft").GetString("FontFile", "")
    except Exception:
        preferred = ""
    bundled = os.path.join(
        App.getResourceDir(), "Mod", "TechDraw", "Resources", "fonts", "osifont-lgpl3fe.ttf"
    )
    for path in (preferred, *_FONT_CANDIDATES, bundled):
        if path and os.path.isfile(path):
            return path
    return ""


def _textGeometry(text: str, height: float, fontFile: str) -> list:
    """Return sketch geometry for ``text`` centred on the origin.

    Args:
        text: Text to draw.
        height: Height of the letters, in millimetres.
        fontFile: Path of the TrueType font.

    Returns:
        Sketch geometry (letter outlines, counters included); empty when the
        font produced nothing (e.g. the text is only spaces).
    """
    glyphs = Part.makeWireString(text, fontFile, height, 0)
    wires = [wire for glyph in glyphs for wire in glyph]
    if not wires:
        return []
    compound = Part.Compound(wires)
    center = compound.BoundBox.Center
    geometry = shapeToSketchGeometry(compound)
    # se centra en el origen del boceto, que queda en el centro de la cara
    for item in geometry:
        item.translate(App.Vector(-center.x, -center.y, 0))
    return geometry


def _orientUp(sketch) -> None:
    """Rotate the sketch about its normal so the text reads upright.

    Vertical faces put the top of the letters towards +Z; horizontal ones
    towards +Y. FreeCAD picks the sketch axes on its own, which would leave
    the text lying on its side on some faces.
    """
    rotation = sketch.Placement.Rotation
    normal = rotation.multVec(App.Vector(0, 0, 1))
    yAxis = rotation.multVec(App.Vector(0, 1, 0))
    up = App.Vector(0, 0, 1) if abs(normal.z) < 0.9 else App.Vector(0, 1, 0)
    up = up - normal * up.dot(normal)
    if up.Length < 1e-9:
        return
    up.normalize()
    angle = math.degrees(math.atan2(normal.dot(yAxis.cross(up)), yAxis.dot(up)))
    offset = sketch.AttachmentOffset
    sketch.AttachmentOffset = App.Placement(offset.Base, App.Rotation(App.Vector(0, 0, 1), angle))


# lados del sólido, con hacia dónde mira cada uno (mismas convenciones de vistas)
_SIDES = (
    ("superior", (0, 0, 1)),
    ("inferior", (0, 0, -1)),
    ("frontal", (0, -1, 0)),
    ("trasera", (0, 1, 0)),
    ("derecha", (1, 0, 0)),
    ("izquierda", (-1, 0, 0)),
)


def _tangentOptions(doc) -> dict:
    """Offer the six side planes of a solid that has no flat face (sphere, ellipsoid...).

    Cada opción es el plano tangente al sólido en su punto más extremo de ese
    lado; el texto se dibuja plano sobre ese polo. Tiene el mismo formato que
    ``listPlanarFaces`` más la marca ``tangent``.

    Args:
        doc: Active FreeCAD document.

    Returns:
        Ordered dict of options; empty when the document has no solid.
    """
    support, body = findSolid(doc)
    if support is None:
        return {}
    box = support.Shape.optimalBoundingBox(True, False)
    options = {}
    for name, direction in _SIDES:
        normal = App.Vector(*direction)
        # extremo del sólido en esa dirección, centrado en las otras dos
        point = box.Center + App.Vector(
            direction[0] * box.XLength / 2,
            direction[1] * box.YLength / 2,
            direction[2] * box.ZLength / 2,
        )
        extent = abs(normal.x) * box.XLength + abs(normal.y) * box.YLength + abs(normal.z) * box.ZLength
        options[f"Side{name.capitalize()}"] = {
            "label": f"Cara {name} (curva)",
            "tangent": True,
            "body": body,
            "point": point,
            "normal": normal,
            "extent": extent,
        }
    return options


def _tangentSketch(doc, option: dict, lift: float):
    """Create a free sketch on the tangent plane of ``option``, text upright.

    Args:
        doc: Active FreeCAD document.
        option: One value of :func:`_tangentOptions`.
        lift: Distance the plane is moved outwards, in millimetres (the height
            of a relief, so its top ends up that far above the surface).

    Returns:
        ``(sketch, body)``.
    """
    body = option["body"] or _activeBody(doc)
    normal = option["normal"]
    up = App.Vector(0, 0, 1) if abs(normal.z) < 0.9 else App.Vector(0, 1, 0)
    yAxis = up - normal * up.dot(normal)
    yAxis.normalize()
    xAxis = yAxis.cross(normal)

    sketch = body.newObject("Sketcher::SketchObject", _unique_sketch_name(doc))
    sketch.MapMode = "Deactivated"
    sketch.Placement = App.Placement(
        option["point"] + normal * lift, App.Rotation(xAxis, yAxis, normal, "ZXY")
    )
    return sketch, body


def _buildFeature(doc, body, sketch, emboss: bool, length: float, reverse: bool = False):
    """Pad (relief) or pocket (engraving) the text sketch; None if it changed nothing.

    Args:
        doc: Active FreeCAD document.
        body: Body that receives the feature.
        sketch: Sketch with the text outlines.
        emboss: True for a pad (relief), False for a pocket (engraving).
        length: Extrusion length, in millimetres.
        reverse: Start with the direction flipped; it is flipped again if the
            solid did not change.
    """
    feature = body.newObject(
        "PartDesign::Pad" if emboss else "PartDesign::Pocket",
        "TextRelief" if emboss else "TextEngraving",
    )
    feature.Profile = sketch
    feature.Type = 0  # 0 = Length
    feature.Length = length
    feature.Reversed = reverse

    before = body.Shape.Volume
    doc.recompute()
    if abs(body.Shape.Volume - before) < 1e-6:
        # el sentido depende de cómo quedó orientada la superficie: se prueba al revés
        feature.Reversed = not reverse
        doc.recompute()
    if abs(body.Shape.Volume - before) < 1e-6 or "Invalid" in feature.State:
        doc.removeObject(feature.Name)
        doc.recompute()
        return None
    return feature


def engraveTextOn(
    doc, choice: str, faces: dict, text: str, height: float, depth: float, emboss: bool
) -> bool:
    """Draw ``text`` on the chosen face or plane and raise or sink it.

    Args:
        doc: Active FreeCAD document.
        choice: Plane key (``"XY"``, ``"XZ"``, ``"YZ"``) or a key of ``faces``.
        faces: Planar faces offered by ``listPlanarFaces``.
        text: Text to write.
        height: Height of the letters, in millimetres.
        depth: Relief height or engraving depth, in millimetres.
        emboss: True for relief (raised), False to sink it into the solid.

    Returns:
        True when the text was added to the solid.

    Example::

        engraveTextOn(doc, "Face11", faces, "DAV", 6, 1, emboss=True)
    """
    if height <= 0 or depth <= 0:
        print("[modify] Error: the letter height and the depth must be greater than zero.")
        return False
    fontFile = _findFont()
    if not fontFile:
        print("[modify] Error: no TrueType font found; choose one in Draft preferences.")
        return False

    option = faces.get(choice, {})
    tangent = bool(option.get("tangent"))
    if tangent:
        # el relieve arranca `depth` por encima del polo; el texto queda plano
        sketch, body = _tangentSketch(doc, option, depth if emboss else 0.0)
        where = f"la {option['label'].lower()}"
    else:
        created = createSketchOnChoice(doc, choice, faces)
        if created is None:
            return False
        sketch, body, where = created
    geometry = _textGeometry(text, height, fontFile)
    if not geometry:
        doc.removeObject(sketch.Name)
        print("[modify] Error: the text has no visible letters.")
        return False

    sketch.addGeometry(geometry, False)
    doc.recompute()
    if not tangent:
        _orientUp(sketch)
        doc.recompute()

    length, reverse = depth, False
    if tangent and emboss:
        # el relieve se apoya en el polo y se hunde hacia el sólido: como la
        # superficie cae hacia los bordes del texto, se alarga para que llegue
        # siempre a material y quede fusionado
        margin = min(sketch.Shape.BoundBox.DiagonalLength / 2, option["extent"] / 2)
        length, reverse = depth + margin, True

    feature = _buildFeature(doc, body, sketch, emboss, length, reverse)
    if feature is None:
        print(f"[modify] Error: the text did not change the solid on {where}; check the size and depth.")
        return False
    sketch.Visibility = False
    print(f"[modify] {'Relief' if emboss else 'Engraved'} text '{text}' on {where}")
    return True


def engraveText() -> None:
    """Engrave or emboss a text, everything chosen and dictated by voice.

    Steps: choose the plane or face (same selector as a new sketch), choose
    relief or perforation, spell the text letter by letter ("espacio" for a
    space) and dictate the letter height and the depth.

    Example::

        engraveText()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[modify] Error: no active document.")
        return
    faces = listPlanarFaces(doc)
    if not faces:
        # sin caras planas (esfera, elipsoide...) se ofrecen los planos tangentes
        faces = _tangentOptions(doc)
    if not faces:
        print("[modify] Error: create a solid first; there is nothing to engrave on.")
        return

    result = _ask_plane(faces)
    if result is None or result.Cancelled or not result.Value:
        print("[modify] Engraving cancelled.")
        return
    choice = str(result.Value)

    mode = askChoice("Grabar texto", "¿Relieve o perforación? Decilo, o arriba/abajo y okey", _MODES)
    if mode is None:
        print("[modify] Engraving cancelled.")
        return
    emboss = mode == "emboss"

    text = askText("Grabar texto", "Deletreá el texto letra por letra")
    if text is None:
        print("[modify] Engraving cancelled.")
        return

    height = askNumber("Grabar texto", "Decí la altura de las letras en mm")
    if height is None:
        print("[modify] Engraving cancelled.")
        return
    depth = askNumber(
        "Grabar texto",
        "Decí el alto del relieve en mm" if emboss else "Decí la profundidad en mm",
    )
    if depth is None:
        print("[modify] Engraving cancelled.")
        return

    engraveTextOn(doc, choice, faces, text, height, depth, emboss)
