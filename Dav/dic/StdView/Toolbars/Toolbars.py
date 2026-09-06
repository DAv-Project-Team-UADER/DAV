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
    from PySide6.QtWidgets import QToolBar
except ImportError:
    try:
        from PySide2.QtWidgets import QToolBar
    except ImportError:
        QToolBar = None



def _find_toolbar(targets):
    """Busca un QToolBar en la ventana principal que coincida con alguno de los identificadores."""
    mw = Gui.getMainWindow()
    if not mw:
        return None

    targets_lower = [t.lower() for t in targets]
    toolbars_list = mw.findChildren(QToolBar) if QToolBar else [
        c for c in mw.findChildren(object) if hasattr(c, 'toggleViewAction')
    ]

    for tb in toolbars_list:
        obj_name = tb.objectName() or ""
        if obj_name.lower() in targets_lower:
            return tb
        title = tb.windowTitle().lower()
        if title in targets_lower:
            return tb
        action = tb.toggleViewAction()
        if action:
            text = action.text().replace('&', '').strip().lower()
            if text in targets_lower:
                return tb
    return None


def _toggle_toolbar(targets):
    """Alterna la visibilidad de una barra de herramientas (QToolBar)."""
    tb = _find_toolbar(targets)
    if tb:
        action = tb.toggleViewAction()
        if action:
            action.trigger()
        else:
            tb.setVisible(not tb.isVisible())


def _toggle_toolbar_lock():
    """Alterna el bloqueo de las barras de herramientas de forma segura en Qt."""
    import FreeCAD as App

    param = App.ParamGet("User parameter:BaseApp/Preferences/General")
    currently_locked = param.GetBool("LockToolBars", False)
    new_locked = not currently_locked
    param.SetBool("LockToolBars", new_locked)

    mw = Gui.getMainWindow()
    if not mw:
        return

    toolbars_list = mw.findChildren(QToolBar) if QToolBar else [
        c for c in mw.findChildren(object) if hasattr(c, 'setMovable')
    ]
    for tb in toolbars_list:
        tb.setMovable(not new_locked)


# Diccionario DAV - StdView / Toolbars
toolbars = {
    'clipboard':    lambda: _toggle_toolbar(['Clipboard', 'Portapapeles']),
    'edit':         lambda: _toggle_toolbar(['Edit', 'Edición', 'Edicion']),
    'file':         lambda: _toggle_toolbar(['File', 'Archivo']),
    'toolbarshelp': lambda: _toggle_toolbar(['Help', 'Ayuda']),
    'views':        lambda: _toggle_toolbar(['Individual Views', 'Views', 'Vistas individuales', 'Vistas']),
    'lock':         _toggle_toolbar_lock,
    'macro':        lambda: _toggle_toolbar(['Macro', 'Macros']),
    'structure':    lambda: _toggle_toolbar(['Structure', 'Estructura']),
    'view':         lambda: _toggle_toolbar(['View', 'Vista']),
    'workbench':    lambda: _toggle_toolbar(['Workbench', 'Bancos de trabajo', 'Banco de trabajo', 'Mesa de trabajo']),
    'help':         ayuda,
}
