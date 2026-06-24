import FreeCADGui as Gui
from .ayuda import ayuda

other_views = {
    'active_view': lambda: Gui.runCommand('TechDraw_ActiveView', 0),
    'help': ayuda
}