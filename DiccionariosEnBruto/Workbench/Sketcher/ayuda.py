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
    print('Comandos y subconjuntos disponibles en el nivel raíz de Sketcher:')
    
    print('  validate      - Subconjunto: validación de boceto')
    print('  sketcher_tools- Subconjunto: herramientas varias (borrar geometría, restricciones, etc.)')
    print('  select        - Subconjunto: selección rápida (ejes, origen)')
    print('  external      - Subconjunto: geometría externa (proyección, intersección)')
    print('  view          - Subconjunto: alineación de cámara y secciones')

    print('  line          - Subconjunto para la creación de líneas rectas en croquis.')
    print('  point         - Subconjunto para la creación de puntos en croquis.')
    print('  polyline      - Subconjunto para la creación de líneas compuestas (polilíneas).')
    print('  rectangle     - Subconjunto para la creación de rectángulos (esquinas opuestas, centrado).')
    print('  square        - Subconjunto para la creación de cuadrados regulares.')
    print('  triangle      - Subconjunto para la creación de triángulos equiláteros.')
    print('  circle        - Subconjunto para la creación de círculos.')
    print('  arc           - Subconjunto para la creación de arcos circulares.')
    print('  ellipse       - Subconjunto para la creación de elipses, parábolas e hipérbolas.')
    print('  slot          - Subconjunto para la creación de ojales (ranuras).')
    print('  arc_slot      - Subconjunto para la creación de ranuras curvas.')
    print('  oblong        - Subconjunto para la creación de oblongos.')
    print('  polygon       - Subconjunto para la creación de pentágonos, octágonos y polígonos regulares.')
    print('  bspline       - Subconjunto para la creación de curvas B-Spline.')
    print('  bspline_tools - Herramientas de edición y modificación de B-Splines.')
    print('  text          - Subconjunto para la creación de texto 2D paramétrico.')
    print('  constraints   - Subconjunto para restricciones dimensionales.')

    print('  new           - Crea un nuevo sketch.')
    print('  edit          - Edita el sketch seleccionado.')
    print('  attach        - Adjunta o mapea el sketch seleccionado.')
    print('  grid          - Alterna la grilla del Sketcher.')
    print('  stop          - Cancela la operación activa.')
    print('  leave         - Sale del modo edición del sketch.')

    print('  toggleconstruction - Alterna el estado de construcción de la geometría en el boceto activo.')
    print('  cancelediting      - Sale del modo de edición del boceto actual cancelando los cambios.')
    print('  carboncopy         - Crea una copia de la geometría de otro boceto en el activo.')
    print('  copyelements       - Copia los elementos seleccionados del boceto al portapapeles.')
    print('  cutelements        - Corta los elementos seleccionados del boceto.')
    print('  pasteelements      - Pega los elementos del portapapeles en el boceto activo.')
    print('  mirror             - Refleja los elementos seleccionados respecto a una línea o eje.')
    print('  mirrorsketch       - Refleja todo el boceto respecto a los ejes principales.')
    print('  offset             - Crea una geometría paralela a cierta distancia de los elementos seleccionados.')
    print('  movearray          - Mueve o crea copias en forma de matriz de la geometría seleccionada.')
    print('  rotatepolar        - Rota o crea copias polares de la geometría seleccionada.')
    print('  scale              - Cambia la escala de la geometría seleccionada en el boceto.')
    print('  trimedge           - Recorta una arista en el boceto usando otra geometría como límite.')
    print('  splitedge          - Divide una arista en dos partes en el punto seleccionado.')
    print('  extendedge         - Extiende una arista hasta intersectar con otra geometría del boceto.')
    print('  fillet             - Crea un redondeo (fillet) entre dos aristas adyacentes.')
    print('  chamfer            - Crea un chaflán (chamfer) entre dos aristas adyacentes.')

    print('              (Ejecutar ayuda de cada subconjunto para ver sus comandos en detalle)')
