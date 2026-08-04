import FreeCAD as App
import FreeCADGui as Gui

from createobjects import CreateObjects
from .ayuda import ayuda


def shape_2d_view():
    Gui.runCommand("Draft_Shape2DView", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def wire_to_bspline():
    Gui.runCommand("Draft_WireToBSpline", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


modification = {
    "scale": lambda: Gui.runCommand("Draft_Scale", 0),
    "shape_2d_view": shape_2d_view,
    "slope": lambda: Gui.runCommand("Draft_Slope", 0),
    "split": lambda: Gui.runCommand("Draft_Split", 0),
    "stretch": lambda: Gui.runCommand("Draft_Stretch", 0),
    "subelement_highlight": lambda: Gui.runCommand("Draft_SubelementHighlight", 0),
    "trimex": lambda: Gui.runCommand("Draft_Trimex", 0),
    "upgrade": lambda: Gui.runCommand("Draft_Upgrade", 0),
    "wire_to_bspline": wire_to_bspline,
    "help": ayuda,
}
