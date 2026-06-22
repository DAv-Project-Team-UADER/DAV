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

"""Mapeo de palabras en español para TechDraw Page."""

from .page import page
from .ayuda import ayuda

TraduceToEs = {

    # Página por defecto
    "página": page["default"],
    "pagina": page["default"],
    "página por defecto": page["default"],
    "crear página": page["default"],
    "nueva página": page["default"],

    # Plantilla
    "plantilla": page["template"],
    "plantilla de página": page["template"],
    "usar plantilla": page["template"],

    # Redibujar
    "redibujar": page["redraw"],
    "actualizar página": page["redraw"],
    "refrescar página": page["redraw"],

    # Imprimir
    "imprimir": page["print"],
    "imprimir todo": page["print"],

    # Exportar DXF
    "dxf": page["dxf"],
    "formato de intercambio de dibujo": page["dxf"],
    "guardar dxf": page["dxf"],
    "exportar dxf": page["dxf"],
    "guardar formato de intercambio de dibujo": page["dxf"],
    "exportar formato de intercambio de dibujo": page["dxf"],

    # Exportar SVG
    "svg": page["svg"],
    "exportar svg": page["svg"],
    "guardar svg": page["svg"],
    "exportar formato svg": page["svg"],
    "guardar formato svg": page["svg"],
    "formato svg": page["svg"],
    "gráficos vectoriales escalables": page["svg"],
    "exportar gráficos vectoriales escalables": page["svg"],
    "guardar gráficos vectoriales escalables": page["svg"],

    # Ayuda
    "ayuda": ayuda,
}
