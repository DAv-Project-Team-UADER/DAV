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
from .dimension.dimension   import dimension
from .length.length         import length
from .horizontal.horizontal import horizontal
from .extent.extent         import extent
from .radius.radius         import radius
from .diameter.diameter     import diameter
from .angle.angle           import angle
from .ayuda import ayuda

dimensions = {
    'vertical': lambda: Gui.runCommand('TechDraw_VerticalDimension', 0),
    'area': lambda: Gui.runCommand('TechDraw_AreaDimension', 0),
    'fit': lambda: Gui.runCommand('TechDraw_HoleShaftFit', 0)
}

dimensions.update(dimension)
dimensions.update(length)
dimensions.update(horizontal)
dimensions.update(extent)
dimensions.update(radius)
dimensions.update(diameter)
dimensions['angle'] = angle
dimensions['help']  = ayuda