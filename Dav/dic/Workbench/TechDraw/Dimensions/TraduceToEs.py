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

from .dimensions import dimensions
from .dimension.dimension   import dimension
from .length.length         import length
from .horizontal.horizontal import horizontal
from .extent.extent         import extent
from .radius.radius         import radius
from .diameter.diameter     import diameter
from .angle.angle           import angle

TraduceToEs = {
    # vertical
    "vertical":            dimensions["vertical"],
    "dimensión vertical":  dimensions["vertical"],  
    "altura":              dimensions["vertical"],  

    # area
    "area":                dimensions["area"],
    "dimensión area":      dimensions["area"],      
    "superficie":          dimensions["area"],    

    # fit
    "ajuste":              dimensions["fit"],
    "tolerancia":          dimensions["fit"],       
    "ajuste agujero":      dimensions["fit"],     

    # dimension
    "dimensión":           dimension,
    "medir":               dimension, 
    "medida":              dimension, 

    # length
    "longitud":            length,
    "distancia":           length,   

    # horizontal
    "horizontal":          horizontal,
    "ancho":               horizontal, 

    # extent
    "extensión":           extent,
    "longitud total":      extent,    

    # radius
    "radio":               radius,
    "radio arco":          radius,    

    # diameter
    "diámetro":            diameter,
    "dimensión círculo":   diameter,  

    # angle
    "ángulo":              angle,
    "dimensión angular":   angle,     

    # help
    "ayuda":               dimensions["help"],
    "información":         dimensions["help"],      
    "opciones":            dimensions["help"]      
}
