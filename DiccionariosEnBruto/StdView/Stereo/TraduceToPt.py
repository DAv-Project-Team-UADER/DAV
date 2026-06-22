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

from .stereo import stereo

TraduceToPt = {
    # camerapos
    "posicao camera":         stereo["camerapos"],
    "posicao vista camera":   stereo["camerapos"],  # sinonimo
    # stereocolumns
    "colunas estereo":        stereo["stereocolumns"],
    "colunas entrelacadas":   stereo["stereocolumns"],  # sinonimo
    # stereorows
    "linhas estereo":         stereo["stereorows"],
    "linhas entrelacadas":    stereo["stereorows"],     # sinonimo
    # stereooff
    "estereo desligado":      stereo["stereooff"],
    "desativar estereo":      stereo["stereooff"],      # sinonimo
    # stereoquad
    "estereo quad":           stereo["stereoquad"],
    "buffer quad":            stereo["stereoquad"],     # sinonimo
    # stereoanaglyph
    "anaglifo estereo":       stereo["stereoanaglyph"],
    "estereo vermelho verde": stereo["stereoanaglyph"], # sinonimo
    # help
    "ajuda":                  stereo["help"],
    "informacao":             stereo["help"],           # sinonimo
    "opcoes":                 stereo["help"],           # sinonimo
}
