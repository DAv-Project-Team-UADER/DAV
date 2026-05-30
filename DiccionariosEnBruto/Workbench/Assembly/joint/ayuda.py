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


def ayuda():
    print('=== Joint ===')
    print('  angle:         Crea una restriccion de angulo entre dos entidades geometricas. | Req: ensamblaje activo.')
    print('  ball:          Crea una union esferica (rotula) entre dos piezas.              | Req: ensamblaje activo.')
    print('  parallel:      Crea una restriccion de paralelismo entre dos entidades.        | Req: ensamblaje activo.')
    print('  perpendicular: Crea una restriccion de perpendicularidad (90°) entre piezas.  | Req: ensamblaje activo.')
    print('  belt:          Crea una union de correa que acopla dos Revolute joints.        | Req: dos Revolute joints previos.')
    print('  gears:         Crea una union de engranajes que acopla dos Revolute joints.    | Req: dos Revolute joints previos.')
    print('  rackpinion:    Crea una union pinon-cremallera (Slider + Revolute).            | Req: un Slider y un Revolute joint previos.')
    print('  screw:         Crea una union helicoidal (tornillo de avance).                 | Req: un Slider y un Revolute joint previos.')