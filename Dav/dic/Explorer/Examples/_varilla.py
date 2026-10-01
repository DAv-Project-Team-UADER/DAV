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

"""Assembly example: an M30 threaded rod with two nuts that turn along its thread (screw joint)."""

import Part
import Sketcher
from FreeCAD import Vector

from ._bulontuerca import _assemblyHelpers, _connectors, _link as _boltLink, _pick, _pickBody
from ._common import activeDoc, attachAt, fitView, lastOfType, setView
from ._words import down, nextItem, no, numbers, send, yes

TITLE = {
    "es": "Varilla roscada M30 con tuercas",
    "en": "M30 threaded rod with nuts",
    "pt": "Barra roscada M30 com porcas",
}

# Rosca métrica M30 de paso grueso (ISO 261): paso 3,5 mm y diámetro mayor 30 mm. El eje va por Z.
PITCH = 3.5
MAJOR_RADIUS = 15  # cresta de la rosca
CORE_RADIUS = 13  # núcleo del vástago, un poco menos que el diámetro menor (26,2 mm)
ROD_LENGTH = 100
THREAD_START = 2  # altura donde empieza la hélice
THREAD_HEIGHT = 96  # 27 vueltas, hasta z = 98

# Perfil de la rosca (triángulo de 60° incluidos) en el plano XZ: la base se hunde en el núcleo
# para que la hélice quede fundida con él y la cresta llega a 15.
PROFILE = ((12.5, 0.6), (12.5, 3.4), (15, 2))

# Tuerca hexagonal M30 (DIN 934): 46 mm entre caras (radio circunscrito 26,5) y 24 mm de alto.
# Se dibuja aparte, con su eje en x = 50, y el ensamblaje la lleva al eje de la varilla.
NUT_RADIUS = 26.5
NUT_HEIGHT = 24
NUT_X = 50
NUT_CENTER_Z = NUT_HEIGHT // 2
HOLE_HEIGHT = 30

# la segunda tuerca se aprieta contra la primera: sus caras quedan a esta distancia
LOCK_GAP = 0

# la tuerca se gira esta cantidad de grados y avanza lo que le toca al paso
TURN_DEGREES = 360


def _bodies() -> list:
    return [obj for obj in activeDoc().Objects if obj.TypeId == "PartDesign::Body"]


def _links() -> list:
    """The assembly links in the order they were inserted: the rod, the first nut and the second nut."""
    return [obj for obj in activeDoc().Objects if obj.TypeId == "App::Link"]


def _rod() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    core = doc.addObject("PartDesign::AdditiveCylinder", "Core")
    core.Radius = CORE_RADIUS
    core.Height = ROD_LENGTH
    body.addObject(core)
    # el cilindro nace con su base en el origen: el centro dictado (0, 0, 50) queda a media altura
    attachAt(body, core, 0, 0, 0)
    doc.recompute()
    fitView()


def _threadSketch() -> None:
    doc = activeDoc()
    body = _bodies()[0]
    plane = next(item for item in body.Origin.OriginFeatures if item.Role == "XZ_Plane")
    sketch = body.newObject("Sketcher::SketchObject", "ThreadProfile")
    sketch.AttachmentSupport = [(plane, "")]
    sketch.MapMode = "FlatFace"
    doc.recompute()
    fitView()


def _threadProfile() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    corners = [Vector(x, z, 0) for x, z in PROFILE]
    for index in range(3):
        sketch.addGeometry(Part.LineSegment(corners[index], corners[(index + 1) % 3]), False)
    for index in range(3):
        sketch.addConstraint(Sketcher.Constraint("Coincident", index, 2, (index + 1) % 3, 1))
    doc.recompute()
    fitView()


def _thread() -> None:
    doc = activeDoc()
    body = _bodies()[0]
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    helix = body.newObject("PartDesign::AdditiveHelix", "Thread")
    helix.Profile = sketch
    helix.ReferenceAxis = (sketch, ["V_Axis"])
    helix.Mode = "pitch-height-angle"
    helix.Pitch = PITCH
    helix.Height = THREAD_HEIGHT
    sketch.Visibility = False
    doc.recompute()
    if not helix.isValid():
        raise RuntimeError("No se pudo hacer la rosca: seguí los cuadros en orden.")
    fitView()


def _dimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario (3D: hay un sólido)
    from measure import _dimension3d

    _dimension3d(MAJOR_RADIUS, 0, THREAD_START, MAJOR_RADIUS, 0, THREAD_START + PITCH)
    activeDoc().recompute()
    fitView()


def _nut() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    prism = doc.addObject("PartDesign::AdditivePrism", "Nut")
    prism.Polygon = 6
    prism.Circumradius = NUT_RADIUS
    prism.Height = NUT_HEIGHT
    body.addObject(prism)
    attachAt(body, prism, NUT_X, 0, NUT_CENTER_Z - NUT_HEIGHT / 2)
    doc.recompute()
    fitView()


def _nutHole() -> None:
    doc = activeDoc()
    body = _bodies()[1]
    hole = doc.addObject("PartDesign::SubtractiveCylinder", "NutHole")
    hole.Radius = MAJOR_RADIUS
    hole.Height = HOLE_HEIGHT
    body.addObject(hole)
    attachAt(body, hole, NUT_X, 0, NUT_CENTER_Z - HOLE_HEIGHT / 2)
    doc.recompute()
    fitView()


def _createAssembly() -> None:
    doc = activeDoc()
    assembly = doc.addObject("Assembly::AssemblyObject", "Assembly")
    assembly.Type = "Assembly"
    assembly.newObject("Assembly::JointGroup", "Joints")
    doc.recompute()
    fitView()


def _insertLink(position: int):
    def action() -> None:
        doc = activeDoc()
        assembly = lastOfType(doc, "Assembly::AssemblyObject")
        _assemblyHelpers()._InsertLink(doc, assembly, _bodies()[position])
        fitView()

    return action
