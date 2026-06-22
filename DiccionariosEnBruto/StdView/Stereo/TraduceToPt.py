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

TraduceToPt = {
    # camerapos
    "posição câmera":         stereo["camerapos"],
    "posição vista câmera":   stereo["camerapos"],  # sinônimo
    "salvar posição vista":   stereo["camerapos"],  # sinônimo
    # stereocolumns
    "colunas estéreo":        stereo["stereocolumns"],
    "colunas entrelaçadas":   stereo["stereocolumns"],  # sinônimo
    "modo colunas":           stereo["stereocolumns"],  # sinônimo
    # stereorows
    "linhas estéreo":         stereo["stereorows"],
    "linhas entrelaçadas":    stereo["stereorows"],     # sinônimo
    "modo linhas":            stereo["stereorows"],     # sinônimo
    # stereooff
    "estéreo desligado":      stereo["stereooff"],
    "desativar estéreo":      stereo["stereooff"],      # sinônimo
    "desligar estéreo":       stereo["stereooff"],      # sinônimo
    # stereoquad
    "estéreo quad":           stereo["stereoquad"],
    "buffer quad":            stereo["stereoquad"],     # sinônimo
    "modo quad":              stereo["stereoquad"],     # sinônimo
    # stereoanaglyph
    "anáglifo estéreo":       stereo["stereoanaglyph"],
    "estéreo vermelho verde": stereo["stereoanaglyph"], # sinônimo
    "modo anáglifo":          stereo["stereoanaglyph"], # sinônimo
    # help
    "ajuda":                  stereo["help"],
    "informação":             stereo["help"],           # sinônimo
    "opções":                 stereo["help"],           # sinônimo
}
