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


def _cross_sections():
    """Open the Cross Sections dialog for the selected Part object.

    There is no Document API equivalent — this tool generates section
    curves interactively via a panel; requires user input to define planes.
    """
    sel = Gui.Selection.getSelection()
    if not sel:
        return
    Gui.runCommand('Part_CrossSections', 0)


part_cross_sections = {
    'secciones transversales': _cross_sections,
    'cross sections': _cross_sections,
    'help': ayuda,
}