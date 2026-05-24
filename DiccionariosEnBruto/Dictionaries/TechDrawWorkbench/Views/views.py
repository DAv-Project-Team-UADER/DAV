import FreeCADGui as Gui
from .help import help

views = {
    'detail_view': lambda: Gui.runCommand('TechDraw_DetailView', 0),
    'broken_view': lambda: Gui.runCommand('TechDraw_BrokenView', 0),
    'clip_group': lambda: Gui.runCommand('TechDraw_ClipGroup', 0),
    'complex_section': lambda: Gui.runCommand('TechDraw_ComplexSection', 0),
    'help': help
}
