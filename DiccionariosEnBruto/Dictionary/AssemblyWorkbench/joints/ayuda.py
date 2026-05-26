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
    print('Comandos disponibles en joints:')
    print('PRECONDICIÓN CRÍTICA: Todos requieren elementos geométricos seleccionados en dos piezas diferentes previamente.')
    print('  fixed         - Crea una unión fija')
    print('  revolute      - Crea una unión de revolución')
    print('  cylindrical   - Crea una unión cilíndrica')
    print('  slider        - Crea una unión de deslizamiento')
    print('  ball          - Crea una unión esférica')
    print('  distance      - Crea una unión de distancia')
    print('  parallel      - Crea una unión paralela')
    print('  perpendicular - Crea una unión perpendicular')
