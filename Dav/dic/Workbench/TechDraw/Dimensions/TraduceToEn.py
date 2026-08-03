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

TraduceToEn = {
    # vertical
    "vertical":           dimensions["vertical"],
    "vertical dimension": dimensions["vertical"],  
    "height":             dimensions["vertical"],  

    # area
    "area":               dimensions["area"],
    "area dimension":     dimensions["area"],      
    "surface":            dimensions["area"],    

    # fit
    "fit":                dimensions["fit"],
    "tolerance":          dimensions["fit"],       
    "hole shaft":         dimensions["fit"],  
    
    "dimension":           dimension,
    "measure":             dimension,
    "size":                dimension,

    # length
    "length":             length,
    "distance":           length,    
    "measure":            length,  

    # horizontal
    "horizontal":         horizontal,
    "width":              horizontal, 
    "x distance":         horizontal, 

    # extent
    "extent":             extent,
    "span":               extent,    
    "total length":       extent,  

    # radius
    "radius":             radius,
    "arc radius":         radius,  

    # diameter
    "diameter":           diameter,
    "circle dimension":   diameter,  

    # angle
    "angle":              angle,
    "angular":            angle,   
      
    # help
    "help":               dimensions["help"],
    "info":               dimensions["help"],   
    "options":            dimensions["help"]   
}
