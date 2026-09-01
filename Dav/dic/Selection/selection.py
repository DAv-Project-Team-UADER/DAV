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
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.util
import sys
from pathlib import Path

import FreeCAD as App

from .ayuda import ayuda


def _load_object_selection():
    """Dynamically import ObjectSelection from Dav/scr/selection/."""
    scr_selection = Path(__file__).resolve().parents[2] / "scr" / "selection"
    if str(scr_selection) not in sys.path:
        sys.path.insert(0, str(scr_selection))
    spec = importlib.util.spec_from_file_location(
        "object_selection", scr_selection / "object_selection.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ObjectSelection


ObjectSelection = _load_object_selection()
SelectorInstance = ObjectSelection()


def SelectNext():
    """Selects the next object from the active document."""
    SelectorInstance.SelectNext()


def SelectPrevious():
    """Selects the previous object from the active document."""
    SelectorInstance.SelectPrevious()


def SelectAll():
    """Selects all objects in the active document."""
    SelectorInstance.SelectAll()


def DeselectAll():
    """Clears the current selection."""
    SelectorInstance.DeselectAll()


def CurrentObject():
    """Prints the name of the object at the current index."""
    Name = SelectorInstance.GetCurrentObject()
    if Name:
        print(f"Current object: {Name}")
    else:
        print("No objects loaded. Say 'next' or 'previous' to start.")


def ObjectCount():
    """Prints the number of objects in the selection list."""
    Count = SelectorInstance.GetObjectCount()
    if Count:
        print(f"Objects in list: {Count}")
    else:
        print("No objects loaded. Say 'next' or 'previous' to start.")


selection = {
    'next': SelectNext,
    'previous': SelectPrevious,
    'selectall': SelectAll,
    'deselectall': DeselectAll,
    'current': CurrentObject,
    'count': ObjectCount,
    'help': ayuda,
}
