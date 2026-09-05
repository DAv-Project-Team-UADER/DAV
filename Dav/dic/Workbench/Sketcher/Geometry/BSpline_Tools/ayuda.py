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
    print('=== B-Spline Tools ===')

    print('  tonurbs  - Convierte una geometría B-Spline en curva NURBS editable.')
    print('             Abre la ventana DAV y dicta el nombre del objeto a convertir.')

    print('  decrease - Disminuye el grado matemático de una curva B-Spline.')
    print('             Abre la ventana DAV y dicta el nombre del objeto.')

    print('  increase - Aumenta el grado matemático de una B-Spline sin alterar su forma.')
    print('             Abre la ventana DAV y dicta el nombre del objeto.')

    print('  knot     - Inserta un nudo en una posición paramétrica de una B-Spline.')
    print('             Abre la ventana DAV y dicta el nombre del objeto y la posición (0 a 1).')

    print('  join     - Fusiona dos curvas conectadas en un único B-Spline continuo.')
    print('             Abre la ventana DAV y dicta los nombres de las dos curvas.')