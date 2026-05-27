import FreeCADGui as Gui
from .help import help

other_views = {
    'active_view': lambda: Gui.runCommand('TechDraw_ActiveView', 0),
    'help': help
}