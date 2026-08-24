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

TraduceToEn = {
    # Arc Slot with Arc Ends
    "arc slot":         arc_slot["arcends"],
    "curved ends":      arc_slot["arcends"],
    "rounded slot":     arc_slot["arcends"],
    "slot with arcs":   arc_slot["arcends"],
    "arcends":          arc_slot["arcends"],

    # Arc Slot with Flat Ends
    "flat slot":        arc_slot["flatends"],
    "straight ends":    arc_slot["flatends"],
    "rectangular slot": arc_slot["flatends"],
    "slot with flats":  arc_slot["flatends"],
    "flatends":         arc_slot["flatends"],

    # Help
    "help":             arc_slot["help"],
    "info":             arc_slot["help"],
    "options":          arc_slot["help"]
}