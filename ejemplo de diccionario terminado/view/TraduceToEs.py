import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToEs = {
    'panel acoplado': lambda: Gui.runCommand('Std_PanelView', 0),
    'mostrar panel': lambda: Gui.runCommand('Std_PanelView', 0),
    'acoplar vista': lambda: Gui.runCommand('Std_DockView', 0),
    'fijar ventana': lambda: Gui.runCommand('Std_DockView', 0),
    'pantalla completa': lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'maximizar vista': lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'desacoplar vista': lambda: Gui.runCommand('Std_UndockView', 0),
    'ventana flotante': lambda: Gui.runCommand('Std_UndockView', 0),
    'cargar imagen': lambda: Gui.runCommand('Std_ViewLoadImage', 0),
    'abrir imagen': lambda: Gui.runCommand('Std_ViewLoadImage', 0),
    # StdWorkbench requiere un parametro. Lo dejamos mapeado a una función que pueda manejar un entorno por defecto 
    # o simplemente dejamos el lambda listo si el framework de la VUI inyecta parametros.
    'entorno': lambda: Gui.activateWorkbench("PartDesignWorkbench"), # Ejemplo por defecto
    'ayuda': ayuda,
    'asistencia': ayuda,
}
