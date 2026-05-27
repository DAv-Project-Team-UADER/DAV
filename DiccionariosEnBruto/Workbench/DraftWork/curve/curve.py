import FreeCADGui as Gui
from .ayuda import ayuda

curve = {
    'bezier':  lambda: Gui.runCommand('Draft_BezCurve', 0),
    'bspline': lambda: Gui.runCommand('Draft_BSpline', 0),
    'cubic':   lambda: Gui.runCommand('Draft_CubicBezCurve', 0),
    'help':    ayuda
}