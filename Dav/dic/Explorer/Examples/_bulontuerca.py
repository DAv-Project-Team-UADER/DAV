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

"""Assembly example: a bolt (simplified DIN 931) and its nut, built in PartDesign and joined in an assembly."""

from FreeCAD import Vector

from ._common import activeDoc, attachAt, fitView, lastOfType, setView
from ._words import nextItem, no, numbers, send, yes

TITLE = {
    "es": "Bulón-tuerca",
    "en": "Bolt-nut",
    "pt": "Parafuso-porca",
}

# Bulón M6 simplificado de la DIN 931: vástago liso de 20 mm y cabeza hexagonal de 4 mm.
# El eje va por Z y la punta en z = 0.
SHANK_RADIUS = 3
SHANK_LENGTH = 20
HEX_RADIUS = 6  # radio de la circunferencia que rodea al hexágono, en cabeza y tuerca
HEAD_HEIGHT = 4

# La tuerca (como la DIN 934, de 5 mm) se dibuja ya sobre el bulón, cerca de la punta: al
# insertar las piezas en el ensamblaje sus orígenes coinciden y cada una queda donde se la modeló.
NUT_HEIGHT = 5
NUT_CENTER_Z = 4
HOLE_HEIGHT = 10

# «insertar vínculo» deja cada pieza donde cae en la vista; acá la tuerca queda a un costado
NUT_SIDE_OFFSET = 30


def _bodies() -> list:
    return [obj for obj in activeDoc().Objects if obj.TypeId == "PartDesign::Body"]


def _shank() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    shank = doc.addObject("PartDesign::AdditiveCylinder", "Shank")
    shank.Radius = SHANK_RADIUS
    shank.Height = SHANK_LENGTH
    body.addObject(shank)
    # el cilindro nace con su base en el origen: el centro dictado (0, 0, 10) queda a media altura
    attachAt(body, shank, 0, 0, 0)
    doc.recompute()
    fitView()


def _head() -> None:
    doc = activeDoc()
    body = _bodies()[0]
    head = doc.addObject("PartDesign::AdditivePrism", "Head")
    head.Polygon = 6
    head.Circumradius = HEX_RADIUS
    head.Height = HEAD_HEIGHT
    body.addObject(head)
    attachAt(body, head, 0, 0, SHANK_LENGTH)
    doc.recompute()
    fitView()


def _nut() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    prism = doc.addObject("PartDesign::AdditivePrism", "Nut")
    prism.Polygon = 6
    prism.Circumradius = HEX_RADIUS
    prism.Height = NUT_HEIGHT
    body.addObject(prism)
    attachAt(body, prism, 0, 0, NUT_CENTER_Z - NUT_HEIGHT / 2)
    doc.recompute()
    fitView()


def _nutHole() -> None:
    doc = activeDoc()
    body = _bodies()[1]
    hole = doc.addObject("PartDesign::SubtractiveCylinder", "NutHole")
    hole.Radius = SHANK_RADIUS
    hole.Height = HOLE_HEIGHT
    body.addObject(hole)
    attachAt(body, hole, 0, 0, NUT_CENTER_Z - HOLE_HEIGHT / 2)
    doc.recompute()
    fitView()


def _createAssembly() -> None:
    doc = activeDoc()
    # lo mismo que hace el comando «crear ensamblaje» de FreeCAD
    assembly = doc.addObject("Assembly::AssemblyObject", "Assembly")
    assembly.Type = "Assembly"
    assembly.newObject("Assembly::JointGroup", "Joints")
    doc.recompute()
    fitView()


def _insertLink(position: int, offset: float):
    def action() -> None:
        doc = activeDoc()
        assembly = lastOfType(doc, "Assembly::AssemblyObject")
        body = _bodies()[position]
        # lo mismo que hace «insertar vínculo»: un App::Link al cuerpo dentro del ensamblaje
        link = assembly.newObject("App::Link", body.Label)
        link.LinkedObject = body
        link.Label = body.Label
        link.Placement.Base = Vector(offset, 0, 0)
        doc.recompute()
        fitView()

    return action


def _link(position: int):
    """Return the assembly link that points to the body number ``position``."""
    body = _bodies()[position]
    for obj in activeDoc().Objects:
        if obj.TypeId == "App::Link" and obj.LinkedObject == body:
            return obj
    raise RuntimeError("Falta el vínculo de la pieza: seguí los cuadros en orden.")


def _assemblyHelpers():
    """Return the helpers the real assembly commands use, wherever the dictionary was loaded from."""
    try:
        from Workbench.Assembly import _parametric
    except ImportError:
        from dic.Workbench.Assembly import _parametric
    return _parametric


def _offered():
    """Parts the voice list offers, in the order it shows them."""
    try:
        from Workbench._prompts import isPart
    except ImportError:
        from dic.Workbench._prompts import isPart
    return [obj for obj in activeDoc().Objects if isPart(obj)]


def _pick(language: str, *links) -> tuple:
    """Words that pick each of ``links`` from the parts list: «avanzar» up to it and «enviar».

    Args:
        language: ``"es"``, ``"en"`` or ``"pt"``.
        *links: the parts to pick, in the order the dialogs ask for them; one already
            chosen no longer shows up in the next dialog.
    """
    words: tuple = ()
    chosen: list = []
    for link in links:
        options = [obj for obj in _offered() if obj not in chosen]
        words += nextItem(language, options.index(link)) + send(language)
        chosen.append(link)
    return words


def _ground() -> None:
    parametric = _assemblyHelpers()
    import JointObject

    doc = activeDoc()
    assembly = parametric._ActiveAssembly(doc)
    # lo mismo que hace «anclar pieza»
    feature = parametric._JointGroup(assembly).newObject("App::FeaturePython", "GroundedJoint")
    JointObject.GroundedJoint(feature, _link(0))
    doc.recompute()
    parametric._RegisterObject(feature)


def _joint() -> None:
    parametric = _assemblyHelpers()
    doc = activeDoc()
    # lo mismo que hace «junta cilíndrica»
    joint = parametric._CreateJoint("Cylindrical", doc, [_link(0), _link(1)])
    if joint is None:
        raise RuntimeError("No se pudo crear la junta: seguí los cuadros en orden.")
    doc.recompute()
    parametric._RegisterObject(joint)


def _solve() -> None:
    doc = activeDoc()
    assembly = lastOfType(doc, "Assembly::AssemblyObject")
    assembly.solve()
    doc.recompute()
    # la tuerca tiene que haber vuelto sobre el eje del bulón
    if _link(1).Placement.Base.Length > 0.01:
        raise RuntimeError("El ensamblaje no encastró la tuerca en el bulón.")
    fitView()


def _isometric() -> None:
    setView("isometric")


def steps() -> list:
    """Return the frames of the bolt and nut example."""
    from InputPrompts.ExampleStep import ExampleStep

    def values(*items):
        return lambda language: numbers(language, *items)

    return [
        ExampleStep(
            Text={
                "es": "El bulón, simplificado de la DIN 931: primero el vástago, un cilindro de radio 3 y 20 de alto, con el centro en (0, 0, 10).",
                "en": "The bolt, simplified from DIN 931: first the shank, a cylinder with radius 3 and height 20, centred at (0, 0, 10).",
                "pt": "O parafuso, simplificado da DIN 931: primeiro a haste, um cilindro de raio 3 e 20 de altura, com o centro em (0, 0, 10).",
            },
            Path={
                "es": ("banco", "diseño", "sumar", "cilindro"),
                "en": ("workbench", "design", "add", "cylinder"),
                "pt": ("trabalho", "design", "aditivo", "cilindro"),
            },
            Values=values(SHANK_RADIUS, SHANK_LENGTH, 0, 0, SHANK_LENGTH // 2),
            Action=_shank,
        ),
        ExampleStep(
            Text={
                "es": "La cabeza hexagonal: un prisma de 6 lados, radio 6 y 4 de alto, centro en (0, 0, 22). Como ya hay un cuerpo, se responde «no» a «¿cuerpo nuevo?» y se elige el existente.",
                "en": "The hex head: a 6-sided prism, radius 6 and 4 high, centred at (0, 0, 22). There is a body already, so answer “no” to “new body?” and pick the existing one.",
                "pt": "A cabeça sextavada: um prisma de 6 lados, raio 6 e 4 de altura, centro em (0, 0, 22). Como já há um corpo, responda «não» a «corpo novo?» e escolha o existente.",
            },
            Path={"es": ("prisma",), "en": ("prism",), "pt": ("prisma",)},
            Values=lambda language: numbers(language, 6, HEX_RADIUS, HEAD_HEIGHT, 0, 0, SHANK_LENGTH + HEAD_HEIGHT // 2)
            + no(language)
            + send(language),
            Action=_head,
        ),
        ExampleStep(
            Text={
                "es": "La tuerca es otra pieza: un prisma de 6 lados, radio 6 y 5 de alto, centro en (0, 0, 4), sobre el mismo eje del bulón. Esta vez se responde «sí» a «¿cuerpo nuevo?».",
                "en": "The nut is another part: a 6-sided prism, radius 6 and 5 high, centred at (0, 0, 4), on the same axis as the bolt. This time answer “yes” to “new body?”.",
                "pt": "A porca é outra peça: um prisma de 6 lados, raio 6 e 5 de altura, centro em (0, 0, 4), sobre o mesmo eixo do parafuso. Desta vez responda «sim» a «corpo novo?».",
            },
            Path={"es": ("prisma",), "en": ("prism",), "pt": ("prisma",)},
            Values=lambda language: numbers(language, 6, HEX_RADIUS, NUT_HEIGHT, 0, 0, NUT_CENTER_Z) + yes(language),
            Action=_nut,
        ),
        ExampleStep(
            Text={
                "es": "Agujereá la tuerca: un cilindro sustractivo de radio 3 y 10 de alto, centro en (0, 0, 4). Primero «subir» un nivel, porque estás en Sumar. En la lista de cuerpos, «avanzar» una vez para elegir la tuerca.",
                "en": "Drill the nut: a subtractive cylinder with radius 3 and height 10, centred at (0, 0, 4). First go “up” one level, since you are in Add. In the list of bodies, say “next” once to pick the nut.",
                "pt": "Fure a porca: um cilindro subtrativo de raio 3 e 10 de altura, centro em (0, 0, 4). Primeiro «subir» um nível, porque você está em Aditivo. Na lista de corpos, «avancar» uma vez para escolher a porca.",
            },
            Path={
                "es": ("subir", "cortar", "cilindro"),
                "en": ("up", "cut", "cylinder"),
                "pt": ("subir", "cortar", "cilindro"),
            },
            Values=lambda language: numbers(language, SHANK_RADIUS, HOLE_HEIGHT, 0, 0, NUT_CENTER_Z)
            + nextItem(language, 1)
            + send(language),
            Action=_nutHole,
        ),
        ExampleStep(
            Text={
                "es": "Ahora el ensamblaje: creá uno nuevo.",
                "en": "Now the assembly: create a new one.",
                "pt": "Agora o conjunto: crie um novo.",
            },
            Path={
                "es": ("banco", "ensamblaje", "crear ensamblaje"),
                "en": ("workbench", "assembly", "create assembly"),
                "pt": ("trabalho", "montagem", "criar conjunto"),
            },
            Action=_createAssembly,
        ),
        ExampleStep(
            Text={
                "es": "Insertá el bulón en el ensamblaje. FreeCAD abre su cuadro de piezas, que se maneja con el mouse: el ejemplo inserta el vínculo por vos.",
                "en": "Insert the bolt into the assembly. FreeCAD opens its own parts dialog, which is used with the mouse: the example inserts the link for you.",
                "pt": "Insira o parafuso no conjunto. O FreeCAD abre sua própria janela de peças, que se usa com o mouse: o exemplo insere o link por você.",
            },
            Path={
                "es": ("insertar vinculo",),
                "en": ("insert link",),
                "pt": ("inserir link",),
            },
            Action=_insertLink(0, 0),
        ),
        ExampleStep(
            Text={
                "es": "Insertá la tuerca del mismo modo. Queda a un costado, a 30 mm del bulón.",
                "en": "Insert the nut the same way. It lands to one side, 30 mm from the bolt.",
                "pt": "Insira a porca do mesmo modo. Ela fica de lado, a 30 mm do parafuso.",
            },
            Path={
                "es": ("insertar vinculo",),
                "en": ("insert link",),
                "pt": ("inserir link",),
            },
            Action=_insertLink(1, NUT_SIDE_OFFSET),
        ),
        ExampleStep(
            Text={
                "es": "Anclá el bulón: el solver lo deja quieto y mueve la tuerca. La lista muestra primero los cuerpos y después los vínculos: «avanzar» hasta el vínculo del bulón y «enviar».",
                "en": "Ground the bolt: the solver keeps it still and moves the nut. The list shows the bodies first and then the links: say “next” up to the bolt's link and “send”.",
                "pt": "Ancore o parafuso: o solver o deixa parado e move a porca. A lista mostra primeiro os corpos e depois os links: «avancar» até o link do parafuso e «enviar».",
            },
            Path={
                "es": ("anclar pieza",),
                "en": ("ground part",),
                "pt": ("ancorar peca",),
            },
            Values=lambda language: _pick(language, _link(0)),
            Action=_ground,
        ),
        ExampleStep(
            Text={
                "es": "Unilos con una junta cilíndrica: la tuerca gira y desliza sobre el eje del bulón. Elegí primero el vínculo del bulón y después el de la tuerca; al crear la junta, la tuerca salta del costado al eje.",
                "en": "Join them with a cylindrical joint: the nut turns and slides on the bolt's axis. Pick the bolt's link first and then the nut's; when the joint is made, the nut jumps from the side onto the axis.",
                "pt": "Una-os com uma junta cilíndrica: a porca gira e desliza sobre o eixo do parafuso. Escolha primeiro o link do parafuso e depois o da porca; ao criar a junta, a porca salta do lado para o eixo.",
            },
            Path={
                "es": ("junta cilindrica",),
                "en": ("cylindrical joint",),
                "pt": ("junta cilindrica",),
            },
            Values=lambda language: _pick(language, _link(0), _link(1)),
            Action=_joint,
        ),
        ExampleStep(
            Text={
                "es": "Resolvé el ensamblaje para comprobar que todo encaja: la tuerca queda sobre el bulón.",
                "en": "Solve the assembly to check that everything fits: the nut stays on the bolt.",
                "pt": "Resolva o conjunto para conferir que tudo encaixa: a porca fica sobre o parafuso.",
            },
            Path={
                "es": ("resolver",),
                "en": ("solve",),
                "pt": ("resolver",),
            },
            Action=_solve,
        ),
        ExampleStep(
            Text={
                "es": "Mirá el conjunto terminado en la vista «tres de» (isométrica).",
                "en": "See the finished set in the isometric view.",
                "pt": "Veja o conjunto pronto na vista isométrica.",
            },
            Path={"es": ("tres de",), "en": ("isometric",), "pt": ("isometrica",)},
            Action=_isometric,
        ),
    ]
