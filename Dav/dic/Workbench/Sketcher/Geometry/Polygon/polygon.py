# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import math

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects


def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_regular_polygon(sides: int, cx: float, cy: float, radius: float):
    doc = App.ActiveDocument
    if not doc or sides < 3:
        return
    import Part
    pts = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        pts.append(App.Vector(px, py, 0))
    pts.append(pts[0])
    sketch = getattr(doc, "ActiveObject", None)
    if sketch and getattr(sketch, "TypeId", "") == "Sketcher::SketchObject":
        for i in range(sides):
            sketch.addGeometry(Part.LineSegment(pts[i], pts[i + 1]), False)
        doc.recompute()
    else:
        poly_shape = Part.makePolygon(pts)
        feature = doc.addObject("Part::Feature", f"Polygon_{sides}")
        feature.Shape = poly_shape
        doc.recompute()


polygon = {
    'pentagon': lambda: _execute_with_objects('Sketcher_CreatePentagon'),
    'octagon': lambda: _execute_with_objects('Sketcher_CreateOctagon'),
    'regular': lambda: _execute_with_objects('Sketcher_CreateRegularPolygon'),
    'create_regular_polygon': create_regular_polygon,
    'help': ayuda,
}