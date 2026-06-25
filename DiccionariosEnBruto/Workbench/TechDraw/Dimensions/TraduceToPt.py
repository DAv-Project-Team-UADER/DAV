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
    "dimensao":            dimensions["dimension"],
    "medir":               dimensions["dimension"], 
    "medida":              dimensions["dimension"], 

    # length
    "comprimento":         dimensions["length"],
    "distância":           dimensions["length"],    

    # horizontal
    "horizontal":          dimensions["horizontal"],
    "largura":             dimensions["horizontal"], 

    # extent
    "extensao":            dimensions["extent"],
    "comprimento total":   dimensions["extent"],   

    # radius
    "raio":                dimensions["radius"],
    "raio arco":           dimensions["radius"],    

    # diameter
    "diametro":            dimensions["diameter"],
    "dimensao circulo":    dimensions["diameter"],  

    # angle
    "angulo":              dimensions["angle"],
    "dimensao angular":    dimensions["angle"],    

    # help
    "ajuda":               dimensions["help"],
    "informação":                dimensions["help"],      
    "opções":              dimensions["help"],      
}
