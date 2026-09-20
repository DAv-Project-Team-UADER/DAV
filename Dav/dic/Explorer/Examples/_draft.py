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

"""Draft example: 2D shapes, an annotation and a copy."""

from FreeCAD import Placement, Rotation, Vector

from ._common import activeDoc, fitView

TITLE = {
    "es": "Draft: dibujo 2D directo",
    "en": "Draft: direct 2D drawing",
    "pt": "Draft: desenho 2D direto",
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


def _line() -> None:
    import Draft

    doc = activeDoc()
    Draft.make_line(Vector(0, 0, 0), Vector(60, 40, 0))
    doc.recompute()
    fitView()


def _text() -> None:
    import Draft

    doc = activeDoc()
    Draft.make_text(["DAV"], Vector(2, 44, 0))
    doc.recompute()
    fitView()


def _copy() -> None:
    import Draft

    doc = activeDoc()
    shapes = [obj for obj in doc.Objects if obj.Name.startswith(("Rectangle", "Circle", "Line"))]
    Draft.move(shapes, Vector(80, 0, 0), copy=True)
    doc.recompute()
    fitView()


def steps() -> list:
    """Return the frames of the Draft example."""
    from InputPrompts.ExampleStep import ExampleStep

    return [
        ExampleStep(
            Text={
                "es": "Dibujá un rectángulo de 60 x 40.",
                "en": "Draw a 60 x 40 rectangle.",
                "pt": "Desenhe um retângulo de 60 x 40.",
            },
            Say={"es": ("rectángulo",), "en": ("rectangle",), "pt": ("retângulo",)},
            Action=_rectangle,
        ),
        ExampleStep(
            Text={
                "es": "Agregá un círculo en el centro.",
                "en": "Add a circle in the middle.",
                "pt": "Adicione um círculo no centro.",
            },
            Say={"es": ("círculo",), "en": ("circle",), "pt": ("círculo",)},
            Action=_circle,
        ),
        ExampleStep(
            Text={
                "es": "Trazá una línea diagonal de esquina a esquina.",
                "en": "Draw a diagonal line from corner to corner.",
                "pt": "Trace uma linha diagonal de canto a canto.",
            },
            Say={"es": ("línea",), "en": ("line",), "pt": ("linha",)},
            Action=_line,
        ),
        ExampleStep(
            Text={
                "es": "Anotá el dibujo con un texto.",
                "en": "Annotate the drawing with a text.",
                "pt": "Anote o desenho com um texto.",
            },
            Say={"es": ("texto",), "en": ("text",), "pt": ("texto",)},
            Action=_text,
        ),
        ExampleStep(
            Text={
                "es": "Modificá: copiá todo el dibujo a la derecha.",
                "en": "Modify: copy the whole drawing to the right.",
                "pt": "Modifique: copie todo o desenho para a direita.",
            },
            Say={"es": ("copiar",), "en": ("copy",), "pt": ("copiar",)},
            Action=_copy,
        ),
    ]
