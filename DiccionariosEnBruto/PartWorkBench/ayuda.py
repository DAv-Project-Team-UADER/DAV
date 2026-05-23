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

from .box.ayuda      import ayuda as ayuda_box
from .circle.ayuda   import ayuda as ayuda_circle
from .cone.ayuda     import ayuda as ayuda_cone
from .cube.ayuda     import ayuda as ayuda_cube
from .cylinder.ayuda import ayuda as ayuda_cylinder
from .ellipse.ayuda  import ayuda as ayuda_ellipse
from .line.ayuda     import ayuda as ayuda_line


def ayuda():
    ayuda_box()
    print()
    ayuda_circle()
    print()
    ayuda_cone()
    print()
    ayuda_cube()
    print()
    ayuda_cylinder()
    print()
    ayuda_ellipse()
    print()
    ayuda_line()