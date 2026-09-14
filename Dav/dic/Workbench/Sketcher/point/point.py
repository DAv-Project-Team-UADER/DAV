# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects


def _execute_with_objects():
    Gui.runCommand('Sketcher_CreatePoint', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_by_coords(x: float, y: float):
    doc = App.ActiveDocument
    if not doc:
        return
    sketch = getattr(doc, "ActiveObject", None)
    import Part
    if sketch and getattr(sketch, "TypeId", "") == "Sketcher::SketchObject":
        sketch.addGeometry(Part.Point(App.Vector(x, y, 0)), False)
        doc.recompute()
    else:
        pt = doc.addObject("Part::Feature", "Point")
        pt.Shape = Part.Point(App.Vector(x, y, 0)).toShape()
        doc.recompute()


point = {
    'create': _execute_with_objects,
    'create_by_coords': create_by_coords,
    'help': ayuda,
}