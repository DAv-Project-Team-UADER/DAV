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

TraduceToPt = {
    # vertical
    "vertical":            dimensions["vertical"],
    "dimensao vertical":   dimensions["vertical"],  
    "altura":              dimensions["vertical"],  

    # area
    "area":                dimensions["area"],
    "dimensao area":       dimensions["area"],      
    "superficie":          dimensions["area"],  

    # fit
    "ajuste":              dimensions["fit"],
    "tolerancia":          dimensions["fit"],       
    "ajuste furo":         dimensions["fit"],     

    # dimension
    "dimensao":            dimension,
    "medir":               dimension, 
    "medida":              dimension, 

    # length
    "comprimento":         length,
    "distância":           length,    

    # horizontal
    "horizontal":          horizontal,
    "largura":             horizontal, 

    # extent
    "extensao":            extent,
    "comprimento total":   extent,   

    # radius
    "raio":                radius,
    "raio arco":           radius,    

    # diameter
    "diametro":            diameter,
    "dimensao circulo":    diameter,  

    # angle
    "angulo":              angle,
    "dimensao angular":    angle,    

    # help
    "ajuda":               dimensions["help"],
    "informação":          dimensions["help"],      
    "opções":              dimensions["help"]      
}
