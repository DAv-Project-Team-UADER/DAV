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
    print('=== Ellipse (paramétrico con ventana, como línea por puntos) ===')
    print('  center     - Elipse por centro y radios. Requiere: X,Y, major, minor (floats).')
    print('               Alias: create_by_center.')
    print('  3points    - Elipse por 3 puntos. p1-p2 = extremos eje mayor, p3 = punto para minor.')
    print('               Requiere: x1,y1,x2,y2,x3,y3 (floats). p3 no puede estar sobre recta p1-p2.')
    print('               Alias: create_by_3_points.')
    print('  elliptic   - Arco de elipse. Requiere: X,Y, major, minor, angle1, angle2 (grados).')
    print('               Alias: create_elliptic.')
    print('  hyperbolic - Arco de hipérbola axis-aligned. Requiere: X,Y, a,b, angle1,angle2 (grados).')
    print('               Alias: create_hyperbolic.')
    print('  parabolic  - Arco de parábola. Requiere: x_focus,y_focus, x_vertex,y_vertex, angle1,angle2 (grados).')
    print('               Alias: create_parabolic.')
    print('  interactive_* - Modo mouse legacy (requiere sketch activo).')