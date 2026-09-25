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
    content = """Comandos disponibles en Proyecto (sin diálogos nativos):
  nuevo     - Crea un documento nuevo, vacío
  abrir     - Recorre las carpetas por voz y abre el archivo elegido
              (siguiente / anterior, abrir carpeta, subir, okey, cancelar)
  guardar   - Guarda el documento; si es nuevo pide carpeta y nombre
              (nombre sugerido o deletreado)
  exportar  - Elige el formato (STEP, IGES, STL, OBJ, DXF), carpeta y nombre
              y exporta la selección o todo lo visible"""
    show_help_dialog("Proyecto", content)
