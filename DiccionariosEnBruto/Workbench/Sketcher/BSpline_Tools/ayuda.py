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

    print('  convert to nurbs - Convierte líneas, arcos, círculos')
    print('                      y otras geometrías en curvas')
    print('                      B-Spline (NURBS) editables.')
    print('                      Requiere: croquis activo en')
    print('                                 modo edición y una')
    print('                                 o más geometrías')
    print('                                 seleccionadas.')

    print('  decrease degree - Disminuye el grado matemático')
    print('                    de una curva B-Spline.')
    print('                    Requiere: croquis activo en')
    print('                               modo edición y una')
    print('                               o más B-Splines')
    print('                               seleccionadas.')

    print('  increase degree - Aumenta el grado matemático')
    print('                    de una curva B-Spline sin')
    print('                    alterar su forma visible.')
    print('                    Requiere: croquis activo en')
    print('                               modo edición y una')
    print('                               o más B-Splines')
    print('                               seleccionadas.')

    print('  insert knot - Inserta un nuevo nudo (knot)')
    print('                en una posición paramétrica')
    print('                específica de una B-Spline.')
    print('                Requiere: croquis activo y una')
    print('                           curva B-Spline.')
    
    print('  join curve - Fusiona dos curvas o aristas')
    print('               conectadas en un único')
    print('               B-Spline continuo.')
    print('               Requiere: croquis activo en')
    print('                          modo edición y un')
    print('                          vértice coincidente')
    print('                          seleccionado.')