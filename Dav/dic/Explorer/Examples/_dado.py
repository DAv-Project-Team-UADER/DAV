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

"""PartDesign example: a die. A cube, a cylinder cut for the one and a sketch and pocket per face."""

import FreeCAD as App

from ._common import activeDoc, attachAt, fitView, lastOfType, setView
from ._words import down, nextItem, numbers, send

TITLE = {
    "es": "Dado",
    "en": "Die",
    "pt": "Dado",
}

SIDE = 20  # el dado ocupa de (0, 0, 0) a (20, 20, 20)
PIP_RADIUS = 2
PIP_DEPTH = 2

# Caras del dado: (número, cómo se llama la cara en el selector de planos, vista que la muestra).
# El 1 está arriba y se hace con un cilindro; opuestas suman 7: 2-5, 3-4 y 1-6.
FACES = (
    (2, "frontal", "front"),
    (3, "derecha", "right"),
    (4, "izquierda", "left"),
    (5, "trasera", "rear"),
    (6, "inferior", "bottom"),
)

# Puntos de cada cara medidos desde el centro de la cara; el primero es el que se dicta.
PIPS = {
    2: ((5, 5), (-5, -5)),
    3: ((5, 5), (0, 0), (-5, -5)),
    4: ((5, 5), (-5, 5), (5, -5), (-5, -5)),
    5: ((5, 5), (-5, 5), (5, -5), (-5, -5), (0, 0)),
    6: ((5, 5), (-5, 5), (5, 0), (-5, 0), (5, -5), (-5, -5)),
}


def _faces(doc) -> dict:
    """Planar faces the sketch selector lists (the same function the real command uses)."""
    try:
        from Workbench.Sketcher.new_sketch._faces import listPlanarFaces
    except ImportError:
        from dic.Workbench.Sketcher.new_sketch._faces import listPlanarFaces
    return listPlanarFaces(doc)


def _isSketch(obj) -> bool:
    return obj.isDerivedFrom("Sketcher::SketchObject") and obj.GeometryCount > 0


def _cube() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    box = doc.addObject("PartDesign::AdditiveBox", "Box")
    box.Length = box.Width = box.Height = SIDE
    body.addObject(box)
    # la caja nace con una esquina en el origen: el centro dictado (10, 10, 10) queda a media medida
    attachAt(body, box, 0, 0, 0)
    doc.recompute()
    fitView()


def _cylinderForOne() -> None:
    doc = activeDoc()
    body = lastOfType(doc, "PartDesign::Body")
    cut = doc.addObject("PartDesign::SubtractiveCylinder", "One")
    cut.Radius = PIP_RADIUS
    cut.Height = 2 * PIP_DEPTH
    body.addObject(cut)
    # centro dictado (10, 10, 20): la cara de arriba; la base del cilindro está media altura más abajo
    attachAt(body, cut, SIDE / 2, SIDE / 2, SIDE - PIP_DEPTH)
    doc.recompute()
    fitView()


def _sketchOnFace(name: str):
    def action() -> None:
        from Workbench.Sketcher.new_sketch._faces import attachSketchToFace

        doc = activeDoc()
        faces = _faces(doc)
        option = faces[_faceKey(faces, name)]
        body = option["body"]
        sketch = body.newObject("Sketcher::SketchObject", f"Face_{name}")
        attachSketchToFace(sketch, option)
        doc.recompute()
        fitView()

    return action


def _faceKey(faces: dict, name: str) -> str:
    """Key of the biggest face looking that way (its label has no numeric suffix)."""
    for key, option in faces.items():
        if option["label"] == f"Cara {name}":
            return key
    raise RuntimeError(f"No encuentro la cara {name}: seguí los cuadros en orden.")


def _pips(number: int):
    def action() -> None:
        import Part

        doc = activeDoc()
        sketch = lastOfType(doc, "Sketcher::SketchObject")
        for x, y in PIPS[number]:
            sketch.addGeometry(
                Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), PIP_RADIUS), False
            )
        doc.recompute()
        fitView()

    return action


def _pocket() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    body = sketch.getParentGeoFeatureGroup() or lastOfType(doc, "PartDesign::Body")
    pocket = doc.addObject("PartDesign::Pocket", "Pocket")
    pocket.Profile = sketch
    pocket.Length = PIP_DEPTH
    body.addObject(pocket)
    sketch.Visibility = False
    doc.recompute()
    fitView()


def _dimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario (3D: hay un sólido)
    from measure import _dimension3d

    _dimension3d(0, 0, 0, SIDE, 0, 0)
    activeDoc().recompute()
    fitView()


def _showView(name: str):
    return lambda: setView(name)


def _downToFace(name: str):
    """«abajo» tantas veces como haga falta: tres planos base y después las caras de la lista."""

    def values(language: str) -> tuple:
        faces = _faces(activeDoc())
        position = list(faces).index(_faceKey(faces, name))
        return down(language, 3 + position) + send(language)

    return values


def _pocketValues(language: str) -> tuple:
    """Profundidad y, en la lista de dibujos, «avanzar» hasta el último boceto."""
    sketches = [obj for obj in activeDoc().Objects if _isSketch(obj)]
    return numbers(language, PIP_DEPTH) + nextItem(language, max(len(sketches) - 1, 0)) + send(language)


def steps() -> list:
    """Return the frames of the die example."""
    from InputPrompts.ExampleStep import ExampleStep

    def values(*items):
        return lambda language: numbers(language, *items)

    frames = [
        ExampleStep(
            Text={
                "es": "El cuerpo del dado: una caja de 20 x 20 x 20 con el centro en (10, 10, 10). Sin cuerpos previos, se crea uno solo.",
                "en": "The body of the die: a 20 x 20 x 20 box centred at (10, 10, 10). With no bodies yet, one is created for you.",
                "pt": "O corpo do dado: uma caixa de 20 x 20 x 20 com o centro em (10, 10, 10). Sem corpos prévios, um é criado sozinho.",
            },
            Path={
                "es": ("banco", "diseño", "sumar", "caja"),
                "en": ("workbench", "design", "add", "box"),
                "pt": ("trabalho", "projeto", "aditivo", "caixa"),
            },
            Values=values(SIDE, SIDE, SIDE, 10, 10, 10),
            Action=_cube,
        ),
        ExampleStep(
            Text={
                "es": "La cara del 1 (arriba): un solo hueco, con un cilindro sustractivo de radio 2 y 4 de alto, centro en (10, 10, 20). Primero «subir» un nivel, porque estás en Sumar. Después se elige el cuerpo.",
                "en": "The face with 1 (top): a single hole, with a subtractive cylinder of radius 2 and height 4, centred at (10, 10, 20). First go “up” one level, since you are in Add. Then pick the body.",
                "pt": "A face do 1 (em cima): um único furo, com um cilindro subtrativo de raio 2 e 4 de altura, centro em (10, 10, 20). Primeiro «subir» um nível, porque você está em Aditivo. Depois escolha o corpo.",
            },
            Path={
                "es": ("subir", "cortar", "cilindro"),
                "en": ("up", "cut", "cylinder"),
                "pt": ("subir", "cortar", "cilindro"),
            },
            Values=lambda language: numbers(language, PIP_RADIUS, 2 * PIP_DEPTH, 10, 10, SIDE) + send(language),
            Action=_cylinderForOne,
        ),
    ]

    for number, name, _view in FACES:
        frames += [
            ExampleStep(
                Text={
                    "es": f"Cara del {number}: un boceto nuevo sobre la cara {name}. Elegila con «abajo» en la lista (tres planos y después las caras) y «enviar».",
                    "en": f"Face with {number}: a new sketch on that face ({name}). Pick it with “down” in the list (three planes, then the faces) and “send”.",
                    "pt": f"Face do {number}: um esboço novo sobre essa face ({name}). Escolha-a com «abaixo» na lista (três planos e depois as faces) e «enviar».",
                },
                Path={
                    "es": ("base", "nuevo boceto"),
                    "en": ("base", "new sketch"),
                    "pt": ("base", "esboco novo"),
                },
                Values=_downToFace(name),
                Action=_sketchOnFace(name),
            ),
            ExampleStep(
                Text={
                    "es": f"Dibujá el primer hueco del {number}: círculo de centro (5, 5) y radio 2, medido desde el centro de la cara. Los demás huecos del {number} se dibujan solos.",
                    "en": f"Draw the first pip of the {number}: a circle centred at (5, 5) with radius 2, measured from the centre of the face. The other pips are drawn for you.",
                    "pt": f"Desenhe o primeiro furo do {number}: círculo de centro (5, 5) e raio 2, medido do centro da face. Os outros furos são desenhados sozinhos.",
                },
                Path={
                    "es": ("geometria", "circulo", "circulo"),
                    "en": ("geometry", "circle", "circle"),
                    "pt": ("geometria", "circulo", "circulo"),
                },
                Values=values(5, 5, PIP_RADIUS),
                Action=_pips(number),
            ),
            ExampleStep(
                Text={
                    "es": f"Cerrá el croquis y vaciá {PIP_DEPTH} mm: los huecos del {number} se restan del dado. Al cerrar volvés a «banco» y «diseño», porque el cierre te deja en Croquis. La lista de dibujos se recorre con «avanzar» hasta el último.",
                    "en": f"Close the sketch and hollow {PIP_DEPTH} mm: the pips of the {number} are subtracted from the die. Move through the drawings with “next” up to the last one.",
                    "pt": f"Feche o esboço e esvazie {PIP_DEPTH} mm: os furos do {number} são subtraídos do dado. A lista de desenhos se percorre com «avancar» até o último.",
                },
                Path={
                    "es": ("cerrar croquis", "banco", "diseño", "cortar", "vaciar"),
                    "en": ("close sketch", "workbench", "design", "cut", "hollow"),
                    "pt": ("fechar esboco", "trabalho", "projeto", "cortar", "esvaziar"),
                },
                Values=_pocketValues,
                Action=_pocket,
            ),
        ]

    frames.append(
        ExampleStep(
            Text={
                "es": "Medí el borde del dado en 3D: de (0, 0, 0) a (20, 0, 0). «cota» pide 6 valores: X, Y y Z de cada punto.",
                "en": "Measure the edge of the die in 3D: from (0, 0, 0) to (20, 0, 0). “measure” asks for 6 values: X, Y and Z of each point.",
                "pt": "Meça a aresta do dado em 3D: de (0, 0, 0) a (20, 0, 0). «medir» pede 6 valores: X, Y e Z de cada ponto.",
            },
            Path={"es": ("cota",), "en": ("measure",), "pt": ("medir",)},
            Values=values(0, 0, 0, SIDE, 0, 0),
            Action=_dimension,
        )
    )

    # ensayo de vistas: cada cara del dado con su vista estándar, y al final el «tres de»
    viewWords = {
        "front": {"es": "frontal", "en": "front", "pt": "frontal"},
        "rear": {"es": "trasera", "en": "rear", "pt": "traseira"},
        "left": {"es": "izquierda", "en": "left", "pt": "esquerda"},
        "right": {"es": "derecha", "en": "right", "pt": "direita"},
        "top": {"es": "arriba", "en": "top", "pt": "superior"},
        "bottom": {"es": "abajo", "en": "bottom", "pt": "inferior"},
    }
    tour = (("front", 2), ("rear", 5), ("left", 4), ("right", 3), ("top", 1), ("bottom", 6))
    for view, number in tour:
        frames.append(
            ExampleStep(
                Text={
                    "es": f"Ensayo de vistas: mirá la cara del {number}.",
                    "en": f"View test: look at the face with {number}.",
                    "pt": f"Ensaio de vistas: veja a face do {number}.",
                },
                Path={lang: (word,) for lang, word in viewWords[view].items()},
                Action=_showView(view),
            )
        )
    frames.append(
        ExampleStep(
            Text={
                "es": "Y para cerrar, el dado completo en la vista «tres de» (isométrica).",
                "en": "And to finish, the whole die in the isometric view.",
                "pt": "E para terminar, o dado completo na vista isométrica.",
            },
            Path={"es": ("tres de",), "en": ("isometric",), "pt": ("isometrica",)},
            Action=_showView("isometric"),
        )
    )
    return frames
