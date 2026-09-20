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

"""PartDesign example: a screw with a chamfer and a thread, then measured in 3D."""

import Part
import Sketcher
from FreeCAD import Vector

from ._common import activeDoc, attachAt, fitView, lastOfType, setView
from ._words import down, no, numbers, send

TITLE = {
    "es": "PartDesign: un tornillo paso a paso",
    "en": "PartDesign: a screw, step by step",
    "pt": "PartDesign: um parafuso passo a passo",
}


def _body(doc):
    return lastOfType(doc, "PartDesign::Body")


def _shank() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    shank = doc.addObject("PartDesign::AdditiveCylinder", "Shank")
    shank.Radius = 5
    shank.Height = 16
    body.addObject(shank)
    # el cilindro nace con su base en el origen: se baja media altura del centro dictado
    attachAt(body, shank, 0, 0, 12 - 16 / 2)
    doc.recompute()
    fitView()


def _tip() -> None:
    doc = activeDoc()
    body = _body(doc)
    tip = doc.addObject("PartDesign::AdditiveCone", "Tip")
    tip.Radius1 = 1
    tip.Radius2 = 5
    tip.Height = 4
    body.addObject(tip)
    attachAt(body, tip, 0, 0, 2 - 4 / 2)
    doc.recompute()
    fitView()


def _head() -> None:
    doc = activeDoc()
    body = _body(doc)
    head = doc.addObject("PartDesign::AdditivePrism", "Head")
    head.Polygon = 6
    head.Circumradius = 8
    head.Height = 4
    body.addObject(head)
    attachAt(body, head, 0, 0, 22 - 4 / 2)
    doc.recompute()
    fitView()


def _chamfer() -> None:
    doc = activeDoc()
    body = _body(doc)
    # como el comando del diccionario: todos los bordes de la última operación
    chamfer = doc.addObject("PartDesign::Chamfer", "Chamfer")
    chamfer.Base = (body.Tip, [""])
    chamfer.UseAllEdges = True
    chamfer.Size = 0.5
    body.addObject(chamfer)
    doc.recompute()
    fitView()


def _threadSketch() -> None:
    doc = activeDoc()
    body = _body(doc)
    plane = next(item for item in body.Origin.OriginFeatures if item.Role == "XZ_Plane")
    sketch = body.newObject("Sketcher::SketchObject", "ThreadProfile")
    sketch.AttachmentSupport = [(plane, "")]
    sketch.MapMode = "FlatFace"
    doc.recompute()
    fitView()


def _threadProfile() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    # rectángulo por esquinas (4, 2) - (6, 3): un surco que entra en el vástago desde afuera
    corners = [Vector(4, 2, 0), Vector(6, 2, 0), Vector(6, 3, 0), Vector(4, 3, 0)]
    for index in range(4):
        sketch.addGeometry(Part.LineSegment(corners[index], corners[(index + 1) % 4]), False)
    for index in range(4):
        sketch.addConstraint(Sketcher.Constraint("Coincident", index, 2, (index + 1) % 4, 1))
    doc.recompute()
    fitView()


def _thread() -> None:
    doc = activeDoc()
    body = _body(doc)
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    helix = body.newObject("PartDesign::SubtractiveHelix", "Thread")
    helix.Profile = sketch
    helix.ReferenceAxis = (sketch, ["V_Axis"])
    helix.Mode = "pitch-height-angle"
    helix.Pitch = 3
    helix.Height = 12
    sketch.Visibility = False
    doc.recompute()
    fitView()


def _dimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario (3D: hay un sólido)
    from measure import _dimension3d

    _dimension3d(-8, 0, 24, 8, 0, 24)
    activeDoc().recompute()
    fitView()


def _isometric() -> None:
    setView("isometric")


def steps() -> list:
    """Return the frames of the screw example."""
    from InputPrompts.ExampleStep import ExampleStep

    def more(*items):
        # tras los valores, la figura se suma a un cuerpo que ya existe: «no» a cuerpo nuevo y elegirlo
        return lambda language: numbers(language, *items) + no(language) + send(language)

    return [
        ExampleStep(
            Text={
                "es": "Empezá por el vástago: un cilindro de radio 5 y 16 de alto, con el centro en (0, 0, 12).",
                "en": "Start with the shank: a cylinder with radius 5 and height 16, centred at (0, 0, 12).",
                "pt": "Comece pela haste: um cilindro de raio 5 e 16 de altura, com o centro em (0, 0, 12).",
            },
            Path={
                "es": ("banco", "diseño", "sumar", "cilindro"),
                "en": ("workbench", "design", "add", "cylinder"),
                "pt": ("trabalho", "design", "aditivo", "cilindro"),
            },
            Values=lambda language: numbers(language, 5, 16, 0, 0, 12),
            Action=_shank,
        ),
        ExampleStep(
            Text={
                "es": "Agregá la punta: un cono de radio 1 abajo y 5 arriba, 4 de alto, centro en (0, 0, 2). Como ya hay un cuerpo, se responde «no» a «¿cuerpo nuevo?» y se elige el existente.",
                "en": "Add the tip: a cone with radius 1 at the bottom and 5 at the top, 4 high, centred at (0, 0, 2). There is a body already, so answer “no” to “new body?” and pick the existing one.",
                "pt": "Adicione a ponta: um cone de raio 1 embaixo e 5 em cima, 4 de altura, centro em (0, 0, 2). Como já há um corpo, responda «não» a «corpo novo?» e escolha o existente.",
            },
            Path={"es": ("cono",), "en": ("cone",), "pt": ("cone",)},
            Values=more(1, 5, 4, 0, 0, 2),
            Action=_tip,
        ),
        ExampleStep(
            Text={
                "es": "Ahora la cabeza: un prisma de 6 lados, radio 8 y 4 de alto, centro en (0, 0, 22).",
                "en": "Now the head: a 6-sided prism, radius 8 and 4 high, centred at (0, 0, 22).",
                "pt": "Agora a cabeça: um prisma de 6 lados, raio 8 e 4 de altura, centro em (0, 0, 22).",
            },
            Path={"es": ("prisma",), "en": ("prism",), "pt": ("prisma",)},
            Values=more(6, 8, 4, 0, 0, 22),
            Action=_head,
        ),
        ExampleStep(
            Text={
                "es": "Achaflaná los bordes: 0,5 mm. El comando trabaja sobre la pieza seleccionada o, si no hay ninguna, sobre la última operación. Dictás «cero punto cinco» (o «cero coma cinco»).",
                "en": "Chamfer the edges: 0.5 mm. The command works on the selected part or, if there is none, on the last operation. Say “zero point five”.",
                "pt": "Chanfre as bordas: 0,5 mm. O comando trabalha sobre a peça selecionada ou, se não houver, sobre a última operação. Diga «zero ponto cinco».",
            },
            Path={
                "es": ("subir", "editar", "chaflan por medida"),
                "en": ("up", "edit", "chamfer by size"),
                "pt": ("subir", "editar", "chanfro por medida"),
            },
            Values=lambda language: numbers(language, 0.5),
            Action=_chamfer,
        ),
        ExampleStep(
            Text={
                "es": "Para la rosca hace falta un dibujo del surco. Boceto nuevo sobre el plano XZ (es el segundo de la lista: «abajo» una vez y «enviar»).",
                "en": "The thread needs a drawing of the groove. New sketch on the XZ plane (second in the list: “down” once and “send”).",
                "pt": "Para a rosca é preciso um desenho do sulco. Esboço novo no plano XZ (é o segundo da lista: «abaixo» uma vez e «enviar»).",
            },
            Path={
                "es": ("base", "nuevo boceto"),
                "en": ("base", "new sketch"),
                "pt": ("base", "esboco novo"),
            },
            Values=lambda language: down(language, 1) + send(language),
            Action=_threadSketch,
        ),
        ExampleStep(
            Text={
                "es": "Dibujá el surco: un rectángulo de (4, 2) a (6, 3). Entra 1 mm en el vástago, que tiene radio 5.",
                "en": "Draw the groove: a rectangle from (4, 2) to (6, 3). It goes 1 mm into the shank, which has radius 5.",
                "pt": "Desenhe o sulco: um retângulo de (4, 2) a (6, 3). Entra 1 mm na haste, que tem raio 5.",
            },
            Path={
                "es": ("geometria", "rectangulo", "rectangulo por esquinas"),
                "en": ("geometry", "rectangle", "rectangle by corners"),
                "pt": ("geometria", "retangulo", "retangulo por cantos"),
            },
            Values=lambda language: numbers(language, 4, 2, 6, 3),
            Action=_threadProfile,
        ),
        ExampleStep(
            Text={
                "es": "Cerrá el croquis y cortá la rosca con una hélice: paso 3 y altura 12. Después elegís el dibujo de la lista (es el único: «enviar»).",
                "en": "Close the sketch and cut the thread with a helix: pitch 3 and height 12. Then pick the drawing from the list (it is the only one: “send”).",
                "pt": "Feche o esboço e corte a rosca com uma hélice: passo 3 e altura 12. Depois escolha o desenho da lista (é o único: «enviar»).",
            },
            Path={
                "es": ("cerrar croquis", "banco", "diseño", "cortar", "helice"),
                "en": ("close sketch", "workbench", "design", "cut", "helix"),
                "pt": ("fechar esboco", "trabalho", "design", "cortar", "helice"),
            },
            Values=lambda language: numbers(language, 3, 12) + send(language),
            Action=_thread,
        ),
        ExampleStep(
            Text={
                "es": "Medí el ancho de la cabeza en 3D: de (-8, 0, 24) a (8, 0, 24). Con un sólido en el documento, «cota» pide 6 valores: X, Y y Z de cada punto.",
                "en": "Measure the width of the head in 3D: from (-8, 0, 24) to (8, 0, 24). With a solid in the document, “measure” asks for 6 values: X, Y and Z of each point.",
                "pt": "Meça a largura da cabeça em 3D: de (-8, 0, 24) a (8, 0, 24). Com um sólido no documento, «medir» pede 6 valores: X, Y e Z de cada ponto.",
            },
            Path={"es": ("cota",), "en": ("measure",), "pt": ("medir",)},
            Values=lambda language: numbers(language, -8, 0, 24, 8, 0, 24),
            Action=_dimension,
        ),
        ExampleStep(
            Text={
                "es": "Mirá el tornillo terminado en la vista «tres de» (isométrica).",
                "en": "See the finished screw in the isometric view.",
                "pt": "Veja o parafuso pronto na vista isométrica.",
            },
            Path={"es": ("tres de",), "en": ("isometric",), "pt": ("isometrica",)},
            Action=_isometric,
        ),
    ]
