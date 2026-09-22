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

"""Sketcher example: a circle with a radius constraint and a 2D dimension."""

import Part
import Sketcher
from FreeCAD import Vector

from ._common import activeDoc, fitView, lastOfType
from ._words import numbers, send

TITLE = {
    "es": "Croquis: un círculo con restricción y cota",
    "en": "Sketcher: a circle with a constraint and a dimension",
    "pt": "Croqui: um círculo com restrição e cota",
}

RADIUS = 12


def _newSketch() -> None:
    doc = activeDoc()
    doc.addObject("Sketcher::SketchObject", "Sketch")
    doc.recompute()
    fitView()


def _circle() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    sketch.addGeometry(Part.Circle(Vector(0, 0, 0), Vector(0, 0, 1), RADIUS), False)
    doc.recompute()
    fitView()


def _radius() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    sketch.addConstraint(Sketcher.Constraint("Radius", 0, RADIUS))
    doc.recompute()


def _dimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario
    from measure import _dimension2d

    _dimension2d(0, 0, RADIUS, 0)
    activeDoc().recompute()
    fitView()


def _close() -> None:
    fitView()


def steps() -> list:
    """Return the frames of the Sketcher example."""
    from InputPrompts.ExampleStep import ExampleStep

    def values(*items):
        return lambda language: numbers(language, *items)

    return [
        ExampleStep(
            Text={
                "es": "Abrí un croquis nuevo en el plano base (XY es el primero de la lista: «enviar» lo elige).",
                "en": "Open a new sketch on the base plane (XY is first in the list: “send” picks it).",
                "pt": "Abra um croqui novo no plano base (XY é o primeiro da lista: «enviar» o escolhe).",
            },
            Path={
                "es": ("banco", "croquis", "nuevo"),
                "en": ("workbench", "sketcher", "new"),
                "pt": ("trabalho", "croqui", "novo"),
            },
            Values=lambda language: send(language),
            Action=_newSketch,
        ),
        ExampleStep(
            Text={
                "es": "Dibujá un círculo: centro en 0, 0 y radio 12. Cada valor se confirma con «enviar».",
                "en": "Draw a circle: centre at 0, 0 and radius 12. Each value is confirmed with “send”.",
                "pt": "Desenhe um círculo: centro em 0, 0 e raio 12. Cada valor se confirma com «enviar».",
            },
            Path={
                "es": ("geometría", "círculo", "círculo"),
                "en": ("geometry", "circle", "circle"),
                "pt": ("geometria", "círculo", "círculo"),
            },
            Values=values(0, 0, RADIUS),
            Action=_circle,
        ),
        ExampleStep(
            Text={
                "es": "Fijá el radio con una restricción: 12 mm.",
                "en": "Fix the radius with a constraint: 12 mm.",
                "pt": "Fixe o raio com uma restrição: 12 mm.",
            },
            Path={
                "es": ("restricciones", "radio"),
                "en": ("constraints", "radius"),
                "pt": ("restrições", "raio"),
            },
            Values=values(RADIUS),
            Action=_radius,
        ),
        ExampleStep(
            Text={
                "es": "Acotá el círculo en 2D: de su centro (0, 0) a su borde (12, 0). Primero «subir» a Croquis (en Restricciones, «cota» es otra cosa). «cota» pide 4 valores: X e Y de cada punto.",
                "en": "Dimension the circle in 2D: from its centre (0, 0) to its edge (12, 0). First go “up” to Sketcher. “measure” asks for 4 values: X and Y of each point.",
                "pt": "Cote o círculo em 2D: do centro (0, 0) à borda (12, 0). Primeiro «subir» ao Croqui. «medir» pede 4 valores: X e Y de cada ponto.",
            },
            Path={
                "es": ("subir", "cota"),
                "en": ("up", "measure"),
                "pt": ("subir", "medir"),
            },
            Values=values(0, 0, RADIUS, 0),
            Action=_dimension,
        ),
        ExampleStep(
            Text={
                "es": "Cerrá el croquis.",
                "en": "Close the sketch.",
                "pt": "Feche o croqui.",
            },
            Path={
                "es": ("cerrar croquis",),
                "en": ("close sketch",),
                "pt": ("fechar croqui",),
            },
            Action=_close,
        ),
    ]
