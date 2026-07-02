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

TraduceToEs = {
    # camerapos
    "posicion camara":       stereo["camerapos"],
    "posicion vista camara": stereo["camerapos"],  # sinonimo
    # stereocolumns
    "columnas estereo":      stereo["stereocolumns"],
    "columnas entrelazadas": stereo["stereocolumns"],  # sinonimo
    # stereorows
    "filas estereo":         stereo["stereorows"],
    "filas entrelazadas":    stereo["stereorows"],     # sinonimo
    # stereooff
    "estereo apagado":       stereo["stereooff"],
    "desactivar estereo":    stereo["stereooff"],      # sinonimo
    # stereoquad
    "estereo cuadruple":     stereo["stereoquad"],
    "buffer cuadruple":      stereo["stereoquad"],     # sinonimo
    # stereoanaglyph
    "anaglifo estereo":      stereo["stereoanaglyph"],
    "estereo rojo verde":    stereo["stereoanaglyph"],  # sinonimo
    # help
    "ayuda":                 stereo["help"],
    "informacion":           stereo["help"],            # sinonimo
    "opciones":               stereo["help"],           # sinonimo
}
