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
# SPDX-License-Identifier: GPL-3.0-or-later

"""Build a stepped shaft by voice: each section is dictated as length and diameter."""

import FreeCAD as App

from ..._prompts import askNumber

_MAX_SECTIONS = 12


def _askSections() -> list | None:
    """Ask how many sections the shaft has, then each one's length and diameter.

    Returns:
        A list of ``(length, diameter)`` in mm, or None when cancelled or invalid.
    """
    title = "Generador de ejes"
    count = askNumber(title, f"Decí cuántos tramos tiene el eje (1 a {_MAX_SECTIONS})")
    if count is None:
        return None
    count = int(count)
    if not 1 <= count <= _MAX_SECTIONS:
        print(f"[DAV] Error: la cantidad de tramos debe estar entre 1 y {_MAX_SECTIONS} (dijiste {count}).")
        return None
    sections = []
    for number in range(1, count + 1):
        length = askNumber(title, f"Tramo {number} de {count}: decí el largo en mm")
        if length is None:
            return None
        diameter = askNumber(title, f"Tramo {number} de {count}: decí el diámetro en mm")
        if diameter is None:
            return None
        if length <= 0 or diameter <= 0:
            print(f"[DAV] Error: el largo y el diámetro del tramo {number} deben ser mayores que cero.")
            return None
        sections.append((float(length), float(diameter)))
    return sections


def _profilePoints(sections: list) -> list:
    """Closed outline (x = radius, y = position along the axis) of the shaft, axis included."""
    points = [(0.0, 0.0)]
    position = 0.0
    for length, diameter in sections:
        radius = diameter / 2.0
        points.append((radius, position))
        position += length
        points.append((radius, position))
    points.append((0.0, position))
    return points


def wizardShaft() -> None:
    """Create a stepped shaft by voice (sections of length and diameter), along the Z axis.

    Pregunta la cantidad de tramos y, de cada uno, el largo y el diámetro. Dibuja el
    perfil en un croquis sobre el plano XZ y lo revoluciona 360° sobre el eje del croquis.
    Ya no abre el asistente nativo de FreeCAD, que no se maneja por voz.

    Example::

        wizardShaft()
    """
    import Part
    import Sketcher

    from ..additive._parametric import _revolveProfile

    doc = App.activeDocument()
    if doc is None:
        doc = App.newDocument()
    sections = _askSections()
    if sections is None:
        print("[DAV] Generador de ejes cancelado.")
        return

    body = doc.addObject("PartDesign::Body", "Eje")
    try:
        import FreeCADGui as Gui

        Gui.activeView().setActiveObject("pdbody", body)
    except Exception:
        pass
    plane = next((f for f in body.Origin.OriginFeatures if f.Role == "XZ_Plane"), None)
    sketch = body.newObject("Sketcher::SketchObject", "PerfilEje")
    support = "AttachmentSupport" if hasattr(sketch, "AttachmentSupport") else "Support"
    setattr(sketch, support, [(plane, "")])
    sketch.MapMode = "FlatFace"

    points = _profilePoints(sections)
    count = len(points)
    for index in range(count):
        start, end = points[index], points[(index + 1) % count]
        sketch.addGeometry(Part.LineSegment(App.Vector(start[0], start[1], 0), App.Vector(end[0], end[1], 0)), False)
    for index in range(count):
        sketch.addConstraint(Sketcher.Constraint("Coincident", index, 2, (index + 1) % count, 1))
    doc.recompute()

    if _revolveProfile(doc, sketch, 360.0) is None:
        doc.removeObject(sketch.Name)
        doc.removeObject(body.Name)
        doc.recompute()
        return
    total = sum(length for length, _ in sections)
    print(f"[DAV] Eje de {len(sections)} tramo/s y {total:g} mm de largo, sobre el eje Z.")
