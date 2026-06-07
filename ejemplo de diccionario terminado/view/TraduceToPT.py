import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToPT = {
    'painel acoplado': lambda: Gui.runCommand('Std_PanelView', 0),
    'mostrar painel': lambda: Gui.runCommand('Std_PanelView', 0),
    'acoplar vista': lambda: Gui.runCommand('Std_DockView', 0),
    'tela cheia': lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'desacoplar vista': lambda: Gui.runCommand('Std_UndockView', 0),
    'carregar imagem': lambda: Gui.runCommand('Std_ViewLoadImage', 0),
    'ambiente': lambda: Gui.activateWorkbench("PartDesignWorkbench"),
    'ajuda': ayuda,
    'assistência': ayuda,
}
