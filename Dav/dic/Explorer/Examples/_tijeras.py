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

"""Assembly example: scissors made of 5 parts (2 blades, 2 handles and a pin), joined in an assembly.

The full voice guide, with the open assembly and the ANSI B drawing, is ``Dav/docs/en/voice-scissors-guide.md``.
"""

import FreeCAD as App

from ._bulontuerca import _assemblyHelpers, _connectors, _offered, _pick, _pickBody
from ._common import activeDoc, attachAt, fitView, lastOfType, setView
from ._words import down, nextItem, no, numbers, send, yes

TITLE = {
    "es": "Tijera de 5 piezas",
    "en": "Five-part scissors",
    "pt": "Tesoura de 5 peças",
}

# La tijera yace en el plano XY y el eje del perno es Z. Medidas en mm.
THICK = 2
BLADE_A = ((80, 0), (-10, -16), (-26, 14))  # punta, base y cola de la hoja A
BLADE_B = ((80, 0), (-10, 16), (-26, -14))  # espejo de la hoja A en Y
TANG_RADIUS, HOLE_RADIUS, RING_RADIUS, RING_HEIGHT = 10, 8, 14, 4
HANDLE_X, HANDLE_Y = -32, 18  # centro del mango A; el B va en -Y
PIN_A, PIN_B = 2, 1.8  # perno escalonado: la hoja B queda 2 mm sobre la A sin juntas de posición
CUT_HEIGHT = 10


def _bodies() -> list:
    return [obj for obj in activeDoc().Objects if obj.TypeId == "PartDesign::Body"]


def _links() -> list:
    """The assembly links in the order they were inserted: blade A, blade B, handle A, handle B, pin."""
    return [obj for obj in activeDoc().Objects if obj.TypeId == "App::Link"]


def _additiveHelpers():
    try:
        from Workbench.PartDesign.additive import _parametric
    except ImportError:
        from dic.Workbench.PartDesign.additive import _parametric
    return _parametric


def _profiles() -> list:
    """Drawings the «extruir por medida» list offers, in the order it shows them."""
    try:
        from Workbench._prompts import isProfile
    except ImportError:
        from dic.Workbench._prompts import isProfile
    return [obj for obj in activeDoc().Objects if isProfile(obj)]


# ---------------------------------------------------------------- acciones de las piezas


def _triangle(vertices):
    def action() -> None:
        import Part

        doc = activeDoc()
        points = [App.Vector(x, y, 0) for x, y in vertices]
        shape = Part.makePolygon(points + [points[0]])
        feature = doc.addObject("Part::Feature", "Triangle")
        feature.Shape = shape
        doc.recompute()
        fitView()

    return action


def _pad() -> None:
    doc = activeDoc()
    triangle = [obj for obj in doc.Objects if obj.TypeId == "Part::Feature" and obj.Name.startswith("Triangle")][-1]
    helpers = _additiveHelpers()
    # lo mismo que hace «extruir por medida»: el dibujo suelto se pasa a croquis y se extruye
    profile = helpers._ResolveProfile(doc, triangle)
    triangle.Visibility = False
    helpers._PadProfile(doc, profile, THICK)
    fitView()


def _cylinder(kind: str, bodyIndex: int, newBody: bool, radius, height, x, y, z):
    def action() -> None:
        doc = activeDoc()
        if newBody:
            body = doc.addObject("PartDesign::Body", "Body")
        else:
            body = _bodies()[bodyIndex]
        cyl = doc.addObject(f"PartDesign::{kind}Cylinder", "Cylinder")
        cyl.Radius, cyl.Height = radius, height
        body.addObject(cyl)
        # el cilindro nace con su base en el origen: el centro dictado queda a media altura
        attachAt(body, cyl, x, y, z - height / 2)
        doc.recompute()
        fitView()

    return action


# ---------------------------------------------------------------- acciones del ensamblaje


def _createAssembly() -> None:
    doc = activeDoc()
    assembly = doc.addObject("Assembly::AssemblyObject", "Assembly")
    assembly.Type = "Assembly"
    assembly.newObject("Assembly::JointGroup", "Joints")
    doc.recompute()
    fitView()


def _insertLink(position: int):
    def action() -> None:
        doc = activeDoc()
        assembly = lastOfType(doc, "Assembly::AssemblyObject")
        _assemblyHelpers()._InsertLink(doc, assembly, _bodies()[position])
        fitView()

    return action


def _ground() -> None:
    parametric = _assemblyHelpers()
    import JointObject

    doc = activeDoc()
    assembly = parametric._ActiveAssembly(doc)
    feature = parametric._JointGroup(assembly).newObject("App::FeaturePython", "GroundedJoint")
    JointObject.GroundedJoint(feature, _links()[4])
    doc.recompute()
    parametric._RegisterObject(feature)


def _faceName(link, radius: float) -> str:
    """Name of the cylinder face of ``link`` with that radius, as the voice list shows it."""
    for name, label in _connectors().listConnectors(link):
        if label == f"Cilindro de radio {radius:g}":
            return name
    raise RuntimeError(f"La pieza no tiene un cilindro de radio {radius:g}.")


def _facePosition(link, radius: float) -> int:
    names = [name for name, _label in _connectors().listConnectors(link)]
    return names.index(_faceName(link, radius))


def _joint(kind: str, first: int, second: int, radiusFirst: float, radiusSecond: float):
    def action() -> None:
        parametric = _assemblyHelpers()
        doc = activeDoc()
        links = [_links()[first], _links()[second]]
        joint = parametric._CreateJoint(
            kind, doc, links, [_faceName(links[0], radiusFirst), _faceName(links[1], radiusSecond)]
        )
        if joint is None:
            raise RuntimeError("No se pudo crear la junta: seguí los cuadros en orden.")
        doc.recompute()
        parametric._RegisterObject(joint)

    return action


def _solve() -> None:
    doc = activeDoc()
    assembly = lastOfType(doc, "Assembly::AssemblyObject")
    assembly.solve()
    doc.recompute()
    # la hoja B tiene que haber subido sobre la A, que el perno escalonado apila
    if abs(_links()[1].Placement.Base.z - _links()[0].Placement.Base.z - THICK) > 0.01:
        raise RuntimeError("El ensamblaje no apiló la hoja B sobre la A.")
    fitView()


def _isometric() -> None:
    setView("isometric")


# ---------------------------------------------------------------- cuadros


def _jointWords(language: str, first: int, second: int, radiusFirst: float, radiusSecond: float) -> tuple:
    """Words of a joint: the two parts from the list and then the face of each one."""
    links = _links()
    return (
        _pick(language, links[first], links[second])
        + down(language, _facePosition(links[first], radiusFirst))
        + send(language)
        + down(language, _facePosition(links[second], radiusSecond))
        + send(language)
    )


def steps() -> list:
    """Return the frames of the scissors example."""
    from InputPrompts.ExampleStep import ExampleStep

    def frame(text, path, action, values=None):
        return ExampleStep(Text=text, Path=path, Values=values, Action=action)

    def say(es, en, pt):
        return {"es": es, "en": en, "pt": pt}

    def route(es, en, pt):
        return {"es": es, "en": en, "pt": pt}

    sketchPath = route(
        ("banco", "croquis", "geometría", "triángulo", "triángulo por vértices"),
        ("workbench", "sketch", "geometry", "triangle", "triangle by vertices"),
        ("trabalho", "croqui", "geometria", "triângulo", "triângulo por vértices"),
    )
    padPath = route(
        ("subir", "subir", "subir", "diseño", "sumar", "extruir por medida"),
        ("up", "up", "up", "design", "add", "extrude by length"),
        ("subir", "subir", "subir", "projeto", "aditivo", "extrudar por medida"),
    )
    addPath = route(("cilindro por medidas",), ("cylinder by size",), ("cilindro por medidas",))
    cutPath = route(
        ("subir", "cortar", "cortar cilindro por medidas"),
        ("up", "cut", "cut cylinder by size"),
        ("subir", "cortar", "cortar cilindro por medidas"),
    )
    cutAgainPath = route(
        ("cortar cilindro por medidas",), ("cut cylinder by size",), ("cortar cilindro por medidas",)
    )
    toAddPath = route(
        ("subir", "sumar", "cilindro por medidas"),
        ("up", "add", "cylinder by size"),
        ("subir", "aditivo", "cilindro por medidas"),
    )

    def cyl(kind, body, new, radius, height, x, y, z, newBody):
        """Values of a cylinder: the five numbers and then «cuerpo nuevo» and the body when it is not new."""

        def values(language):
            words = numbers(language, radius, height, x, y, z)
            if kind == "Additive":
                words += yes(language) if new else no(language) + nextItem(language, body) + send(language)
            else:
                words += nextItem(language, body) + send(language)
            return words

        return values

    def padValues(language):
        profiles = _profiles()
        triangle = [o for o in profiles if o.Name.startswith("Triangle")][-1]
        return numbers(language, THICK) + nextItem(language, profiles.index(triangle)) + send(language)

    frames = []

    # --- hoja A y hoja B -----------------------------------------------------------------
    for index, (name, vertices, sign) in enumerate((("A", BLADE_A, 1), ("B", BLADE_B, -1))):
        flat = [value for vertex in vertices for value in vertex]
        pivot = PIN_A if name == "A" else PIN_B
        frames += [
            frame(
                say(
                    f"Hoja {name}: un triángulo por vértices, {vertices[0]}, {vertices[1]} y {vertices[2]}. Es la hoja con su cola.",
                    f"Blade {name}: a triangle by vertices, {vertices[0]}, {vertices[1]} and {vertices[2]}. It is the blade with its tail.",
                    f"Lâmina {name}: um triângulo por vértices, {vertices[0]}, {vertices[1]} e {vertices[2]}. É a lâmina com a cauda.",
                ),
                sketchPath if index == 0 else route(
                    ("subir", "subir", "croquis", "geometría", "triángulo", "triángulo por vértices"),
                    ("up", "up", "sketch", "geometry", "triangle", "triangle by vertices"),
                    ("subir", "subir", "croqui", "geometria", "triângulo", "triângulo por vértices"),
                ),
                _triangle(vertices),
                lambda language, flat=flat: numbers(language, *flat),
            ),
            frame(
                say(
                    f"Extruí el triángulo 2 mm: nace el cuerpo de la hoja {name}. En la lista de dibujos elegí el último, el que acabás de hacer.",
                    f"Extrude the triangle 2 mm: the body of blade {name} is born. In the list of drawings pick the last one, the one you just made.",
                    f"Extrude o triângulo 2 mm: nasce o corpo da lâmina {name}. Na lista de desenhos escolha o último, o que acabou de fazer.",
                ),
                padPath,
                _pad,
                padValues,
            ),
            frame(
                say(
                    f"La lengüeta donde se agarra el mango: un cilindro de radio {TANG_RADIUS} y {THICK} de alto, centro en ({HANDLE_X}, {sign * HANDLE_Y}, 1). Decí «no» a «¿cuerpo nuevo?» y elegí la hoja en la lista.",
                    f"The tang that holds the handle: a cylinder with radius {TANG_RADIUS} and height {THICK}, centred at ({HANDLE_X}, {sign * HANDLE_Y}, 1). Say “no” to “new body?” and pick the blade in the list.",
                    f"A lingueta que segura o cabo: um cilindro de raio {TANG_RADIUS} e {THICK} de altura, centro em ({HANDLE_X}, {sign * HANDLE_Y}, 1). Diga «nao» a «corpo novo?» e escolha a lâmina na lista.",
                ),
                route(("subir", "subir", "diseño", "sumar", "cilindro por medidas"), ("up", "up", "design", "add", "cylinder by size"), ("subir", "subir", "projeto", "aditivo", "cilindro por medidas")),
                _cylinder("Additive", index, False, TANG_RADIUS, THICK, HANDLE_X, sign * HANDLE_Y, THICK / 2),
                cyl("Additive", index, False, TANG_RADIUS, THICK, HANDLE_X, sign * HANDLE_Y, THICK / 2, False),
            ),
            frame(
                say(
                    f"El agujero del perno: un cilindro sustractivo de radio {pivot}, centro en (0, 0, 1). Primero «subir», porque estás en Sumar. Elegí la hoja en la lista.",
                    f"The pin hole: a subtractive cylinder with radius {pivot}, centred at (0, 0, 1). First go “up”, since you are in Add. Pick the blade in the list.",
                    f"O furo do pino: um cilindro subtrativo de raio {pivot}, centro em (0, 0, 1). Primeiro «subir», porque você está em Aditivo. Escolha a lâmina na lista.",
                ),
                cutPath,
                _cylinder("Subtractive", index, False, pivot, CUT_HEIGHT, 0, 0, THICK / 2),
                cyl("Subtractive", index, False, pivot, CUT_HEIGHT, 0, 0, THICK / 2, False),
            ),
            frame(
                say(
                    f"El hueco de la lengüeta: un cilindro sustractivo de radio {HOLE_RADIUS}, mismo centro que la lengüeta. Sobre este hueco irá la junta fija del mango.",
                    f"The hollow of the tang: a subtractive cylinder with radius {HOLE_RADIUS}, same centre as the tang. The handle's fixed joint will go on this hollow.",
                    f"O vazio da lingueta: um cilindro subtrativo de raio {HOLE_RADIUS}, mesmo centro da lingueta. A junta fixa do cabo irá neste vazio.",
                ),
                cutAgainPath,
                _cylinder("Subtractive", index, False, HOLE_RADIUS, CUT_HEIGHT, HANDLE_X, sign * HANDLE_Y, THICK / 2),
                cyl("Subtractive", index, False, HOLE_RADIUS, CUT_HEIGHT, HANDLE_X, sign * HANDLE_Y, THICK / 2, False),
            ),
        ]

    # --- mangos -----------------------------------------------------------------------------
    for index, (name, sign) in enumerate((("A", 1), ("B", -1)), start=2):
        frames += [
            frame(
                say(
                    f"Mango {name}: un anillo, o sea un cilindro de radio {RING_RADIUS} y {RING_HEIGHT} de alto, centro en ({HANDLE_X}, {sign * HANDLE_Y}, 1). Es otra pieza: decí «sí» a «¿cuerpo nuevo?».",
                    f"Handle {name}: a ring, that is a cylinder with radius {RING_RADIUS} and height {RING_HEIGHT}, centred at ({HANDLE_X}, {sign * HANDLE_Y}, 1). It is another part: say “yes” to “new body?”.",
                    f"Cabo {name}: um anel, ou seja, um cilindro de raio {RING_RADIUS} e {RING_HEIGHT} de altura, centro em ({HANDLE_X}, {sign * HANDLE_Y}, 1). É outra peça: diga «sim» a «corpo novo?».",
                ),
                route(("subir", "sumar", "cilindro por medidas"), ("up", "add", "cylinder by size"), ("subir", "aditivo", "cilindro por medidas")),
                _cylinder("Additive", index, True, RING_RADIUS, RING_HEIGHT, HANDLE_X, sign * HANDLE_Y, THICK / 2),
                cyl("Additive", index, True, RING_RADIUS, RING_HEIGHT, HANDLE_X, sign * HANDLE_Y, THICK / 2, True),
            ),
            frame(
                say(
                    f"El hueco del mango {name}: cilindro sustractivo de radio {HOLE_RADIUS}, mismo centro. Elegí el mango en la lista de cuerpos.",
                    f"The hollow of handle {name}: a subtractive cylinder with radius {HOLE_RADIUS}, same centre. Pick the handle in the list of bodies.",
                    f"O vazio do cabo {name}: cilindro subtrativo de raio {HOLE_RADIUS}, mesmo centro. Escolha o cabo na lista de corpos.",
                ),
                cutPath,
                _cylinder("Subtractive", index, False, HOLE_RADIUS, CUT_HEIGHT, HANDLE_X, sign * HANDLE_Y, THICK / 2),
                cyl("Subtractive", index, False, HOLE_RADIUS, CUT_HEIGHT, HANDLE_X, sign * HANDLE_Y, THICK / 2, False),
            ),
        ]

    # --- perno --------------------------------------------------------------------------------
    frames += [
        frame(
            say(
                "El perno es escalonado. Primero la cabeza: cilindro de radio 5 y 2 de alto, centro en (0, 0, -1). Pieza nueva: «sí».",
                "The pin is stepped. First the head: a cylinder with radius 5 and height 2, centred at (0, 0, -1). New part: “yes”.",
                "O pino é escalonado. Primeiro a cabeça: cilindro de raio 5 e 2 de altura, centro em (0, 0, -1). Peça nova: «sim».",
            ),
            toAddPath,
            _cylinder("Additive", 4, True, 5, THICK, 0, 0, -1),
            cyl("Additive", 4, True, 5, THICK, 0, 0, -1, True),
        ),
        frame(
            say(
                f"El eje que pasa por la hoja A: radio {PIN_A}, {THICK} de alto, centro en (0, 0, 1). «No» a cuerpo nuevo y elegí el perno en la lista.",
                f"The shaft through blade A: radius {PIN_A}, height {THICK}, centred at (0, 0, 1). “No” to new body and pick the pin in the list.",
                f"O eixo que passa pela lâmina A: raio {PIN_A}, altura {THICK}, centro em (0, 0, 1). «Nao» a corpo novo e escolha o pino na lista.",
            ),
            addPath,
            _cylinder("Additive", 4, False, PIN_A, THICK, 0, 0, THICK / 2),
            cyl("Additive", 4, False, PIN_A, THICK, 0, 0, THICK / 2, False),
        ),
        frame(
            say(
                f"El eje de la hoja B, un poco más fino: radio {PIN_B}, {THICK} de alto, centro en (0, 0, 3). Así el ensamblaje apila la hoja B 2 mm sobre la A.",
                f"The shaft of blade B, a little thinner: radius {PIN_B}, height {THICK}, centred at (0, 0, 3). That way the assembly stacks blade B 2 mm above A.",
                f"O eixo da lâmina B, um pouco mais fino: raio {PIN_B}, altura {THICK}, centro em (0, 0, 3). Assim o conjunto empilha a lâmina B 2 mm sobre a A.",
            ),
            addPath,
            _cylinder("Additive", 4, False, PIN_B, THICK, 0, 0, 3 * THICK / 2),
            cyl("Additive", 4, False, PIN_B, THICK, 0, 0, 3 * THICK / 2, False),
        ),
    ]

    # --- ensamblaje cerrado ------------------------------------------------------------------
    frames.append(
        frame(
            say(
                "Ahora el ensamblaje: creá uno nuevo.",
                "Now the assembly: create a new one.",
                "Agora o conjunto: crie um novo.",
            ),
            route(("subir", "subir", "ensamblaje", "crear ensamblaje"), ("up", "up", "assembly", "create assembly"), ("subir", "subir", "montagem", "criar conjunto")),
            _createAssembly,
        )
    )
    parts = (("la hoja A", "blade A", "a lâmina A"), ("la hoja B", "blade B", "a lâmina B"), ("el mango A", "handle A", "o cabo A"), ("el mango B", "handle B", "o cabo B"), ("el perno", "the pin", "o pino"))
    for position, (es, en, pt) in enumerate(parts):
        frames.append(
            frame(
                say(
                    f"Insertá {es}: en la lista de cuerpos elegí el número {position + 1}.",
                    f"Insert {en}: in the list of bodies pick number {position + 1}.",
                    f"Insira {pt}: na lista de corpos escolha o número {position + 1}.",
                ),
                route(("insertar vínculo",), ("insert link",), ("inserir link",)),
                _insertLink(position),
                lambda language, position=position: _pickBody(language, position),
            )
        )
    frames += [
        frame(
            say(
                "Anclá el perno: el solver lo deja quieto y mueve lo demás. En la lista, «avanzar» hasta el vínculo del perno (después de los cinco cuerpos) y «enviar».",
                "Ground the pin: the solver keeps it still and moves the rest. In the list say “next” up to the pin's link (after the five bodies) and “send”.",
                "Ancore o pino: o solver o deixa parado e move o resto. Na lista, «próximo» até o link do pino (depois dos cinco corpos) e «enviar».",
            ),
            route(("anclar pieza",), ("ground part",), ("ancorar peca",)),
            _ground,
            lambda language: _pick(language, _links()[4]),
        ),
        frame(
            say(
                "Articulá el perno con la hoja A con una bisagra: elegí los dos vínculos y, en cada uno, el cilindro de radio 2 (el del eje y el del agujero).",
                "Hinge the pin to blade A: pick both links and, in each, the cylinder of radius 2 (the shaft and the hole).",
                "Articule o pino com a lâmina A com uma dobradiça: escolha os dois links e, em cada um, o cilindro de raio 2 (o do eixo e o do furo).",
            ),
            route(("bisagra",), ("hinge",), ("dobradiça",)),
            _joint("Revolute", 4, 0, PIN_A, PIN_A),
            lambda language: _jointWords(language, 4, 0, PIN_A, PIN_A),
        ),
        frame(
            say(
                "Lo mismo con la hoja B, por los cilindros de radio 1,8. La hoja B salta 2 mm hacia arriba.",
                "The same with blade B, through the cylinders of radius 1.8. Blade B jumps 2 mm up.",
                "O mesmo com a lâmina B, pelos cilindros de raio 1,8. A lâmina B sobe 2 mm.",
            ),
            route(("bisagra",), ("hinge",), ("dobradiça",)),
            _joint("Revolute", 4, 1, PIN_B, PIN_B),
            lambda language: _jointWords(language, 4, 1, PIN_B, PIN_B),
        ),
        frame(
            say(
                "Unite la hoja A con su mango con un ensamble fijo, por los huecos de radio 8.",
                "Join blade A to its handle with a fixed joint, through the hollows of radius 8.",
                "Una a lâmina A ao seu cabo com uma junta fixa, pelos vazios de raio 8.",
            ),
            route(("ensamble fijo",), ("fixed joint",), ("junta fixa",)),
            _joint("Fixed", 0, 2, HOLE_RADIUS, HOLE_RADIUS),
            lambda language: _jointWords(language, 0, 2, HOLE_RADIUS, HOLE_RADIUS),
        ),
        frame(
            say(
                "Y la hoja B con su mango, igual.",
                "And blade B with its handle, the same way.",
                "E a lâmina B com o seu cabo, igual.",
            ),
            route(("ensamble fijo",), ("fixed joint",), ("junta fixa",)),
            _joint("Fixed", 1, 3, HOLE_RADIUS, HOLE_RADIUS),
            lambda language: _jointWords(language, 1, 3, HOLE_RADIUS, HOLE_RADIUS),
        ),
        frame(
            say(
                "Resolvé el ensamblaje para comprobar que todo encaja: la hoja B queda apilada sobre la A.",
                "Solve the assembly to check that everything fits: blade B is stacked on A.",
                "Resolva o conjunto para conferir que tudo encaixa: a lâmina B fica empilhada sobre a A.",
            ),
            route(("resolver",), ("solve",), ("resolver",)),
            _solve,
        ),
        frame(
            say(
                "Mirá la tijera terminada: decí «tres de» (vista isométrica). La versión abierta al 50 % y el plano ANSI están en la guía guia-tijeras-voz.md. Después decí «enviar» para cerrar el ejemplo.",
                "See the finished scissors: say “isometric”. The version open at 50 % and the ANSI drawing are in the guide guia-tijeras-voz.md. Then say “send” to close the example.",
                "Veja a tesoura pronta: diga «isometrica». A versão aberta a 50 % e o desenho ANSI estão no guia guia-tijeras-voz.md. Depois diga «enviar» para fechar o exemplo.",
            ),
            {"es": ("tres de",), "en": ("isometric",), "pt": ("isométrica",)},
            _isometric,
        ),
    ]
    return frames
