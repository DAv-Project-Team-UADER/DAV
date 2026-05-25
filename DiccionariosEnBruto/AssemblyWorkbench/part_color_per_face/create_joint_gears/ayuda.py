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
    print('Comandos disponibles en este nivel:')
    print('  crear union de engranajes / union de engranajes / acoplar engranajes - Crea una unión de engranajes (gears joint).')
    print('         Requiere: Workbench Assembly activo y un Ensamblaje activo.')
    print('                   REQUISITO OBLIGATORIO: Deben existir previamente dos Revolute joints en el ensamblaje.')
    print('         Devuelve: Abre el panel de tareas para configurar radios de paso. Crea un objeto Gears bajo Joints.')
    print('         Nota: No crea la geometría, sólo impone el acoplamiento cinemático entre dos piezas que ya rotan.')
