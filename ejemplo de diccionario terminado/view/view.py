import FreeCADGui as Gui
from .ayuda import ayuda

view = {
    'docked_panel': lambda: Gui.runCommand('Std_PanelView', 0),
    'dock_view': lambda: Gui.runCommand('Std_DockView', 0),
    'fullscreen': lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'undock_view': lambda: Gui.runCommand('Std_UndockView', 0),
    'load_image': lambda: Gui.runCommand('Std_ViewLoadImage', 0),
    # StdWorkbench will be handled via Gui.activateWorkbench in the translator/resolver if arguments are provided,
    # but the ticket says `Gui.activateWorkbench("NombreDelWorkbench")`. 
    # Since we can't easily pass arguments via dictionary lambda directly without custom logic,
    # we'll provide a wrapper or just the key. Let's do a basic lambda.
    'help': ayuda,
}
