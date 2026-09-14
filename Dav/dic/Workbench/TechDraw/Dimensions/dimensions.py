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
from _lenient import LenientDict
from .dimension.dimension   import dimension
from .length.length         import length
from .horizontal.horizontal import horizontal
from .extent.extent         import extent
from .radius.radius         import radius
from .diameter.diameter     import diameter
from .angle.angle           import angle
from .ayuda import ayuda

# Subcontextos anidados: el Browser navega por niveles y espera
# dimensions['dimension'], dimensions['length'], ... como submenús (no
# aplanados), igual que Explorer/Explorer.py.
# Antes los .update() de los sub-dicts se descartaban por completo: la
# reasignación `dimensions = {...}` que venía justo después los pisaba, así
# que dimension/length/horizontal/extent/radius/diameter/angle quedaban fuera
# del diccionario.
dimensions = {
    'dimension':  dimension,
    'length':     length,
    'horizontal': horizontal,
    'extent':     extent,
    'radius':     radius,
    'diameter':   diameter,
    'angle':      angle,

    'vertical': lambda: Gui.runCommand('TechDraw_VerticalDimension', 0),
    'area': lambda: Gui.runCommand('TechDraw_AreaDimension', 0),
    'fit': lambda: Gui.runCommand('TechDraw_HoleShaftFit', 0),
    'help'  : ayuda

}

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
dimensions = LenientDict(dimensions)