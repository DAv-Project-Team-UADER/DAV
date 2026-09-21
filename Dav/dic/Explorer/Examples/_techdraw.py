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

"""TechDraw example: a circle on a page with its title block."""

import os

import FreeCAD as App
from FreeCAD import Vector

from ._common import activeDoc, fitView, lastOfType
from ._words import numbers

TITLE = {
    "es": "TechDraw: un círculo con su rótulo",
    "en": "TechDraw: a circle with its title block",
    "pt": "TechDraw: um círculo com seu carimbo",
}

# plantilla A4 apaisada con rótulo (la que trae FreeCAD)
_TEMPLATE = os.path.join("Mod", "TechDraw", "Templates", "ISO", "A4_Landscape_TD.svg")

# campos del rótulo por idioma: (título, subtítulo, dibujó)
_TITLE_BLOCK = {
    "es": ("Círculo", "Ejemplo de DAV", "Diseño Asistido por Voz"),
    "en": ("Circle", "DAV example", "Voice-Assisted Design"),
    "pt": ("Círculo", "Exemplo do DAV", "Design Assistido por Voz"),
}


def _circle() -> None:
    doc = activeDoc()
    circle = doc.addObject("Part::Circle", "Circle")
    circle.Radius = 20
    doc.recompute()
    fitView()


def _page() -> None:
    doc = activeDoc()
    page = doc.addObject("TechDraw::DrawPage", "Page")
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    template.Template = os.path.join(App.getResourceDir(), _TEMPLATE)
    page.Template = template
    doc.recompute()
    try:
        # abre la hoja en su propia pestaña
        page.ViewObject.doubleClicked()
    except Exception:
        pass


def _view() -> None:
    doc = activeDoc()
    circle = doc.getObject("Circle")
    if circle is None:
        raise RuntimeError("Falta el círculo: seguí los cuadros en orden.")
    page = lastOfType(doc, "TechDraw::DrawPage")
    view = doc.addObject("TechDraw::DrawViewPart", "View")
    page.addView(view)
    view.Source = [circle]
    # vista desde arriba: el círculo se ve sin deformar
    view.Direction = Vector(0, 0, 1)
    view.XDirection = Vector(1, 0, 0)
    view.X = 148
    view.Y = 105
    doc.recompute()


def _titleBlock() -> None:
    from InputPrompts.InputPromptI18n import ResolveLanguage

    doc = activeDoc()
    template = lastOfType(doc, "TechDraw::DrawSVGTemplate")
    title, subtitle, author = _TITLE_BLOCK.get(ResolveLanguage(), _TITLE_BLOCK["es"])
    template.setEditFieldContent("FC-Title", title)
    template.setEditFieldContent("Subtitle", subtitle)
    template.setEditFieldContent("Designed_by_Name", author)
    template.setEditFieldContent("Drawing_number", "DAV-001")
    doc.recompute()


def steps() -> list:
    """Return the frames of the TechDraw example."""
    from InputPrompts.ExampleStep import ExampleStep

    return [
        ExampleStep(
            Text={
                "es": "Creá la pieza a dibujar: un círculo en el origen (0, 0, 0) de radio 20.",
                "en": "Create the part to draw: a circle at the origin (0, 0, 0) with radius 20.",
                "pt": "Crie a peça a desenhar: um círculo na origem (0, 0, 0) com raio 20.",
            },
            Path={
                "es": ("banco", "pieza", "circulo"),
                "en": ("workbench", "part", "circle"),
                "pt": ("trabalho", "peca", "circulo"),
            },
            Values=lambda language: numbers(language, 0, 0, 0, 20),
            Action=_circle,
        ),
        ExampleStep(
            Text={
                "es": "Creá una página técnica nueva.",
                "en": "Create a new technical page.",
                "pt": "Crie uma página técnica nova.",
            },
            Path={
                "es": ("dibujo tecnico", "pagina", "pagina"),
                "en": ("drawing", "page", "new page"),
                "pt": ("tecnico", "pagina", "pagina"),
            },
            Action=_page,
        ),
        ExampleStep(
            Text={
                "es": "Poné una vista del círculo en la página (con el círculo seleccionado).",
                "en": "Place a view of the circle on the page (with the circle selected).",
                "pt": "Coloque uma vista do círculo na página (com o círculo selecionado).",
            },
            Path={
                "es": ("vistas", "vista"),
                "en": ("views", "view"),
                "pt": ("vistas", "vista"),
            },
            Action=_view,
        ),
        ExampleStep(
            Text={
                "es": "Completá el rótulo: título, subtítulo, autor y número de plano.",
                "en": "Fill in the title block: title, subtitle, author and drawing number.",
                "pt": "Preencha o carimbo: título, subtítulo, autor e número do desenho.",
            },
            Path={
                "es": ("elementos", "campos"),
                "en": ("features", "fields"),
                "pt": ("recursos", "campos"),
            },
            Action=_titleBlock,
        ),
    ]
