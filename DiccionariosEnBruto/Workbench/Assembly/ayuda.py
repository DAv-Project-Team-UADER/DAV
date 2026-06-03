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

from .joint.ayuda import ayuda as ayuda_joint

def ayuda():
    print('=== AssemblyWorkbench ===')
    print('  create:      Crea un nuevo objeto de ensamblaje raiz en el documento activo.')
    print('  newpart:     Crea e inserta una nueva pieza vacia dentro del ensamblaje activo.')
    print('  link:        Inserta un vinculo a una pieza existente en el ensamblaje activo.')
    print('  solve:       Recalcula y aplica todas las restricciones geometricas del ensamblaje.')
    print('  view:        Crea una vista explosionada de los componentes del ensamblaje.')
    print('  simulation:  Crea un contenedor de simulacion para definir movimientos entre piezas.')
    print('  bom:         Genera una lista de materiales con todos los componentes del ensamblaje.')
    print('  preferences: Abre el panel de configuracion global del workbench Assembly.')
    print('  grounded:    Fija/libera la posicion de una pieza en el ensamblaje (toggle).')
    print('  joint:       Subconjunto de uniones entre piezas.')
    print()
    ayuda_joint()