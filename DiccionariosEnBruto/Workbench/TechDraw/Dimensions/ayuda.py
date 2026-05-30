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

from .dimension.ayuda  import ayuda as ayuda_dimension
from .length.ayuda     import ayuda as ayuda_length
from .horizontal.ayuda import ayuda as ayuda_horizontal
from .extent.ayuda     import ayuda as ayuda_extent
from .radius.ayuda     import ayuda as ayuda_radius
from .diameter.ayuda   import ayuda as ayuda_diameter
from .angle.ayuda      import ayuda as ayuda_angle

def ayuda():
    print('=== Dimensions ===')
    print('  vertical : Acota la distancia vertical entre dos puntos o de una arista.')
    print('             Req: Seleccionar una arista, o bien dos vértices en la vista.')
    print('  area     : Agrega una dimensión de área a una cara seleccionada en la vista. | Req: Cara seleccionada')
    print('  fit      : Abre el panel interactivo para aplicar un ajuste normalizado ISO 286. | Req: Cota lineal seleccionada')
    print()
    ayuda_dimension()
    print()
    ayuda_length()
    print()
    ayuda_horizontal()
    print()
    ayuda_extent()
    print()
    ayuda_radius()
    print()
    ayuda_diameter()
    print()
    ayuda_angle()