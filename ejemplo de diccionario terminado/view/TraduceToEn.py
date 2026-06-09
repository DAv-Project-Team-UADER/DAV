import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToEn = {
    'docked panel': lambda: Gui.runCommand('Std_PanelView', 0),
    'show panel': lambda: Gui.runCommand('Std_PanelView', 0),
    'dock view': lambda: Gui.runCommand('Std_DockView', 0),
    'fullscreen': lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'undock view': lambda: Gui.runCommand('Std_UndockView', 0),
    'load image': lambda: Gui.runCommand('Std_ViewLoadImage', 0),
    'workbench': lambda: Gui.activateWorkbench("PartDesignWorkbench"), 
    'help': ayuda,
    'assistance': ayuda,
}
