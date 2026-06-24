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

from .Tools import tools

TraduceToEs = {
    "medir": tools["measure"],
    "medida": tools["measure"],
    "medir distancia": tools["measure"],

    "aclarar seleccion": tools["clarifyselection"],
    "aclarar selección": tools["clarifyselection"],
    "limpiar seleccion": tools["clarifyselection"],
    "limpiar selección": tools["clarifyselection"],

    "modo demo": tools["demomode"],
    "modo demostracion": tools["demomode"],
    "modo demostración": tools["demomode"],

    "personalizar": tools["customize"],
    "configuracion": tools["customize"],
    "configuración": tools["customize"],

    "editar parametros": tools["editparameters"],
    "editar parámetros": tools["editparameters"],
    "parametros": tools["editparameters"],
    "parámetros": tools["editparameters"],

    "utilidad de proyecto": tools["projectutil"],
    "utilidades de proyecto": tools["projectutil"],
    "herramientas de proyecto": tools["projectutil"],

    "ayuda": tools["help"],
    "información": tools["help"],
    "opciones": tools["help"],
}