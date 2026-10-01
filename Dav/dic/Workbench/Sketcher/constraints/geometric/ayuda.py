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
    print('=== Geometric Constraints ===')
    print('  coincident        - Hace coincidir dos puntos en la misma posición.')
    print('  coincidentunified - Igual que coincident por voz: se eligen los dos puntos.')
    print('  lock              - Fija un punto donde está ahora (elige boceto, elemento y punto).')
    print('  pointonobject     - Restringe un punto a estar sobre una arista o curva.')
    print('  horizontal        - Fuerza una línea o segmento a ser horizontal.')
    print('  vertical          - Fuerza una línea o segmento a ser vertical.')
    print('  horver            - Elige horizontal o vertical según la inclinación de la línea elegida.')
    print('  parallel          - Hace paralelas dos líneas o segmentos.')
    print('  perpendicular     - Hace perpendiculares dos líneas o segmentos (90°).')
    print('  tangent           - Hace tangentes dos curvas o una curva y una línea.')
    print('  equal             - Iguala la longitud o radio de dos entidades.')
    print('  symmetric         - Restringe dos puntos a ser simétricos respecto a un eje.')
    print('  block             - Bloquea la geometría en su posición actual.')
    print('  toggledriving     - Alterna una cota entre conductora y de referencia (se elige por número).')
    print('  toggleactive      - Activa o desactiva una restricción (se elige por número).')
