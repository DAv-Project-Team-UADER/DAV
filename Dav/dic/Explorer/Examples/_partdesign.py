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

"""PartDesign example: a hexagonal-head screw, built one operation at a time."""

import math

import Part
import Sketcher
from FreeCAD import Vector

from ._common import activeDoc, fitView, lastOfType

TITLE = {
    "es": "PartDesign: un tornillo paso a paso",
    "en": "PartDesign: a screw, step by step",
    "pt": "PartDesign: um parafuso passo a passo",
}

HEAD_RADIUS = 8.0  # radio circunscripto del hexágono
HEAD_HEIGHT = 5.0
SHANK_RADIUS = 4.0
SHANK_LENGTH = 25.0


def _body(doc):
    return lastOfType(doc, "PartDesign::Body")


def _sketchOnXY(doc):
    """Add a sketch to the body, attached to its XY plane."""
    body = _body(doc)
    plane = [item for item in body.Origin.OriginFeatures if item.Role == "XY_Plane"][0]
    sketch = body.newObject("Sketcher::SketchObject", "Sketch")
    sketch.AttachmentSupport = [(plane, "")]
    sketch.MapMode = "FlatFace"
    return sketch


def _newBody() -> None:
    doc = activeDoc()
    doc.addObject("PartDesign::Body", "Body")
    doc.recompute()
    fitView()


def _hexagon() -> None:
    doc = activeDoc()
    sketch = _sketchOnXY(doc)
    corners = [
        Vector(
            HEAD_RADIUS * math.cos(math.radians(60 * i)),
            HEAD_RADIUS * math.sin(math.radians(60 * i)),
            0,
        )
        for i in range(6)
    ]
    for index in range(6):
        sketch.addGeometry(Part.LineSegment(corners[index], corners[(index + 1) % 6]), False)
    for index in range(6):
        sketch.addConstraint(Sketcher.Constraint("Coincident", index, 2, (index + 1) % 6, 1))
    doc.recompute()
    fitView()


def _pad(length: float, reversed_: bool) -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    pad = _body(doc).newObject("PartDesign::Pad", "Pad")
    pad.Profile = sketch
    pad.Length = length
    pad.Reversed = reversed_
    sketch.Visibility = False
    doc.recompute()
    fitView()


def _padHead() -> None:
    _pad(HEAD_HEIGHT, False)


def _shankCircle() -> None:
    doc = activeDoc()
    sketch = _sketchOnXY(doc)
    sketch.addGeometry(Part.Circle(Vector(0, 0, 0), Vector(0, 0, 1), SHANK_RADIUS), False)
    doc.recompute()
    fitView()


def _padShank() -> None:
    # hacia abajo: el vástago queda debajo de la cabeza
    _pad(SHANK_LENGTH, True)


def _chamfer() -> None:
    doc = activeDoc()
    pad = lastOfType(doc, "PartDesign::Pad")
    tip = pad.Shape
    # el borde circular de la punta, a la profundidad del vástago
    edges = [
        f"Edge{index + 1}"
        for index, edge in enumerate(tip.Edges)
        if abs(edge.BoundBox.ZMin + SHANK_LENGTH) < 1e-6 and abs(edge.BoundBox.ZMax + SHANK_LENGTH) < 1e-6
    ]
    chamfer = _body(doc).newObject("PartDesign::Chamfer", "Chamfer")
    chamfer.Base = (pad, edges)
    chamfer.Size = 0.8
    doc.recompute()
    fitView()


def _thread() -> None:
    doc = activeDoc()
    body = _body(doc)
    plane = [item for item in body.Origin.OriginFeatures if item.Role == "XZ_Plane"][0]
    profile = body.newObject("Sketcher::SketchObject", "ThreadProfile")
    profile.AttachmentSupport = [(plane, "")]
    profile.MapMode = "FlatFace"
    # triángulo que se hunde en el vástago, cerca de la punta
    z = -SHANK_LENGTH + 2.0
    depth = SHANK_RADIUS - 0.8
    apex = Vector(SHANK_RADIUS, z, 0)
    lower = Vector(depth, z - 0.4, 0)
    upper = Vector(depth, z + 0.4, 0)
    profile.addGeometry(Part.LineSegment(apex, lower), False)
    profile.addGeometry(Part.LineSegment(lower, upper), False)
    profile.addGeometry(Part.LineSegment(upper, apex), False)
    doc.recompute()
    helix = body.newObject("PartDesign::SubtractiveHelix", "Thread")
    helix.Profile = profile
    helix.ReferenceAxis = (profile, ["V_Axis"])
    helix.Pitch = 1.5
    helix.Height = SHANK_LENGTH - 7.0
    profile.Visibility = False
    doc.recompute()
    fitView()


def steps() -> list:
    """Return the frames of the screw example."""
    from InputPrompts.ExampleStep import ExampleStep

    return [
        ExampleStep(
            Text={
                "es": "Creá un cuerpo: es el contenedor donde se arma la pieza.",
                "en": "Create a body: the container where the part is built.",
                "pt": "Crie um corpo: o contêiner onde a peça é montada.",
            },
            Say={"es": ("cuerpo",), "en": ("body",), "pt": ("corpo",)},
            Action=_newBody,
        ),
        ExampleStep(
            Text={
                "es": "Dibujá la cabeza: un hexágono sobre el plano base.",
                "en": "Draw the head: a hexagon on the base plane.",
                "pt": "Desenhe a cabeça: um hexágono no plano base.",
            },
            Say={"es": ("hexágono",), "en": ("hexagon",), "pt": ("hexágono",)},
            Action=_hexagon,
        ),
        ExampleStep(
            Text={
                "es": "Extruí el hexágono 5 mm hacia arriba: ya tenés la cabeza.",
                "en": "Extrude the hexagon 5 mm up: that is the head.",
                "pt": "Extrude o hexágono 5 mm para cima: essa é a cabeça.",
            },
            Say={"es": ("extruir",), "en": ("extrude",), "pt": ("extrudar",)},
            Action=_padHead,
        ),
        ExampleStep(
            Text={
                "es": "Dibujá el vástago: un círculo de 4 mm de radio.",
                "en": "Draw the shank: a circle with a 4 mm radius.",
                "pt": "Desenhe a haste: um círculo de 4 mm de raio.",
            },
            Say={"es": ("círculo",), "en": ("circle",), "pt": ("círculo",)},
            Action=_shankCircle,
        ),
        ExampleStep(
            Text={
                "es": "Extruí el círculo 25 mm hacia abajo.",
                "en": "Extrude the circle 25 mm down.",
                "pt": "Extrude o círculo 25 mm para baixo.",
            },
            Say={"es": ("extruir",), "en": ("extrude",), "pt": ("extrudar",)},
            Action=_padShank,
        ),
        ExampleStep(
            Text={
                "es": "Achaflaná la punta para que entre fácil.",
                "en": "Chamfer the tip so it goes in easily.",
                "pt": "Chanfre a ponta para que entre com facilidade.",
            },
            Say={"es": ("chaflán",), "en": ("chamfer",), "pt": ("chanfro",)},
            Action=_chamfer,
        ),
        ExampleStep(
            Text={
                "es": "Cortá la rosca con una hélice: ¡el tornillo está listo!",
                "en": "Cut the thread with a helix: the screw is ready!",
                "pt": "Corte a rosca com uma hélice: o parafuso está pronto!",
            },
            Say={"es": ("hélice",), "en": ("helix",), "pt": ("hélice",)},
            Action=_thread,
        ),
    ]
