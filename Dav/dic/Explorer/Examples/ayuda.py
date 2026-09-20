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
# SPDX-License-Identifier: GPL-3.0-or-later

from .._help_gui import show_help_dialog

def ayuda():
    content = """Comandos disponibles en Ejemplos:
  manual    - Abre el manual de usuario (en portugués abre el de inglés)
  ejemplos  - Elegí un ejemplo (Croquis, Draft, Rótulo, TechDraw, PartDesign, Dado, Arandela o Bulón-tuerca)
              con retroceder, avanzar y enviar. Cada cuadro te dice qué decir,
              igual que lo dirías para dibujarlo: el camino por los menús y los
              valores. Al decirlo todo, la acción se ejecuta en FreeCAD."""
    show_help_dialog("Ejemplos", content)
