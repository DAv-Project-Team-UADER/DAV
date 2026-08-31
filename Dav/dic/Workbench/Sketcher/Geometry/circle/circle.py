# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects


def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_by_center_radius(x: float, y: float, radius: float):
    doc = App.ActiveDocument
    if not doc:
        return
    sketch = getattr(doc, "ActiveObject", None)
    import Part
    if sketch and getattr(sketch, "TypeId", "") == "Sketcher::SketchObject":
        sketch.addGeometry(Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), radius), False)
        doc.recompute()
    else:
        circ = doc.addObject("Part::Feature", "Circle")
        circ.Shape = Part.makeCircle(radius, App.Vector(x, y, 0), App.Vector(0, 0, 1))
        doc.recompute()


def create_by_3points(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    doc = App.ActiveDocument
    if not doc:
        return
    import Part
    p1 = App.Vector(x1, y1, 0)
    p2 = App.Vector(x2, y2, 0)
    p3 = App.Vector(x3, y3, 0)
    arc = Part.ArcOfCircle(p1, p2, p3)
    circle_shape = Part.Circle(arc.Center, App.Vector(0, 0, 1), arc.Radius)
    sketch = getattr(doc, "ActiveObject", None)
    if sketch and getattr(sketch, "TypeId", "") == "Sketcher::SketchObject":
        sketch.addGeometry(circle_shape, False)
        doc.recompute()
    else:
        circ = doc.addObject("Part::Feature", "Circle3P")
        circ.Shape = Part.makeCircle(arc.Radius, arc.Center, App.Vector(0, 0, 1))
        doc.recompute()


circle = {
    'create': lambda: _execute_with_objects('Sketcher_CreateCircle'),
    '3point': lambda: _execute_with_objects('Sketcher_Create3PointCircle'),
    'create_by_center_radius': create_by_center_radius,
    'create_by_3points': create_by_3points,
    'help': ayuda,
}