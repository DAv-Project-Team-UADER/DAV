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
    print('Comandos y subconjuntos disponibles en el nivel raíz de Geometry:')

    print('  line        - Subconjunto para la creación de líneas rectas.')
    print('  polyline    - Subconjunto para la creación de polilíneas (líneas compuestas).')
    print('  rectangle   - Subconjunto para la creación de rectángulos.')
    print('  circle      - Subconjunto para la creación de círculos.')
    print('  arc         - Subconjunto para la creación de arcos circulares.')
    print('  arc_slot    - Subconjunto para la creación de ranuras curvas.')
    print('  ellipse     - Subconjunto para la creación de elipses.')
    print('  polygon     - Subconjunto para la creación de polígonos regulares.')
    print('  hexagon     - Subconjunto para la creación de hexágonos.')
    print('  heptagon    - Subconjunto para la creación de heptágonos.')
    print('  bspline     - Subconjunto para la creación de curvas B-Spline.')
    print('  tools       - Herramientas de edición y modificación de B-Splines.')

    print('')
    print('  new         - Crea un nuevo sketch.')
    print('  edit        - Abre la ventana DAV y dicta el nombre del sketch a editar.')
    print('  attach      - Abre la ventana DAV y dicta el sketch y la cara/soporte para adjuntarlo.')
    print('  grid        - Alterna la grilla del Sketcher.')

    print('')
    print('              (Ejecutar ayuda de cada subconjunto para ver sus comandos en detalle)')
