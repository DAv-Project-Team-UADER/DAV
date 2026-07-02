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

from .length import length

TraduceToPt = {
    # length
    "comprimento":        length["length"],
<<<<<<< HEAD
    "dimensão comprimento": length["length"],  # sinonimo
    "distância":          length["length"],    # sinonimo
    # help
    "ajuda":              length["help"],
    "informação":               length["help"],      # sinonimo
    "opções":             length["help"],      # sinonimo
=======
    "dimensao comprimento": length["length"],  
    "distância":          length["length"],    

    # help
    "ajuda":              length["help"],
    "informação":         length["help"],      
    "opções":             length["help"],      
>>>>>>> ab0008d5c571ed323a300c3168bedfe72882654d
}
