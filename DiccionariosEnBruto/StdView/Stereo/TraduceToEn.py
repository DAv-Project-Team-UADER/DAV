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

from .stereo import stereo

TraduceToEn = {
    # camerapos
    "camera position":      stereo["camerapos"],
    "view camera position": stereo["camerapos"],  # synonym
    "issue cam position":   stereo["camerapos"],  # synonym
    # stereocolumns
    "stereo columns":       stereo["stereocolumns"],
    "interleaved columns":  stereo["stereocolumns"],  # synonym
    "column stereo mode":   stereo["stereocolumns"],  # synonym
    # stereorows
    "stereo rows":          stereo["stereorows"],
    "interleaved rows":     stereo["stereorows"],     # synonym
    "row stereo mode":      stereo["stereorows"],     # synonym
    # stereooff
    "stereo off":           stereo["stereooff"],
    "disable stereo":       stereo["stereooff"],      # synonym
    "turn off stereo":      stereo["stereooff"],      # synonym
    # stereoquad
    "stereo quad":          stereo["stereoquad"],
    "quad buffer":          stereo["stereoquad"],     # synonym
    "quad buffer stereo":   stereo["stereoquad"],     # synonym
    # stereoanaglyph
    "stereo anaglyph":      stereo["stereoanaglyph"],
    "red green stereo":     stereo["stereoanaglyph"], # synonym
    "anaglyph mode":        stereo["stereoanaglyph"], # synonym
    # help
    "help":                 stereo["help"],
    "info":                 stereo["help"],           # synonym
    "options":              stereo["help"],           # synonym
}
