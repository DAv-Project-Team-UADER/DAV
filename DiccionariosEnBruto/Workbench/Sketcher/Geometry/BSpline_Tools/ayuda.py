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

    print('  tonurbs  - Convierte geometrías en curvas B-Spline (NURBS) editables.')
    print('             Requiere: croquis activo, una o más geometrías seleccionadas.')

    print('  decrease - Disminuye el grado matemático de una curva B-Spline.')
    print('             Requiere: croquis activo, una o más B-Splines seleccionadas.')

    print('  increase - Aumenta el grado matemático de una B-Spline sin alterar su forma.')
    print('             Requiere: croquis activo, una o más B-Splines seleccionadas.')

    print('  knot     - Inserta un nuevo nudo en una posición paramétrica de una B-Spline.')
    print('             Requiere: croquis activo y una curva B-Spline.')

    print('  join     - Fusiona dos curvas conectadas en un único B-Spline continuo.')
    print('             Requiere: croquis activo, vértice coincidente seleccionado.')