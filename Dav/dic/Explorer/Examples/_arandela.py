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

"""Washer example: a flat M6 washer sketched, extruded in PartDesign and put on a TechDraw page."""

import os

import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector

from ._common import activeDoc, fitView, lastOfType
from ._words import decimal, nextItem, numbers, send

TITLE = {
    "es": "Arandela plana M6",
    "en": "M6 flat washer",
    "pt": "Arruela lisa M6",
}

# arandela plana M6 (ISO 7089): agujero de 6,4 mm, exterior de 12 mm y 1,6 mm de espesor
INNER_RADIUS = 3.2
OUTER_RADIUS = 6
THICKNESS = 1.6

# texto de la hoja por idioma
_LABEL = {"es": "M6 arandela", "en": "M6 washer", "pt": "M6 arruela"}

# el círculo de 12 mm se ve de 48 mm en la hoja
_VIEW_SCALE = 4

_TEMPLATE_FALLBACK = os.path.join("Mod", "TechDraw", "Templates", "Default_Template_A4_Landscape.svg")


def _newSketch() -> None:
    doc = activeDoc()
    doc.addObject("Sketcher::SketchObject", "Sketch")
    doc.recompute()
    fitView()


def _circle(radius: float):
    def action() -> None:
        doc = activeDoc()
        sketch = lastOfType(doc, "Sketcher::SketchObject")
        sketch.addGeometry(Part.Circle(Vector(0, 0, 0), Vector(0, 0, 1), radius), False)
        doc.recompute()
        fitView()

    return action


def _innerDiameter() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    # la restricción del comando actúa sobre el primer círculo: el del agujero
    sketch.addConstraint(Sketcher.Constraint("Diameter", 0, 2 * INNER_RADIUS))
    doc.recompute()


def _outerDimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario (2D: todavía no hay sólido)
    from measure import _dimension2d

    _dimension2d(-OUTER_RADIUS, 0, OUTER_RADIUS, 0)
    activeDoc().recompute()
    fitView()


def _close() -> None:
    fitView()


def _pad() -> None:
    try:
        from Workbench.PartDesign.additive._parametric import _PadProfile
    except ImportError:
        from dic.Workbench.PartDesign.additive._parametric import _PadProfile

    doc = activeDoc()
    # la misma función que usa «extruir por medida»; si el perfil no sirve solo avisa por consola
    _PadProfile(doc, lastOfType(doc, "Sketcher::SketchObject"), THICKNESS)
    lastOfType(doc, "PartDesign::Pad")
    fitView()


def _thirdTemplate() -> str:
    """Return the third entry of the template browser: folders first, then the .svg files."""
    try:
        from Workbench.TechDraw.Page._page import _templateDir
    except ImportError:
        from dic.Workbench.TechDraw.Page._page import _templateDir

    folder = _templateDir()
    entries = [entry for entry in folder.iterdir() if not entry.name.startswith(".")]
    ordered = sorted((e for e in entries if e.is_dir()), key=lambda e: e.name.casefold())
    ordered += sorted(
        (e for e in entries if e.is_file() and e.suffix.lower() == ".svg"),
        key=lambda e: e.name.casefold(),
    )
    if len(ordered) >= 3 and ordered[2].is_file():
        return str(ordered[2])
    return os.path.join(App.getResourceDir(), _TEMPLATE_FALLBACK)


def _page() -> None:
    doc = activeDoc()
    page = doc.addObject("TechDraw::DrawPage", "Page")
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    template.Template = _thirdTemplate()
    page.Template = template
    doc.recompute()
    try:
        # abre la hoja en su propia pestaña
        page.ViewObject.doubleClicked()
    except Exception:
        pass


def _addView(name: str, source, direction: Vector, xDirection: Vector, x: float, y: float) -> None:
    doc = activeDoc()
    page = lastOfType(doc, "TechDraw::DrawPage")
    view = doc.addObject("TechDraw::DrawViewPart", name)
    page.addView(view)
    view.Source = [source]
    view.Direction = direction
    view.XDirection = xDirection
    view.ScaleType = "Custom"
    view.Scale = _VIEW_SCALE
    view.X = x
    view.Y = y
    doc.recompute()


def _isometricView() -> None:
    body = lastOfType(activeDoc(), "PartDesign::Body")
    # desde donde mira el «tres de» de FreeCAD: adelante, a la derecha y arriba
    _addView("IsometricView", body, Vector(1, -1, 1), Vector(1, 1, 0), 215, 120)


def _sketchView() -> None:
    sketch = lastOfType(activeDoc(), "Sketcher::SketchObject")
    # desde arriba: los dos círculos se ven sin deformar
    _addView("SketchView", sketch, Vector(0, 0, 1), Vector(1, 0, 0), 80, 120)


def _text() -> None:
    from InputPrompts.InputPromptI18n import ResolveLanguage

    doc = activeDoc()
    page = lastOfType(doc, "TechDraw::DrawPage")
    note = doc.addObject("TechDraw::DrawViewAnnotation", "Annotation")
    page.addView(note)
    note.Text = [_LABEL.get(ResolveLanguage(), _LABEL["es"])]
    note.TextSize = 10
    note.X = 148
    note.Y = 190
    doc.recompute()


def steps() -> list:
    """Return the frames of the washer example."""
    from InputPrompts.ExampleStep import ExampleStep

    def values(*items):
        return lambda language: numbers(language, *items)

    return [
        ExampleStep(
            Text={
                "es": "Empezá con un croquis nuevo en el plano base (XY es el primero de la lista: «enviar» lo elige).",
                "en": "Start with a new sketch on the base plane (XY is first in the list: “send” picks it).",
                "pt": "Comece com um croqui novo no plano base (XY é o primeiro da lista: «enviar» o escolhe).",
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
                "es": "Dibujá primero el agujero: un círculo de centro 0, 0 y radio 3,2 (diámetro 6,4). El radio se dicta «tres coma dos».",
                "en": "Draw the hole first: a circle centred at 0, 0 with radius 3.2 (diameter 6.4). Say the radius as “three point two”.",
                "pt": "Desenhe primeiro o furo: um círculo de centro 0, 0 e raio 3,2 (diâmetro 6,4). O raio se diz «três virgula dois».",
            },
            Path={
                "es": ("geometria", "circulo", "circulo"),
                "en": ("geometry", "circle", "circle"),
                "pt": ("geometria", "circulo", "circulo"),
            },
            Values=lambda language: numbers(language, 0, 0) + decimal(language, 3, 2),
            Action=_circle(INNER_RADIUS),
        ),
        ExampleStep(
            Text={
                "es": "Ahora el borde exterior: otro círculo con el mismo centro y radio 6 (diámetro 12).",
                "en": "Now the outer edge: another circle with the same centre and radius 6 (diameter 12).",
                "pt": "Agora a borda externa: outro círculo com o mesmo centro e raio 6 (diâmetro 12).",
            },
            Path={
                "es": ("geometria", "circulo", "circulo"),
                "en": ("geometry", "circle", "circle"),
                "pt": ("geometria", "circulo", "circulo"),
            },
            Values=values(0, 0, OUTER_RADIUS),
            Action=_circle(OUTER_RADIUS),
        ),
        ExampleStep(
            Text={
                "es": "Mostrá la medida interior con una restricción de diámetro: 6,4 mm. Actúa sobre el primer círculo, el del agujero.",
                "en": "Show the inner size with a diameter constraint: 6.4 mm. It acts on the first circle, the hole.",
                "pt": "Mostre a medida interna com uma restrição de diâmetro: 6,4 mm. Age sobre o primeiro círculo, o furo.",
            },
            Path={
                "es": ("restricciones", "diametro"),
                "en": ("constraints", "diameter"),
                "pt": ("restricoes", "diametro"),
            },
            Values=lambda language: decimal(language, 6, 4),
            Action=_innerDiameter,
        ),
        ExampleStep(
            Text={
                "es": "Y la medida exterior con una cota 2D: de (-6, 0) a (6, 0), o sea 12 mm. Primero «subir» a Croquis. «cota» pide 4 valores: X e Y de cada punto.",
                "en": "And the outer size with a 2D dimension: from (-6, 0) to (6, 0), that is 12 mm. First go “up” to Sketcher. “measure” asks for 4 values: X and Y of each point.",
                "pt": "E a medida externa com uma cota 2D: de (-6, 0) a (6, 0), ou seja 12 mm. Primeiro «subir» ao Croqui. «medir» pede 4 valores: X e Y de cada ponto.",
            },
            Path={
                "es": ("subir", "cota"),
                "en": ("up", "measure"),
                "pt": ("subir", "medir"),
            },
            Values=values(-OUTER_RADIUS, 0, OUTER_RADIUS, 0),
            Action=_outerDimension,
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
        ExampleStep(
            Text={
                "es": "Extruí el croquis con PartDesign: 1,6 mm de espesor. Después elegís el dibujo de la lista (es el único: «enviar»).",
                "en": "Extrude the sketch with PartDesign: 1.6 mm thick. Then pick the drawing from the list (it is the only one: “send”).",
                "pt": "Extrude o croqui com PartDesign: 1,6 mm de espessura. Depois escolha o desenho da lista (é o único: «enviar»).",
            },
            Path={
                "es": ("banco", "diseño", "sumar", "extruir por medida"),
                "en": ("workbench", "design", "add", "extrude by length"),
                "pt": ("trabalho", "design", "aditivo", "extrudar por medida"),
            },
            Values=lambda language: decimal(language, 1, 6) + send(language),
            Action=_pad,
        ),
        ExampleStep(
            Text={
                "es": "Ahora la hoja técnica: una página desde plantilla. En la lista elegí el tercer elemento («avanzar» dos veces) y «enviar»: es la plantilla con rótulo.",
                "en": "Now the technical sheet: a page from a template. In the list pick the third item (“next” twice) and “send”: it is the template with a title block.",
                "pt": "Agora a folha técnica: uma página a partir de um modelo. Na lista escolha o terceiro item («avancar» duas vezes) e «enviar»: é o modelo com carimbo.",
            },
            Path={
                "es": ("banco", "dibujo tecnico", "pagina", "plantilla"),
                "en": ("workbench", "drawing", "page", "template page"),
                "pt": ("trabalho", "tecnico", "pagina", "modelo"),
            },
            Values=lambda language: nextItem(language, 2) + send(language),
            Action=_page,
        ),
        ExampleStep(
            Text={
                "es": "Poné en la hoja la vista isométrica de la arandela (con la pieza seleccionada).",
                "en": "Place the isometric view of the washer on the page (with the part selected).",
                "pt": "Coloque na folha a vista isométrica da arruela (com a peça selecionada).",
            },
            Path={
                "es": ("vistas", "vista"),
                "en": ("views", "view"),
                "pt": ("vistas", "vista"),
            },
            Action=_isometricView,
        ),
        ExampleStep(
            Text={
                "es": "Agregá también la vista del boceto (con el croquis seleccionado): los dos círculos vistos desde arriba. Seguís en Vistas: alcanza con «vista».",
                "en": "Also add the view of the sketch (with the sketch selected): the two circles seen from above. You are still in Views: “view” is enough.",
                "pt": "Adicione também a vista do croqui (com o croqui selecionado): os dois círculos vistos de cima. Você continua em Vistas: basta «vista».",
            },
            Path={"es": ("vista",), "en": ("view",), "pt": ("vista",)},
            Action=_sketchView,
        ),
        ExampleStep(
            Text={
                "es": "Por último, un texto en la hoja que dice «M6 arandela».",
                "en": "Finally, a text on the page that says “M6 washer”.",
                "pt": "Por último, um texto na folha que diz «M6 arruela».",
            },
            Path={
                "es": ("anotaciones", "texto"),
                "en": ("annotations", "text"),
                "pt": ("anotacoes", "texto"),
            },
            Action=_text,
        ),
    ]
