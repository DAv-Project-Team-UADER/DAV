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

from .box.box         import box
from .circle.circle   import circle
from .cone.cone       import cone
from .cube.cube       import cube
from .cylinder.cylinder import cylinder
from .ellipse.ellipse import ellipse
from .line.line       import line

partWorkbench = {}
partWorkbench.update(box)
partWorkbench.update(circle)
partWorkbench.update(cone)
partWorkbench.update(cube)
partWorkbench.update(cylinder)
partWorkbench.update(ellipse)
partWorkbench.update(line)