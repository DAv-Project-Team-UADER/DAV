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


def _color_per_face():
    # Selección de objeto + caras debe hacerse en la GUI
    Gui.runCommand("Std_SetAppearance", 0)


part_color_per_face = {
    'pintar cara': lambda: _color_per_face(),
    'color por cara': lambda: _color_per_face(),
    'colorear cara': lambda: _color_per_face(),
    'help': ayuda,
}