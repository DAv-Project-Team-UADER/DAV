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

from .._help_gui import show_help_dialog

def ayuda():
    content = """Comandos disponibles en Edición:
  deshacer   - Deshace la última acción
  rehacer    - Rehace la última acción
  cortar     - Copia y elimina la selección
  copiar     - Copia la selección
  pegar      - Pega la selección
  duplicar   - Duplica la selección
  seleccionar todo - Selecciona todos los objetos
  borrar     - Elimina la selección
  colocación - Modifica posición, rotación y escala
  transformar - Manipuladores gráficos 3D
  alinear    - Alinea objetos seleccionados
  preferencias - Abre diálogo de Preferencias
  propiedades - Muestra panel de propiedades
  enviar a python - Envía selección a consola Python
  modo edición - Activa modo de edición del objeto"""
    show_help_dialog("Edición", content)


