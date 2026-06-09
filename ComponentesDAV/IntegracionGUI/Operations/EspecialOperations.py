#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.

"""Operaciones especiales invocadas por el reconocedor de voz.

Cada función tiene la firma (a, b) esperada por el backend de voz.
Implementa acciones sobre la ventana principal de FreeCAD y el árbol de objetos.
"""
from __future__ import annotations

try:
    import FreeCAD
except Exception:  # pragma: no cover - FreeCAD may not be importable in tests
    FreeCAD = None

import FreeCADGui
from PySide6.QtWidgets import QTreeView
from PySide6.QtCore import QItemSelectionModel


def _get_tree_view() -> QTreeView | None:
    """Try to locate the main object tree view (Combo View / Tree) in FreeCAD main window."""
    try:
        mw = FreeCADGui.getMainWindow()
        if mw is None:
            return None
        trees = mw.findChildren(QTreeView)
        if not trees:
            return None
        # Prefer a widget whose name contains 'tree' or 'Tree'
        for t in trees:
            try:
                if 'tree' in t.objectName().lower():
                    return t
            except Exception:
                continue
        # Fallback: return first found
        return trees[0]
    except Exception:
        return None


def Minimize(a, b):
    """Minimizar la ventana principal de FreeCAD."""
    try:
        mw = FreeCADGui.getMainWindow()
        if mw is not None:
            mw.showMinimized()
            if FreeCAD is not None:
                FreeCAD.Console.PrintMessage("Interfaz: ventana minimizada.\n")
    except Exception as e:
        if FreeCAD is not None:
            FreeCAD.Console.PrintError(f"Minimize error: {e}\n")


def Maximize(a, b):
    """Maximizar la ventana principal de FreeCAD."""
    try:
        mw = FreeCADGui.getMainWindow()
        if mw is not None:
            # If already maximized, restore; otherwise maximize.
            try:
                if mw.isMaximized():
                    mw.showNormal()
                    if FreeCAD is not None:
                        FreeCAD.Console.PrintMessage("Interfaz: restaurada a tamaño normal.\n")
                else:
                    mw.showMaximized()
                    if FreeCAD is not None:
                        FreeCAD.Console.PrintMessage("Interfaz: maximizada.\n")
            except Exception:
                mw.showMaximized()
    except Exception as e:
        if FreeCAD is not None:
            FreeCAD.Console.PrintError(f"Maximize error: {e}\n")


def Raise(a, b):
    """Mover la selección del TreeView hacia arriba (seleccionar el elemento anterior)."""
    try:
        tree = _get_tree_view()
        if tree is None:
            if FreeCAD is not None:
                FreeCAD.Console.PrintMessage("Raise: no se encontró TreeView.\n")
            return

        model = tree.model()
        sel = tree.selectionModel()
        current = sel.currentIndex()
        if not current.isValid():
            # Select first item if nothing selected
            idx = model.index(0, 0)
            if idx.isValid():
                sel.setCurrentIndex(idx, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Current)
                tree.scrollTo(idx)
            return

        parent = current.parent()
        row = current.row()
        if row > 0:
            new_idx = model.index(row - 1, 0, parent)
            if new_idx.isValid():
                sel.setCurrentIndex(new_idx, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Current)
                tree.scrollTo(new_idx)
                if FreeCAD is not None:
                    FreeCAD.Console.PrintMessage("Seleccion subida en el árbol.\n")
        else:
            # Already at top; no-op
            if FreeCAD is not None:
                FreeCAD.Console.PrintMessage("Seleccion ya está en la primera posición.\n")
    except Exception as e:
        if FreeCAD is not None:
            FreeCAD.Console.PrintError(f"Raise error: {e}\n")


def Lower(a, b):
    """Mover la selección del TreeView hacia abajo (seleccionar el siguiente elemento)."""
    try:
        tree = _get_tree_view()
        if tree is None:
            if FreeCAD is not None:
                FreeCAD.Console.PrintMessage("Lower: no se encontró TreeView.\n")
            return

        model = tree.model()
        sel = tree.selectionModel()
        current = sel.currentIndex()
        if not current.isValid():
            idx = model.index(0, 0)
            if idx.isValid():
                sel.setCurrentIndex(idx, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Current)
                tree.scrollTo(idx)
            return

        parent = current.parent()
        row = current.row()
        count = model.rowCount(parent)
        if row < count - 1:
            new_idx = model.index(row + 1, 0, parent)
            if new_idx.isValid():
                sel.setCurrentIndex(new_idx, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Current)
                tree.scrollTo(new_idx)
                if FreeCAD is not None:
                    FreeCAD.Console.PrintMessage("Seleccion bajada en el árbol.\n")
        else:
            if FreeCAD is not None:
                FreeCAD.Console.PrintMessage("Seleccion ya está en la última posición.\n")
    except Exception as e:
        if FreeCAD is not None:
            FreeCAD.Console.PrintError(f"Lower error: {e}\n")


def RedoPrevious(a, b):
    """Ejecutar el comando de rehacer de FreeCAD."""
    try:
        FreeCADGui.runCommand("Std_Redo")
        if FreeCAD is not None:
            FreeCAD.Console.PrintMessage("Rehacer ejecutado.\n")
    except Exception as e:
        if FreeCAD is not None:
            FreeCAD.Console.PrintError(f"RedoPrevious error: {e}\n")


def UndoPrevious(a, b):
    """Ejecutar el comando de deshacer de FreeCAD."""
    try:
        FreeCADGui.runCommand("Std_Undo")
        if FreeCAD is not None:
            FreeCAD.Console.PrintMessage("Deshacer ejecutado.\n")
    except Exception as e:
        if FreeCAD is not None:
            FreeCAD.Console.PrintError(f"UndoPrevious error: {e}\n")
def minimize(a, b):
    
 #   'minimize':       EspecialOperations.Minimize,
 # ACA DEBERIA IR EL CODIGO DE LA FUNCION MINIMIZE, PARA MINIMINAR LA GUI
    return a + b

def maximize(a, b):
    #   'maximize':       EspecialOperations.Maximize,
    # ACA DEBERIA IR EL CODIGO DE LA FUNCION MAXIMIZE, PARA MAXIMINAR LA GUI
    return a + b

def raise_(a, b):
    #   'raise':          EspecialOperations.Raise,
    # ACA DEBERIA IR EL CODIGO DE LA FUNCION RAISE, PARA SUBIR EN EL HISTORIAL DE OPERACIONES

    return a + b

def lower(a, b):
    #   'lower':          EspecialOperations.Lower,
    # ACA DEBERIA IR EL CODIGO DE LA FUNCION LOWER, PARA BAJAR EN EL HISTORIAL DE OPERACIONES
    return a + b

def redo_previous(a, b):
    #   'redo previous':  EspecialOperations.RedoPrevious,
    # ACA DEBERIA IR EL CODIGO DE LA FUNCION REDO_PREVIOUS, PARA REHACER LA ULTIMA OPERACION DESHECHA
    return a + b

def undo_previous(a, b):
    #   'undo previous':  EspecialOperations.UndoPrevious,
    # ACA DEBERIA IR EL CODIGO DE LA FUNCION UNDO_PREVIOUS,
    return a + b



 #   'minimize':       EspecialOperations.Minimize,
 #   'maximize':       EspecialOperations.Maximize,
 #   'raise':          EspecialOperations.Raise,
 #   'lower':          EspecialOperations.Lower,
 #   'redo previous':  EspecialOperations.RedoPrevious,
 #   'undo previous':  EspecialOperations.UndoPrevious,   