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

from .ayuda import ayuda
from .._parametric import (
    angle_joint,
    ball_joint,
    belt_joint,
    cylindrical_joint,
    distance_joint,
    fixed_joint,
    gears_joint,
    parallel_joint,
    perpendicular_joint,
    rack_pinion_joint,
    revolute_joint,
    screw_joint,
    slider_joint,
)

# Las mismas uniones por voz que el nivel Assembly: las piezas y la cara de cada una se eligen
# con avanzar/okey y los valores (distancia, ángulo, radios) se dictan. Antes esta carpeta
# llamaba a los comandos nativos de FreeCAD, que piden clics sobre las caras.
joint = {
    'angle':         angle_joint,
    'ball':          ball_joint,
    'parallel':      parallel_joint,
    'perpendicular': perpendicular_joint,
    'belt':          belt_joint,
    'gears':         gears_joint,
    'rackpinion':    rack_pinion_joint,
    'screw':         screw_joint,
    'cylindrical':   cylindrical_joint,
    'distance':      distance_joint,
    'fixed':         fixed_joint,
    'revolute':      revolute_joint,
    'slider':        slider_joint,
    'help':         ayuda,
}