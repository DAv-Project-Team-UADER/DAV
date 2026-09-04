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

from ._help_gui import show_help_dialog

def ayuda():
    content = """Submenús disponibles:
  archivo        - Gestión de archivos (nuevo, abrir, guardar, importar, exportar)
  editar         - Operaciones de edición (deshacer, rehacer, cortar, copiar, pegar)
  imprimir       - Impresión y exportación a PDF
  ventanas       - Gestión de ventanas (cerrar, cerrar todo, salir)
  expresiones    - Copiar y pegar expresiones y fórmulas
  herramientas   - Herramientas auxiliares (medir, personalizar, parámetros)
  estructura     - Creación de piezas, grupos y enlaces

Comandos directos:
  refrescar      - Recarga la vista y el árbol
  foto           - Captura de pantalla de la vista activa
  texto          - Crea un documento de texto
  desvincular    - Quita el enlace del objeto seleccionado
  congelar       - Bloquea/congela el objeto seleccionado
  instancias     - Selecciona todas las instancias del objeto
  variables      - Crea un conjunto de variables (VarSet)"""
    show_help_dialog("Explorador", content)


