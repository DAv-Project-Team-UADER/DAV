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

"""Spanish spoken-word mapping for the Sketcher point dictionary."""

from .point import point

TraduceToEs = {
    "crear": point['create'],
    "punto": point['create'],
    "nodo": point['create'],
    "crear punto": point['create'],
    "dibujar punto": point['create'],
    "crear nodo": point['create'],
    "dibujar nodo": point['create'],
    "crear punto por coordenadas": point['create_by_coords'],
    "punto por coordenadas": point['create_by_coords'],
    "crear nodo por coordenadas": point['create_by_coords'],
    "nodo por coordenadas": point['create_by_coords'],

    "ayuda": point['help'],
    "informacion": point['help'],
    "opciones": point['help'],
}