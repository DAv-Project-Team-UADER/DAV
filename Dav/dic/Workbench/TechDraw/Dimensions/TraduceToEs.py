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

TraduceToEs = {
    # vertical
    "vertical":            dimensions["vertical"],
    "dimension vertical":  dimensions["vertical"],  # sinonimo
    "altura":              dimensions["vertical"],  # sinonimo
    # area
    "area":                dimensions["area"],
    "dimension area":      dimensions["area"],      # sinonimo
    "superficie":          dimensions["area"],      # sinonimo
    # fit
    "ajuste":              dimensions["fit"],
    "tolerancia":          dimensions["fit"],       # sinonimo
    "ajuste agujero":      dimensions["fit"],       # sinonimo
    # dimension
    "dimension":           dimensions["dimension"],
    "medir":               dimensions["dimension"], # sinonimo
    "medida":              dimensions["dimension"], # sinonimo
    # length
    "longitud":            dimensions["length"],
    "distancia":           dimensions["length"],    # sinonimo
    # horizontal
    "horizontal":          dimensions["horizontal"],
    "ancho":               dimensions["horizontal"], # sinonimo
    # extent
    "extension":           dimensions["extent"],
    "longitud total":      dimensions["extent"],    # sinonimo
    # radius
    "radio":               dimensions["radius"],
    "radio arco":          dimensions["radius"],    # sinonimo
    # diameter
    "diametro":            dimensions["diameter"],
    "dimension circulo":   dimensions["diameter"],  # sinonimo
    # angle
    "angulo":              dimensions["angle"],
    "dimension angular":   dimensions["angle"],     # sinonimo
    # help
    "ayuda":               dimensions["help"],
    "info":                dimensions["help"],      # sinonimo
    "opciones":            dimensions["help"],      # sinonimo
}
