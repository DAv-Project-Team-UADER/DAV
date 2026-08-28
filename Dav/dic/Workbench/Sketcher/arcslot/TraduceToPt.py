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

from arcslot import arc_slot

TraduceToPt = {
    # Fenda com extremidades curvas
    "ranhura arco":     arc_slot["arcends"],
    "extremos curvos":  arc_slot["arcends"],
    "ranhura arredondada": arc_slot["arcends"],
    "slot com arcos":   arc_slot["arcends"],
    "arcends":          arc_slot["arcends"],

    # Fenda com extremidades planas
    "ranhura plana":    arc_slot["flatends"],
    "extremos retos":   arc_slot["flatends"],
    "ranhura retangular": arc_slot["flatends"],
    "slot com planos":  arc_slot["flatends"],
    "flatends":         arc_slot["flatends"],

    # Ajuda
    "ajuda":            arc_slot["help"],
    "informações":      arc_slot["help"],
    "opções":           arc_slot["help"]
}
