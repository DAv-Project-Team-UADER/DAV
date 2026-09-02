# Copyright (C) 2026 El Equipo del Proyecto DAV
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

"""English spoken-word mapping for Browser navigation commands."""

from .NavActions import NavActions

TraduceToEn = {
    # Go up one level
    "up":             NavActions["up"],
    "go up":          NavActions["up"],
    "back":           NavActions["up"],
    "go back":        NavActions["up"],
    "return":         NavActions["up"],
    "exit":           NavActions["up"],

    # Show the active context
    "context":        NavActions["show_context"],
    "where am i":     NavActions["show_context"],
    "what can i say": NavActions["show_context"],
    "available options": NavActions["show_context"],
    "show context":   NavActions["show_context"],
    "location":       NavActions["show_context"],

    # Confirm the dictated phrase
    "send":           NavActions["send"],
    "enter":          NavActions["send"],
    "accept":         NavActions["send"],
    "confirm":        NavActions["send"],
    "ok":             NavActions["send"],
    "okey":           NavActions["send"],
    "okay":           NavActions["send"],
    "done":           NavActions["send"],
    "yes":            NavActions["send"],
    "yep":            NavActions["send"],

    # Discard the phrase in progress
    "cancel":         NavActions["cancel"],
    "discard":        NavActions["cancel"],
    "never mind":     NavActions["cancel"],
    "abort":          NavActions["cancel"],
    "no":             NavActions["cancel"],
}
