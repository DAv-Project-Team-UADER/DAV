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

import FreeCAD as App
import Part

def GetActiveSketch():
    Doc = App.ActiveDocument
    if Doc is None:
        print("No hay documento activo.")
        return None, None
    try:
        import FreeCADGui as Gui
        for Obj in Gui.Selection.getSelection():
            if getattr(Obj, "TypeId", "") == "Sketcher::SketchObject":
                return Doc, Obj
    except Exception:
        pass
    Active = Doc.ActiveObject
    if Active is not None and getattr(Active, "TypeId", "") == "Sketcher::SketchObject":
        return Doc, Active
    print("Seleccioná un Sketch en el árbol o abrilo en edición para que sea el objeto activo.")
    return None, None

def RequireGeometry(Sketch, Minimum: int, Hint: str = "") -> bool:
    Count = len(Sketch.Geometry)
    if Count < Minimum:
        Msg = f"Este script necesita al menos {Minimum} elemento(s) de geometría en el sketch"
        if Hint:
            Msg += f" ({Hint})"
        Msg += f"; hay {Count}."
        print(Msg)
        return False
    return True

def NewSketch(SketchName: str, DocName: str = "ConstraintExamples"):
    Doc = App.ActiveDocument
    if Doc is None:
        Doc = App.newDocument(DocName)

    ExistingSketch = Doc.getObject(SketchName)
    if ExistingSketch:
        Doc.removeObject(SketchName)
        Doc.recompute()

    Sketch = Doc.addObject("Sketcher::SketchObject", SketchName)
    return Doc, Sketch

def AddLine(Sketch, X1, Y1, X2, Y2):
    return Sketch.addGeometry(Part.LineSegment(App.Vector(X1, Y1, 0), App.Vector(X2, Y2, 0)), False)

def AddCircle(Sketch, X, Y, Radius):
    return Sketch.addGeometry(Part.Circle(App.Vector(X, Y, 0), App.Vector(0, 0, 1), Radius), False)

def AddArc(Sketch, X, Y, Radius, AngleStart, AngleEnd):
    Circle = Part.Circle(App.Vector(X, Y, 0), App.Vector(0, 0, 1), Radius)
    return Sketch.addGeometry(Part.ArcOfCircle(Circle, AngleStart, AngleEnd), False)

def TryAddConstraint(Sketch, ConstraintObject):
    try:
        ConstraintIndex = Sketch.addConstraint(ConstraintObject)
        return ConstraintIndex
    except Exception as Error:
        print(f"Constraint not available in this FreeCAD build: {ConstraintObject.Type} -> {Error}")
        return -1

def Finish(Doc, Label):
    Doc.recompute()
    print(f"Done: {Label}")
