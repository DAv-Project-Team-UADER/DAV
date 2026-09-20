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

"""Sketcher example: a rectangle with geometric and dimensional constraints."""

import Part
import Sketcher
from FreeCAD import Vector

from ._common import activeDoc, fitView, lastOfType

TITLE = {
    "es": "Sketcher: un boceto con restricciones",
    "en": "Sketcher: a constrained sketch",
    "pt": "Sketcher: um esboço com restrições",
}

WIDTH = 60
HEIGHT = 40


def _newSketch() -> None:
    doc = activeDoc()
    doc.addObject("Sketcher::SketchObject", "Sketch")
    doc.recompute()
    fitView()


def _rectangle() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    corners = [Vector(0, 0, 0), Vector(WIDTH, 0, 0), Vector(WIDTH, HEIGHT, 0), Vector(0, HEIGHT, 0)]
    for index in range(4):
        sketch.addGeometry(Part.LineSegment(corners[index], corners[(index + 1) % 4]), False)
    for index in range(4):
        # el final de cada línea coincide con el inicio de la siguiente
        sketch.addConstraint(Sketcher.Constraint("Coincident", index, 2, (index + 1) % 4, 1))
    doc.recompute()
    fitView()


def _orientation() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    for line in (0, 2):
        sketch.addConstraint(Sketcher.Constraint("Horizontal", line))
    for line in (1, 3):
        sketch.addConstraint(Sketcher.Constraint("Vertical", line))
    doc.recompute()


def _dimensions() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    sketch.addConstraint(Sketcher.Constraint("DistanceX", 0, 1, 0, 2, WIDTH))
    sketch.addConstraint(Sketcher.Constraint("DistanceY", 1, 1, 1, 2, HEIGHT))
    doc.recompute()
    fitView()


def _origin() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    # esquina del rectángulo sobre el origen del boceto (-1 es el origen)
    sketch.addConstraint(Sketcher.Constraint("Coincident", 0, 1, -1, 1))
    doc.recompute()
    fitView()


def steps() -> list:
    """Return the frames of the Sketcher example."""
    from InputPrompts.ExampleStep import ExampleStep

    return [
        ExampleStep(
            Text={
                "es": "Creá un boceto nuevo sobre el plano base.",
                "en": "Create a new sketch on the base plane.",
                "pt": "Crie um esboço novo no plano base.",
            },
            Say={"es": ("nuevo boceto",), "en": ("new sketch",), "pt": ("novo esboço",)},
            Action=_newSketch,
        ),
        ExampleStep(
            Text={
                "es": "Dibujá un rectángulo: son cuatro líneas unidas por sus extremos.",
                "en": "Draw a rectangle: four lines joined at their ends.",
                "pt": "Desenhe um retângulo: quatro linhas unidas pelas pontas.",
            },
            Say={"es": ("rectángulo",), "en": ("rectangle",), "pt": ("retângulo",)},
            Action=_rectangle,
        ),
        ExampleStep(
            Text={
                "es": "Restringí la orientación: lados horizontales y lados verticales.",
                "en": "Constrain the orientation: horizontal sides and vertical sides.",
                "pt": "Restrinja a orientação: lados horizontais e verticais.",
            },
            Say={
                "es": ("horizontal", "vertical"),
                "en": ("horizontal", "vertical"),
                "pt": ("horizontal", "vertical"),
            },
            Action=_orientation,
        ),
        ExampleStep(
            Text={
                "es": "Dale medidas: 60 mm de ancho y 40 mm de alto.",
                "en": "Give it dimensions: 60 mm wide and 40 mm high.",
                "pt": "Dê medidas: 60 mm de largura e 40 mm de altura.",
            },
            Say={
                "es": ("ancho", "alto"),
                "en": ("width", "height"),
                "pt": ("largura", "altura"),
            },
            Action=_dimensions,
        ),
        ExampleStep(
            Text={
                "es": "Fijá una esquina al origen: el boceto queda totalmente restringido.",
                "en": "Pin a corner to the origin: the sketch becomes fully constrained.",
                "pt": "Fixe um canto na origem: o esboço fica totalmente restrito.",
            },
            Say={"es": ("origen",), "en": ("origin",), "pt": ("origem",)},
            Action=_origin,
        ),
    ]
