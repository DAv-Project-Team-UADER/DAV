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
    print('Comandos disponibles en Edit:')
    print('  undo       - Deshace la última acción')
    print('  redo       - Rehace la última acción')
    print('  cut        - Copia y elimina la selección')
    print('  copy       - Copia la selección')
    print('  paste      - Pega la selección')
    print('  duplicate  - Duplica la selección')
    print('  selectall  - Selecciona todo')
    print('  delete     - Elimina la selección')
    print('  placement  - Abre la ventana de colocación. Permite modificar la posición, rotación y escala de los objetos seleccionados')
    print('  transform  - Abre la ventana de transformación. Permite modificar la posición, rotación y escala de los objetos seleccionados usando manipuladores gráficos en la vista 3D')
    print('  align      - Abre la ventana de alineación. Permite alinear objetos seleccionados con otros objetos o con el sistema de coordenadas global')
    print('  note       - Crea una nota de texto en la vista 3D')
    print('  screenshot - Captura la vista activa')
    print('  preferences  - Abre el diálogo de Preferencias de FreeCAD')
    print('  properties   - Muestra o enfoca el panel de propiedades (Datos y Vista) del objeto seleccionado.')
    print('  sendtopython - Envía la selección actual a la consola Python')
    print('  editmode     - Abre el modo de edición específico del objeto seleccionado')

