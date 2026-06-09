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
    print('=== Ellipse ===')
    print('  center     - Crea una elipse completa especificando centro, radio mayor y menor.')
    print('               Requiere: croquis activo, centro X/Y, radio mayor y radio menor.')
    print('  3points    - Crea una elipse a partir de los extremos de un eje y un tercer punto.')
    print('               Requiere: croquis activo y tres puntos de referencia.')
    print('  elliptic   - Crea un arco de elipse definiendo centro, radios y ángulos.')
    print('               Requiere: croquis activo, centro X/Y, radio mayor, radio menor,')
    print('               ángulo inicial y ángulo final.')
    print('  hyperbolic - Crea un arco de hipérbola usando centro, radios y parámetros de recorte.')
    print('               Requiere: croquis activo, centro X/Y, radio mayor, radio menor,')
    print('               parámetro inicial y final.')
    print('  parabolic  - Crea un arco de parábola a partir del foco, vértice y parámetros.')
    print('               Requiere: croquis activo, foco X/Y, vértice X/Y,')
    print('               parámetro inicial y parámetro final.')