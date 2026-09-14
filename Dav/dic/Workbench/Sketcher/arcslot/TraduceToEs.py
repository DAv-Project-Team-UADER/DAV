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

TraduceToEs = {
    # Ranura con extremos curvos
    "ranura arco":      arc_slot["arcends"],
    "extremos curvos":  arc_slot["arcends"],
    "ranura redondeada":arc_slot["arcends"],
    "slot con arcos":   arc_slot["arcends"],
    "arcends":          arc_slot["arcends"],

    # Ranura con extremos planos
    "ranura plana":     arc_slot["flatends"],
    "extremos rectos":  arc_slot["flatends"],
    "ranura rectangular": arc_slot["flatends"],
    "slot con planos":  arc_slot["flatends"],
    "flatends":         arc_slot["flatends"],

    # Ayuda
    "ayuda":            arc_slot["help"],
    "información":      arc_slot["help"],
    "opciones":         arc_slot["help"]
}
