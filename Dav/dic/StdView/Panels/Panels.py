# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

import FreeCADGui as Gui

from .ayuda import ayuda

try:
    from PySide6.QtWidgets import QDockWidget
except ImportError:
    try:
        from PySide2.QtWidgets import QDockWidget
    except ImportError:
        QDockWidget = None




def _find_dock(targets):
    """Busca un QDockWidget en la ventana principal que coincida con alguno de los identificadores."""
    mw = Gui.getMainWindow()
    if not mw:
        return None

    targets_lower = [t.lower() for t in targets]

    if QDockWidget:
        docks = mw.findChildren(QDockWidget)
    else:
        docks = [c for c in mw.findChildren(object) if hasattr(c, 'toggleViewAction')]

    for dock in docks:
        obj_name = dock.objectName() or ""
        if obj_name.lower() in targets_lower:
            return dock

        action = dock.toggleViewAction()
        if action:
            data = action.data()
            if data and str(data).lower() in targets_lower:
                return dock
            text = action.text().replace('&', '').strip().lower()
            if text in targets_lower:
                return dock

        title = dock.windowTitle().lower()
        if title in targets_lower:
            return dock

        w = dock.widget()
        if w:
            w_name = w.objectName() or ""
            if w_name.lower() in targets_lower:
                return dock

    return None


def _toggle_panel(targets):
    """Alterna la visibilidad de un panel acoplable (QDockWidget)."""
    dock = _find_dock(targets)
    if dock:
        action = dock.toggleViewAction()
        if action:
            action.trigger()
        else:
            dock.setVisible(not dock.isVisible())


def _dock_window():
    """Acopla la ventana activa de documento."""
    try:
        Gui.runCommand('Std_ViewDockUndockFullscreen', 0)
    except Exception:
        mw = Gui.getMainWindow()
        if mw and hasattr(mw, 'switchToDockedMode'):
            mw.switchToDockedMode()


def _undock_window():
    """Desacopla la ventana activa de documento a ventana flotante."""
    try:
        Gui.runCommand('Std_ViewDockUndockFullscreen', 1)
    except Exception:
        mw = Gui.getMainWindow()
        if mw and hasattr(mw, 'switchToTopLevelMode'):
            mw.switchToTopLevelMode()


def _toggle_fullscreen():
    """Alterna el modo de pantalla completa de la ventana principal."""
    try:
        Gui.runCommand('Std_MainFullscreen', 0)
    except Exception:
        mw = Gui.getMainWindow()
        if mw:
            if mw.isFullScreen():
                mw.showNormal()
            else:
                mw.showFullScreen()


def _toggle_statusbar():
    """Alterna la visibilidad de la barra de estado."""
    mw = Gui.getMainWindow()
    if mw:
        sb = mw.statusBar()
        if sb:
            sb.setVisible(not sb.isVisible())


# Diccionario DAV - StdView / Panels
Panels = {
    'panel':         lambda: _toggle_panel(['DAV_Panel', 'Std_ComboView', 'Model', 'Combo View']),
    'dock':          _dock_window,
    'fullscreen':    _toggle_fullscreen,
    'undock':        _undock_window,
    'dagview':       lambda: _toggle_panel(['Std_DAGView', 'DAG View', 'DAGView', 'Vista DAG']),
    'comboview':     lambda: _toggle_panel(['Std_ComboView', 'Model', 'Combo View', 'ComboView', 'Modelo', 'Vista combinada']),
    'selectionview': lambda: _toggle_panel(['Std_SelectionView', 'Selection view', 'Selection View', 'Selección', 'Vista de selección']),
    'tasks':         lambda: _toggle_panel(['Std_TaskView', 'Tasks', 'Task List', 'Std_TaskWatcher', 'Tareas']),
    'properties':    lambda: _toggle_panel(['Std_PropertyView', 'Property view', 'Property View', 'Propiedades', 'Model', 'Std_ComboView']),
    'console':       lambda: _toggle_panel(['Std_PythonView', 'Std_PythonConsole', 'Python console', 'Python Console', 'Consola Python', 'Consola']),
    'report':        lambda: _toggle_panel(['Std_ReportView', 'Report view', 'Report View', 'Informe', 'Reporte', 'Vista de informe']),
    'treeview':      lambda: _toggle_panel(['Std_TreeView', 'Tree view', 'TreeView', 'Árbol', 'Arbol', 'Model', 'Std_ComboView']),
    'statusbar':     _toggle_statusbar,
    'help':          ayuda,
}
