# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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
# SPDX-License-Identifier: GPL-3.0-or-later

from .._help_gui import show_help_dialog

def ayuda():
    content = """Comandos disponibles en Herramientas:
  medir             - Mide distancias y ángulos
  aclarar selección - Despliega menú para separar objetos seleccionados por tipo
  modo demo         - Activa o configura rotación continua de cámara en 3D
  personalizar      - Abre diálogo de personalización de interfaz
  editar parámetros - Abre el editor de parámetros de FreeCAD
  utilidades proyecto - Extrae y gestiona el contenido del archivo de proyecto"""
    show_help_dialog("Herramientas", content)