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
    circle.Radius = 25
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
                "es": "Creá la pieza a dibujar: un círculo de 25 mm de radio.",
                "en": "Create the part to draw: a circle with a 25 mm radius.",
                "pt": "Crie a peça a desenhar: um círculo de 25 mm de raio.",
            },
            Say={"es": ("círculo",), "en": ("circle",), "pt": ("círculo",)},
            Action=_circle,
        ),
        ExampleStep(
            Text={
                "es": "Creá una hoja técnica A4 con rótulo.",
                "en": "Create an A4 technical sheet with a title block.",
                "pt": "Crie uma folha técnica A4 com carimbo.",
            },
            Say={"es": ("nueva página",), "en": ("new page",), "pt": ("nova página",)},
            Action=_page,
        ),
        ExampleStep(
            Text={
                "es": "Poné una vista del círculo sobre la hoja.",
                "en": "Place a view of the circle on the sheet.",
                "pt": "Coloque uma vista do círculo na folha.",
            },
            Say={"es": ("vista",), "en": ("view",), "pt": ("vista",)},
            Action=_view,
        ),
        ExampleStep(
            Text={
                "es": "Completá el rótulo: título, subtítulo, autor y número de plano.",
                "en": "Fill in the title block: title, subtitle, author and drawing number.",
                "pt": "Preencha o carimbo: título, subtítulo, autor e número do desenho.",
            },
            Say={"es": ("rótulo",), "en": ("title block",), "pt": ("carimbo",)},
            Action=_titleBlock,
        ),
    ]
