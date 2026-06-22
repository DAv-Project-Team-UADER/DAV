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

from .DraftWork import draft
from .ayuda import ayuda

TraduceToEs = {
    'anotacion':  draft['annotation'],
    'anotación':  draft['annotation'],
    'nota':       draft['annotation'],
    'texto':      draft['annotation'],

    'arco':       draft['arc'],

    'curva':      draft['curve'],
    'spline':     draft['curve'],

    'circulo':    draft['circle'],
    'círculo':    draft['circle'],

    'matriz':     draft['array'],
    'patron':     draft['array'],
    'patrón':     draft['array'],
    'matriz circular': draft['array'],

    'modificar':  draft['modify'],
    'editar':     draft['modify'],
    'cambiar':    draft['modify'],

    'dimension':  draft['dimension'],
    'dimensión':  draft['dimension'],
    'medida':     draft['dimension'],
    'medir':      draft['dimension'],

    'elipse':     draft['ellipse'],
    'ovalo':      draft['ellipse'],
    'óvalo':      draft['ellipse'],

    'facebinder': draft['facebinder'],
    'binder':     draft['facebinder'],
    'aglutinante': draft['facebinder'],

    "ayuda":                draft["help"],
    "información":          draft["help"],
    "opciones":             draft["help"]

}