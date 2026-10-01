# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Build the scissors example (5 parts, assembly, ANSI B sheet) the way the DAV voice guide does.

Reproduce, con la API de FreeCAD, exactamente lo que la guía ``guia-tijeras-voz.md`` hace por voz:
las mismas piezas, los mismos valores y las mismas funciones de juntas de DAV. Sirve para ver cómo
debe quedar el resultado y para comprobar la guía.

Uso (con la interfaz de FreeCAD, para poder exportar el PDF)::

    "C:\\Program Files\\FreeCAD 1.1\\bin\\freecad.exe" crear_tijeras.py
"""

import os
import sys

import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector as V

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "dic")))

# ---- medidas (mm) -----------------------------------------------------------------------
HOJA = [(80, 0), (-10, -16), (-26, 14)]  # triángulo de la hoja A: punta, base, cola
ESPESOR = 2
RADIO_PERNO = 2  # el perno es escalonado: Ø4 en la hoja A y Ø3,6 en la hoja B
RADIO_LENGUETA, RADIO_ALOJ, RADIO_MANGO, ALTO_MANGO = 10, 8, 14, 4
CENTRO_MANGO = (-32, 18)  # mango A; el B va en (-32, -18)
ESCALA = 1.25  # 5:4
GAP_ABIERTA = 23.3  # separación entre mangos con la tijera abierta al 50 % (30°)

OUT = os.path.join(HERE, "tijeras_dav")


def _placeAt(body, feature, x, y, z):
    plane = next(i for i in body.Origin.OriginFeatures if i.Role == "XY_Plane")
    feature.AttachmentSupport = [(plane, "")]
    feature.MapMode = "FlatFace"
    feature.AttachmentOffset = App.Placement(V(x, y, z), App.Rotation())


def _cylinder(doc, body, kind, name, radius, height, x, y, z):
    """Same as ``cilindro por medidas`` / ``cortar cilindro por medidas``: the centre is dictated."""
    cyl = doc.addObject(f"PartDesign::{kind}Cylinder", name)
    cyl.Radius, cyl.Height = radius, height
    body.addObject(cyl)
    _placeAt(body, cyl, x, y, z - height / 2)
    doc.recompute()


def _blade(doc, label, triangle, centre):
    body = doc.addObject("PartDesign::Body", label.replace(" ", ""))
    body.Label = label
    sketch = body.newObject("Sketcher::SketchObject", "Triangulo")
    plane = next(i for i in body.Origin.OriginFeatures if i.Role == "XY_Plane")
    sketch.AttachmentSupport = [(plane, "")]
    sketch.MapMode = "FlatFace"
    for i in range(3):  # = «triángulo por vértices» + «extruir por medida»
        a, b = triangle[i], triangle[(i + 1) % 3]
        sketch.addGeometry(Part.LineSegment(V(a[0], a[1], 0), V(b[0], b[1], 0)))
    for i in range(3):
        sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 3, 1))
    doc.recompute()
    pad = body.newObject("PartDesign::Pad", "Extrusion")
    pad.Profile, pad.Length = sketch, ESPESOR
    doc.recompute()
    _cylinder(doc, body, "Additive", "Lengueta", RADIO_LENGUETA, ESPESOR, *centre, ESPESOR / 2)
    radius = RADIO_PERNO - (0.2 if label == "Hoja B" else 0)
    _cylinder(doc, body, "Subtractive", "AgujeroPerno", radius, 10, 0, 0, ESPESOR / 2)
    _cylinder(doc, body, "Subtractive", "AgujeroLengueta", RADIO_ALOJ, 10, *centre, ESPESOR / 2)
    return body


def _handle(doc, label, centre):
    body = doc.addObject("PartDesign::Body", label.replace(" ", ""))
    body.Label = label
    _cylinder(doc, body, "Additive", "Anillo", RADIO_MANGO, ALTO_MANGO, *centre, ESPESOR / 2)
    _cylinder(doc, body, "Subtractive", "Hueco", RADIO_ALOJ, 10, *centre, ESPESOR / 2)
    return body


def _bolt(doc):
    body = doc.addObject("PartDesign::Body", "Perno")
    _cylinder(doc, body, "Additive", "Cabeza", 5, 2, 0, 0, -1)
    _cylinder(doc, body, "Additive", "EjeA", RADIO_PERNO, ESPESOR, 0, 0, ESPESOR / 2)
    _cylinder(doc, body, "Additive", "EjeB", RADIO_PERNO - 0.2, ESPESOR, 0, 0, 1.5 * ESPESOR)
    return body


def buildParts(doc):
    hojaB = [(x, -y) for x, y in HOJA]
    centreB = (CENTRO_MANGO[0], -CENTRO_MANGO[1])
    return {
        "HojaA": _blade(doc, "Hoja A", HOJA, CENTRO_MANGO),
        "HojaB": _blade(doc, "Hoja B", hojaB, centreB),
        "MangoA": _handle(doc, "Mango A", CENTRO_MANGO),
        "MangoB": _handle(doc, "Mango B", centreB),
        "Perno": _bolt(doc),
    }


def buildAssembly(doc, parts):
    """Two assemblies of the 5 parts: «cerrada» (isometric view) and «abierta» (side view).

    Cada vista de TechDraw necesita un solo objeto de origen (por voz solo se elige uno a la vez),
    así que cada estado de la tijera vive en su propio ensamblaje.
    """
    import JointObject
    from Workbench.Assembly import _connectors, _parametric

    current = []
    # en FreeCAD el ensamblaje recién creado queda activo; acá se simula igual
    _parametric._ActiveAssembly = lambda _doc: current[0]

    def cylinderFace(link, radius):
        options = _connectors.listConnectors(link)
        return next(name for name, label in options if label == f"Cilindro de radio {radius:g}")

    def join(kind, first, radiusFirst, second, radiusSecond):
        joint = _parametric._CreateJoint(
            kind, doc, [first, second], [cylinderFace(first, radiusFirst), cylinderFace(second, radiusSecond)]
        )
        doc.recompute()
        _parametric._RegisterObject(joint)
        return joint

    def buildSet(name, label):
        assembly = doc.addObject("Assembly::AssemblyObject", name)  # «crear ensamblaje»
        assembly.Type = "Assembly"
        assembly.newObject("Assembly::JointGroup", "Joints")
        assembly.Label = label
        doc.recompute()
        current[:] = [assembly]
        links = {}
        for key in ("HojaA", "HojaB", "MangoA", "MangoB", "Perno"):  # «insertar vínculo» x5
            links[key] = _parametric._InsertLink(doc, assembly, parts[key])
        ground = _parametric._JointGroup(assembly).newObject("App::FeaturePython", "GroundedJoint")
        JointObject.GroundedJoint(ground, links["Perno"])  # «anclar pieza»
        doc.recompute()
        join("Revolute", links["Perno"], RADIO_PERNO, links["HojaA"], RADIO_PERNO)  # «bisagra»
        join("Revolute", links["Perno"], RADIO_PERNO - 0.2, links["HojaB"], RADIO_PERNO - 0.2)
        join("Fixed", links["HojaA"], RADIO_ALOJ, links["MangoA"], RADIO_ALOJ)  # «ensamble fijo»
        join("Fixed", links["HojaB"], RADIO_ALOJ, links["MangoB"], RADIO_ALOJ)
        return assembly, links

    closed, closedLinks = buildSet("TijeraCerrada", "Tijera cerrada")
    opened, openedLinks = buildSet("TijeraAbierta", "Tijera abierta")
    # «junta por distancia» entre los dos mangos: abre la tijera al 50 % (30°), ±15° del eje X
    handleA, handleB = openedLinks["MangoA"], openedLinks["MangoB"]
    joint = _parametric._CreateJoint(
        "Distance", doc, [handleA, handleB], [cylinderFace(handleA, RADIO_MANGO), cylinderFace(handleB, RADIO_MANGO)]
    )
    joint.Distance = GAP_ABIERTA
    doc.recompute()
    _parametric._RegisterObject(joint)
    for assembly in (closed, opened):  # «resolver ensamblaje»
        for _ in range(2):
            assembly.solve()
            doc.recompute()
    return closed, opened


def buildDrawing(doc, closed, opened):
    page = doc.addObject("TechDraw::DrawPage", "Plano")
    page.Label = "Plano ANSI B"
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Rotulo")
    template.Template = os.path.join(App.getResourceDir(), "Mod", "TechDraw", "Templates", "ASME", "ANSIB_Landscape.svg")
    page.Template = template
    page.ProjectionType = "Third angle"  # ASME Y14.3
    doc.recompute()

    def view(name, source, direction, xDirection, x, y, scale):
        item = doc.addObject("TechDraw::DrawViewPart", name)
        page.addView(item)
        item.Source = [source]
        item.Direction, item.XDirection = direction, xDirection
        item.ScaleType, item.Scale = "Custom", scale
        item.X, item.Y = x, y
        item.HardHidden = False
        doc.recompute()
        return item

    side = view("VistaLateral", opened, V(0, 0, 1), V(1, 0, 0), 105, 160, ESCALA)
    side.Label = "Vista lateral (abierta 50 %)"
    iso = view("VistaIsometrica", closed, V(1, -1, 1), V(1, 1, 0), 325, 160, ESCALA)
    iso.Label = "Vista isométrica (cerrada)"

    def note(name, text, x, y, size):
        item = doc.addObject("TechDraw::DrawViewAnnotation", name)
        page.addView(item)
        item.Text = text
        item.TextSize = size
        item.X, item.Y = x, y
        return item

    note("TituloLateral", ["VISTA LATERAL", "Abierta al 50 % (30°)"], 105, 235, 5)
    note("TituloIso", ["VISTA ISOMÉTRICA", "Cerrada"], 325, 235, 5)
    note(
        "Piezas",
        [
            "1  HOJA A ........ 1",
            "2  HOJA B ........ 1",
            "3  MANGO A ........ 1",
            "4  MANGO B ........ 1",
            "5  PERNO ........ 1",
        ],
        75,
        45,
        4,
    )
    note("EjeTxt", "EJE DE SIMETRÍA", 205, 160 + 4, 3)

    fields = {
        "CompanyName": "DAV - UADER",
        "CompanyAddress": "Concepcion del Uruguay, Entre Rios",
        "DrawingTitle1": "TIJERA",
        "DrawingTitle2": "Ensamble de 5 piezas",
        "DrawingTitle3": "Vistas lateral e isometrica",
        "DrawnBy": "DAV",
        "CheckedBy": "-",
        "Approved1": "-",
        "Approved2": "-",
        "Code": "DAV",
        "Sheet": "1 / 1",
        "Weight": "-",
        "drawing_number": "DAV-TJ-001",
        "revision_index": "A",
        "scale": "5:4",
    }
    for key, value in fields.items():
        template.setEditFieldContent(key, value)
    doc.recompute()
    return page, side, opened


def addAxisAndDimensions(side, opened):
    """Symmetry axis (centre line through the pivot) and the overall dimensions of the side view.

    Hay que hacerlo con la hoja ya dibujada en pantalla: antes la vista no tiene geometría y
    FreeCAD no crea la línea.
    """
    doc = side.Document
    link = next(o for o in opened.Group if o.isDerivedFrom("App::Link") and o.LinkedObject.Label == "Perno")
    pivot, centre = link.Placement.Base, side.getGeometricCenter()
    # las coordenadas 2D de la vista se miden desde el centro de su caja
    start = V(pivot.x - 60 / ESCALA - centre.x, pivot.y - centre.y, 0)
    end = V(pivot.x + 118 / ESCALA - centre.x, pivot.y - centre.y, 0)
    tag = side.makeCosmeticLine(start, end)
    if tag:
        pass  # estilo por defecto de FreeCAD para líneas cosméticas
    else:
        print("No se pudo crear el eje de simetría")
    import TechDraw

    TechDraw.makeExtentDim(side, [], 0)  # largo total
    TechDraw.makeExtentDim(side, [], 1)  # alto total
    for dim in (o for o in doc.Objects if o.TypeId == "TechDraw::DrawViewDimExtent"):
        # fuera de la figura: el largo debajo, el alto a la izquierda
        dim.X, dim.Y = (0, -75) if dim.Type == "DistanceX" else (-78, 0)
    doc.recompute()


def main():
    doc = App.newDocument("Tijera")
    parts = buildParts(doc)
    doc.recompute()
    closed, opened = buildAssembly(doc, parts)
    page, side, opened = buildDrawing(doc, closed, opened)
    for item in parts.values():  # las piezas sueltas quedan ocultas: se ven dentro del ensamblaje
        item.Visibility = False
    try:
        import FreeCADGui as Gui
        import TechDrawGui

        gui = Gui.getMainWindow() is not None
    except ImportError:
        gui = False
    if gui:
        # la hoja tiene que dibujarse en pantalla antes de seguir, si no la vista no tiene geometría
        page.ViewObject.doubleClicked()
        for _ in range(20):
            Gui.updateGui()
        doc.recompute()
        for _ in range(20):
            Gui.updateGui()
    addAxisAndDimensions(side, opened)
    doc.saveAs(OUT + ".FCStd")
    if gui:
        for _ in range(20):
            Gui.updateGui()
        TechDrawGui.exportPageAsPdf(page, OUT + ".pdf")
        print("PDF exportado")


try:
    main()
except Exception:
    import traceback

    with open(OUT + ".log", "w", encoding="utf-8") as log:
        log.write(traceback.format_exc())
try:
    import FreeCADGui as Gui

    if Gui.getMainWindow() is not None:
        Gui.getMainWindow().close()
except Exception:
    pass
