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

import FreeCAD as App
import FreeCADGui as Gui

from createobjects import CreateObjects
from .ayuda import ayuda


def point():
    Gui.runCommand("Draft_Point", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def polygon():
    Gui.runCommand("Draft_Polygon", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def rectangle():
    Gui.runCommand("Draft_Rectangle", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


creation = {
    "help": ayuda,
    "hatch": lambda: Gui.runCommand("Draft_Hatch", 0),
    "point": point,
    "polygon": polygon,
    "rectangle": rectangle,
}
