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

from .annotation import annotation

TraduceToPt = {
    # Text
    "texto":             annotation["text"],
    "adicionar texto":   annotation["text"],
    "escrever":          annotation["text"],
    
    # ShapeString
    "texto 3d":          annotation["shapestring"],
    "texto sólido":      annotation["shapestring"],
    "texto físico":      annotation["shapestring"],
    "texto superficial": annotation["shapestring"],
    "esculpir texto":    annotation["shapestring"],
    
    # Label
    "rótulo":            annotation["label"],

    "etiqueta":          annotation["label"],
    "colocar rótulo":    annotation["label"],
    
    "ajuda":             annotation["help"],
    "informação":       annotation["help"],
    "opções":             annotation["help"]
}