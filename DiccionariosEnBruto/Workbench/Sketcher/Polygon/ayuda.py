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
    print('=== Polygon ===')

    print('  create pentagon - Crea un pentágono regular a partir')
    print('                    de su centro y un radio de amplitud.')
    print('                    Requiere: croquis activo, centro X/Y')
    print('                               y radio.')

    print('  create octagon - Crea un octágono regular a partir')
    print('                   de su centro y un radio de amplitud.')
    print('                   Requiere: croquis activo, centro X/Y')
    print('                              y radio.')

    print('  create regular polygon - Crea un polígono regular')
    print('                           con una cantidad de lados')
    print('                           definida por el usuario.')
    print('                           Requiere: croquis activo,')
    print('                                      centro X/Y, radio')
    print('                                      y cantidad de lados.')