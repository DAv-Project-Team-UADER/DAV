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

"""Draft example: a rectangle, a circle, a polygon and a 2D dimension."""

from FreeCAD import Placement, Rotation, Vector

from ._common import activeDoc, fitView
from ._words import numbers

TITLE = {
    "es": "Draft: dibujo 2D con medidas",
    "en": "Draft: 2D drawing with dimensions",
    "pt": "Draft: desenho 2D com medidas",
}


def _rectangle() -> None:
    import Draft

    doc = activeDoc()
    Draft.make_rectangle(60, 40)
    doc.recompute()
    fitView()


def _circle() -> None:
    import Draft

    doc = activeDoc()
    Draft.make_circle(10, placement=Placement(Vector(30, 20, 0), Rotation()))
    doc.recompute()
    fitView()


def _polygon() -> None:
    import Draft

    doc = activeDoc()
    Draft.make_polygon(6, radius=5, placement=Placement(Vector(30, 20, 0), Rotation()))
    doc.recompute()
    fitView()


def _dimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario
    from measure import _dimension2d

    _dimension2d(0, 0, 60, 0)
    activeDoc().recompute()
    fitView()


def steps() -> list:
    """Return the frames of the Draft example."""
    from InputPrompts.ExampleStep import ExampleStep

    def values(*items):
        return lambda language: numbers(language, *items)

    return [
        ExampleStep(
            Text={
                "es": "Dibujá un rectángulo por sus esquinas: de (0, 0) a (60, 40).",
                "en": "Draw a rectangle by its corners: from (0, 0) to (60, 40).",
                "pt": "Desenhe um retângulo pelos cantos: de (0, 0) a (60, 40).",
            },
            Path={
                "es": ("banco", "borrador", "crear", "rectangulo"),
                "en": ("workbench", "draft", "create", "rectangle"),
                "pt": ("trabalho", "draft", "criar", "retangulo"),
            },
            Values=values(0, 0, 60, 40),
            Action=_rectangle,
        ),
        ExampleStep(
            Text={
                "es": "Agregá un círculo: centro en (30, 20) y radio 10.",
                "en": "Add a circle: centre at (30, 20) and radius 10.",
                "pt": "Adicione um círculo: centro em (30, 20) e raio 10.",
            },
            Path={
                "es": ("circulo", "circulo"),
                "en": ("circle", "circle"),
                "pt": ("circulo", "circulo"),
            },
            Values=values(30, 20, 10),
            Action=_circle,
        ),
        ExampleStep(
            Text={
                "es": "Dentro del círculo, un polígono de 6 lados: centro (30, 20) y radio 5. Primero «subir» un nivel, para volver a Borrador.",
                "en": "Inside the circle, a 6-sided polygon: centre (30, 20) and radius 5. First go “up” one level, back to Draft.",
                "pt": "Dentro do círculo, um polígono de 6 lados: centro (30, 20) e raio 5. Primeiro «subir» um nível, de volta ao Draft.",
            },
            Path={
                "es": ("subir", "crear", "poligono"),
                "en": ("up", "create", "polygon"),
                "pt": ("subir", "criar", "poligono"),
            },
            Values=values(30, 20, 6, 5),
            Action=_polygon,
        ),
        ExampleStep(
            Text={
                "es": "Acotá el ancho del rectángulo en 2D: de (0, 0) a (60, 0). «cota» pide 4 valores: X e Y de cada punto.",
                "en": "Dimension the width of the rectangle in 2D: from (0, 0) to (60, 0). “measure” asks for 4 values: X and Y of each point.",
                "pt": "Cote a largura do retângulo em 2D: de (0, 0) a (60, 0). «medir» pede 4 valores: X e Y de cada ponto.",
            },
            Path={"es": ("cota",), "en": ("measure",), "pt": ("medir",)},
            Values=values(0, 0, 60, 0),
            Action=_dimension,
        ),
    ]
