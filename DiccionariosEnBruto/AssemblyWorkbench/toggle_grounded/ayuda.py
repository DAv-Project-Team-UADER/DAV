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
    print('  anclar pieza / fijar pieza / inmovilizar pieza - Fija la posición y orientación de una o más piezas.')
    print('         Requiere: Workbench Assembly y Ensamblaje activos. Al menos una pieza seleccionada.')
    print('         Devuelve: Crea un objeto GroundedJoint. La pieza queda inmovilizada.')
    print('         Nota: Es el paso previo obligatorio en un flujo de ensamblaje (anclar una pieza base). Ejecutar de nuevo desactiva el anclaje.')
