import Sketcher
from Common import Finish, GetActiveSketch, RequireGeometry, TryAddConstraint
from .ayuda import ayuda


def dimension():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'una línea'):
        line = 0
        TryAddConstraint(sketch, Sketcher.Constraint('Distance', line, 1, line, 2, 15.0))
        Finish(doc, 'Dimension Constraint')


def horizontal():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'una línea'):
        line = 0
        TryAddConstraint(sketch, Sketcher.Constraint('DistanceX', line, 1, line, 2, 18.0))
        Finish(doc, 'Horizontal Dimension')


def vertical():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'una línea'):
        line = 0
        TryAddConstraint(sketch, Sketcher.Constraint('DistanceY', line, 1, line, 2, 20.0))
        Finish(doc, 'Vertical Dimension')


def angle():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 2, 'dos líneas'):
        line_one, line_two = 0, 1
        TryAddConstraint(sketch, Sketcher.Constraint('Coincident', line_one, 1, line_two, 1))
        TryAddConstraint(sketch, Sketcher.Constraint('Angle', line_one, line_two, 45.0))
        Finish(doc, 'Angle Dimension')


def radius():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'un arco o círculo'):
        arc = 0
        TryAddConstraint(sketch, Sketcher.Constraint('Radius', arc, 10.0))
        Finish(doc, 'Radius Dimension')


def diameter():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'un círculo'):
        circle = 0
        TryAddConstraint(sketch, Sketcher.Constraint('Diameter', circle, 14.0))
        Finish(doc, 'Diameter Dimension')


def radiam():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'un círculo'):
        circle = 0
        TryAddConstraint(sketch, Sketcher.Constraint('Diameter', circle, 14.0))
        Finish(doc, 'Radius/Diameter Dimension')
        try:
            import FreeCADGui as Gui
            Gui.SendMsgToActiveView('ViewFit')
        except Exception:
            pass


def distance():
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, 1, 'una línea'):
        line = 0
        TryAddConstraint(sketch, Sketcher.Constraint('Distance', line, 1, line, 2, 20.0))
        Finish(doc, 'Distance Dimension')


constraints = {
    'dimension':  dimension,
    'horizontal': horizontal,
    'vertical':   vertical,
    'angle':      angle,
    'radius':     radius,
    'diameter':   diameter,
    'radiam':     radiam,
    'distance':   distance,
    'help':       ayuda,
}

