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

"""Draft example: a house drawn with rectangles, triangles, circles and lines."""

from FreeCAD import Placement, Rotation, Vector

from ._common import activeDoc, fitView
from ._words import nextItem, numbers, send

TITLE = {
    "es": "Draft: una casa con figuras 2D",
    "en": "Draft: a house from 2D shapes",
    "pt": "Draft: uma casa com formas 2D",
}

# La casa, en milímetros: cuerpo (2,0)-(42,25), techo hasta y=50, chimenea a la derecha.
_BODY = (2, 0, 42, 25)
_ROOF = (0, 25, 44, 25, 22, 50)
_DOOR = (17, 0, 27, 14)
_WINDOW_LEFT = (10, 14, 8, 8)  # centro y tamaño: (6,10)-(14,18)
_WINDOW_RIGHT = (34, 14, 8, 8)  # (30,10)-(38,18)
_CHIMNEY = (31, 30, 37, 48)  # arranca dentro del techo: el corte lo deja detrás
_CHIMNEY_CAP = (29, 48, 39, 48, 34, 54)
_ROOF_WINDOW = (22, 34, 5)
_KNOB = (25, 7, 1)
_PANES = (
    (10, 10, 10, 18),
    (6, 14, 14, 14),
    (34, 10, 34, 18),
    (30, 14, 38, 14),
)


# lo que el corte necesita encontrar: la chimenea (base) y el techo (herramienta)
_made = {}


def _rectangle(x1, y1, x2, y2):
    import Draft

    doc = activeDoc()
    obj = Draft.make_rectangle(
        abs(x2 - x1), abs(y2 - y1), placement=Placement(Vector(min(x1, x2), min(y1, y2), 0), Rotation())
    )
    doc.recompute()
    fitView()
    return obj


def _rectangleByCenter(x, y, width, height) -> None:
    _rectangle(x - width / 2, y - height / 2, x + width / 2, y + height / 2)


def _triangle(x1, y1, x2, y2, x3, y3):
    import Draft

    doc = activeDoc()
    obj = Draft.make_wire([Vector(x1, y1, 0), Vector(x2, y2, 0), Vector(x3, y3, 0)], closed=True)
    doc.recompute()
    fitView()
    return obj


def _roof() -> None:
    _made["roof"] = _triangle(*_ROOF)


def _chimney() -> None:
    _made["chimney"] = _rectangle(*_CHIMNEY)


def _offered() -> list:
    """Objects the voice list offers, in the order it shows them."""
    try:
        from Workbench._prompts import isShape
    except ImportError:
        from dic.Workbench._prompts import isShape
    return [obj for obj in activeDoc().Objects if isShape(obj)]


def _pickCut(language: str) -> tuple:
    """Words that pick the chimney and then the roof from the list: «avanzar» up to each and «enviar»."""
    offered = _offered()
    words = ()
    for key in ("chimney", "roof"):
        words += nextItem(language, offered.index(_made[key])) + send(language)
    return words


def _cut() -> None:
    # la misma operación que ejecuta el comando «cortar»: la chimenea pierde lo que ocupa el techo
    import Draft

    doc = activeDoc()
    Draft.cut(_made["chimney"], _made["roof"])
    doc.recompute()
    try:
        _made["roof"].ViewObject.Visibility = True  # Draft oculta las dos piezas
    except Exception:
        pass
    fitView()


def _circle(x, y, radius) -> None:
    import Draft

    doc = activeDoc()
    Draft.make_circle(radius, placement=Placement(Vector(x, y, 0), Rotation()))
    doc.recompute()
    fitView()


def _line(x1, y1, x2, y2) -> None:
    import Draft

    doc = activeDoc()
    Draft.make_wire([Vector(x1, y1, 0), Vector(x2, y2, 0)], closed=False)
    doc.recompute()
    fitView()


def steps() -> list:
    """Return the frames of the Draft house example."""
    from InputPrompts.ExampleStep import ExampleStep

    def values(*items):
        return lambda language: numbers(language, *items)

    def frame(text, path, items, action):
        return ExampleStep(Text=text, Path=path, Values=values(*items), Action=action)

    return [
        frame(
            {
                "es": "Empezá por el cuerpo de la casa: un rectángulo por esquinas, de (2, 0) a (42, 25).",
                "en": "Start with the body of the house: a rectangle by corners, from (2, 0) to (42, 25).",
                "pt": "Comece pelo corpo da casa: um retângulo por cantos, de (2, 0) a (42, 25).",
            },
            {
                "es": ("banco", "borrador", "crear", "rectángulo"),
                "en": ("workbench", "draft", "create", "rectangle"),
                "pt": ("trabalho", "draft", "criar", "retângulo"),
            },
            _BODY,
            lambda: _rectangle(*_BODY),
        ),
        frame(
            {
                "es": "El techo es un triángulo por vértices: (0, 25), (44, 25) y (22, 50). «triángulo» pide 6 valores: X e Y de cada vértice.",
                "en": "The roof is a triangle by vertices: (0, 25), (44, 25) and (22, 50). “triangle” asks for 6 values: X and Y of each vertex.",
                "pt": "O telhado é um triângulo por vértices: (0, 25), (44, 25) e (22, 50). «triângulo» pede 6 valores: X e Y de cada vértice.",
            },
            {"es": ("triángulo",), "en": ("triangle",), "pt": ("triângulo",)},
            _ROOF,
            _roof,
        ),
        frame(
            {
                "es": "La puerta: otro rectángulo por esquinas, de (17, 0) a (27, 14).",
                "en": "The door: another rectangle by corners, from (17, 0) to (27, 14).",
                "pt": "A porta: outro retângulo por cantos, de (17, 0) a (27, 14).",
            },
            {"es": ("rectángulo",), "en": ("rectangle",), "pt": ("retângulo",)},
            _DOOR,
            lambda: _rectangle(*_DOOR),
        ),
        frame(
            {
                "es": "La ventana izquierda, ahora con «rectángulo por centro»: centro (10, 14), ancho 8 y alto 8.",
                "en": "The left window, now with “rectangle by center”: centre (10, 14), width 8 and height 8.",
                "pt": "A janela esquerda, agora com «retângulo por centro»: centro (10, 14), largura 8 e altura 8.",
            },
            {
                "es": ("rectángulo por centro",),
                "en": ("rectangle by center",),
                "pt": ("retângulo por centro",),
            },
            _WINDOW_LEFT,
            lambda: _rectangleByCenter(*_WINDOW_LEFT),
        ),
        frame(
            {
                "es": "La ventana derecha, igual: centro (34, 14), ancho 8 y alto 8.",
                "en": "The right window, the same way: centre (34, 14), width 8 and height 8.",
                "pt": "A janela direita, do mesmo modo: centro (34, 14), largura 8 e altura 8.",
            },
            {
                "es": ("rectángulo por centro",),
                "en": ("rectangle by center",),
                "pt": ("retângulo por centro",),
            },
            _WINDOW_RIGHT,
            lambda: _rectangleByCenter(*_WINDOW_RIGHT),
        ),
        frame(
            {
                "es": "La chimenea: un rectángulo por esquinas, de (31, 30) a (37, 48). Arranca dentro del techo a propósito: después lo cortamos.",
                "en": "The chimney: a rectangle by corners, from (31, 30) to (37, 48). It starts inside the roof on purpose: we cut it afterwards.",
                "pt": "A chaminé: um retângulo por cantos, de (31, 30) a (37, 48). Ela começa dentro do telhado de propósito: depois a cortamos.",
            },
            {"es": ("rectángulo",), "en": ("rectangle",), "pt": ("retângulo",)},
            _CHIMNEY,
            _chimney,
        ),
        frame(
            {
                "es": "El gorro de la chimenea: un triángulo de (29, 48), (39, 48) y (34, 54).",
                "en": "The chimney cap: a triangle at (29, 48), (39, 48) and (34, 54).",
                "pt": "O chapéu da chaminé: um triângulo em (29, 48), (39, 48) e (34, 54).",
            },
            {"es": ("triángulo",), "en": ("triangle",), "pt": ("triângulo",)},
            _CHIMNEY_CAP,
            lambda: _triangle(*_CHIMNEY_CAP),
        ),
        ExampleStep(
            Text={
                "es": "La chimenea está detrás del techo: hay que cortarla. Entrá a «modificar» y decí «cortar». Primero elegís el objeto a cortar (la chimenea) y después el que corta (el techo): «avanzar» hasta cada uno y «enviar».",
                "en": "The chimney is behind the roof, so it has to be cut. Enter “modify” and say “cut”. First pick the object to cut (the chimney), then the one that cuts (the roof): “next” up to each one and “send”.",
                "pt": "A chaminé está atrás do telhado, então é preciso cortá-la. Entre em «modificar» e diga «cortar». Primeiro escolha o objeto a cortar (a chaminé) e depois o que corta (o telhado): «próximo» até cada um e «enviar».",
            },
            Path={
                "es": ("modificar", "cortar"),
                "en": ("modify", "cut"),
                "pt": ("modificar", "cortar"),
            },
            Values=_pickCut,
            Action=_cut,
        ),
        frame(
            {
                "es": "La ventana redonda del techo: círculo con centro en (22, 34) y radio 5.",
                "en": "The round roof window: a circle centred at (22, 34) with radius 5.",
                "pt": "A janela redonda do telhado: círculo com centro em (22, 34) e raio 5.",
            },
            {
                "es": ("círculo", "círculo"),
                "en": ("circle", "circle"),
                "pt": ("círculo", "círculo"),
            },
            _ROOF_WINDOW,
            lambda: _circle(*_ROOF_WINDOW),
        ),
        frame(
            {
                "es": "El picaporte de la puerta: círculo con centro en (25, 7) y radio 1.",
                "en": "The door knob: a circle centred at (25, 7) with radius 1.",
                "pt": "A maçaneta da porta: círculo com centro em (25, 7) e raio 1.",
            },
            {"es": ("círculo",), "en": ("circle",), "pt": ("círculo",)},
            _KNOB,
            lambda: _circle(*_KNOB),
        ),
        frame(
            {
                "es": "Falta la cruz de las ventanas, con líneas por puntos. Primero «subir» a Borrador y entrá a «dibujo». Vertical de la ventana izquierda: de (10, 10) a (10, 18). «línea» pide 4 valores.",
                "en": "The window crosses are missing, drawn with lines by points. First go “up” to Draft and enter “drafting”. Vertical of the left window: from (10, 10) to (10, 18). “line” asks for 4 values.",
                "pt": "Faltam as cruzes das janelas, com linhas por pontos. Primeiro «subir» ao Draft e entre em «desenho». Vertical da janela esquerda: de (10, 10) a (10, 18). «linha» pede 4 valores.",
            },
            {
                "es": ("subir", "dibujo", "línea"),
                "en": ("up", "drafting", "line"),
                "pt": ("subir", "desenho", "linha"),
            },
            _PANES[0],
            lambda: _line(*_PANES[0]),
        ),
        frame(
            {
                "es": "Horizontal de la ventana izquierda: de (6, 14) a (14, 14).",
                "en": "Horizontal of the left window: from (6, 14) to (14, 14).",
                "pt": "Horizontal da janela esquerda: de (6, 14) a (14, 14).",
            },
            {"es": ("línea",), "en": ("line",), "pt": ("linha",)},
            _PANES[1],
            lambda: _line(*_PANES[1]),
        ),
        frame(
            {
                "es": "Vertical de la ventana derecha: de (34, 10) a (34, 18).",
                "en": "Vertical of the right window: from (34, 10) to (34, 18).",
                "pt": "Vertical da janela direita: de (34, 10) a (34, 18).",
            },
            {"es": ("línea",), "en": ("line",), "pt": ("linha",)},
            _PANES[2],
            lambda: _line(*_PANES[2]),
        ),
        frame(
            {
                "es": "Y por último, la horizontal de la ventana derecha: de (30, 14) a (38, 14). ¡La casa está lista!",
                "en": "And finally the horizontal of the right window: from (30, 14) to (38, 14). The house is done!",
                "pt": "E por fim a horizontal da janela direita: de (30, 14) a (38, 14). A casa está pronta!",
            },
            {"es": ("línea",), "en": ("line",), "pt": ("linha",)},
            _PANES[3],
            lambda: _line(*_PANES[3]),
        ),
    ]
