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

from .Stereo import stereo

TraduceToEn = {
    # camerapos
    "camera position":      stereo["camerapos"],
    "view camera position": stereo["camerapos"],  
    "issue cam position":   stereo["camerapos"],  

    # stereocolumns
    "stereo columns":       stereo["stereocolumns"],
    "interleaved columns":  stereo["stereocolumns"],  
    "column stereo mode":   stereo["stereocolumns"], 

    # stereorows
    "stereo rows":          stereo["stereorows"],
    "interleaved rows":     stereo["stereorows"],     
    "row stereo mode":      stereo["stereorows"],   

    # stereooff
    "stereo off":           stereo["stereooff"],
    "disable stereo":       stereo["stereooff"],      
    "turn off stereo":      stereo["stereooff"],    

    # stereoquad
    "stereo quad":          stereo["stereoquad"],
    "quad buffer":          stereo["stereoquad"],     
    "quad buffer stereo":   stereo["stereoquad"],   

    # stereoanaglyph
    "stereo anaglyph":      stereo["stereoanaglyph"],
    "red green stereo":     stereo["stereoanaglyph"], 
    "anaglyph mode":        stereo["stereoanaglyph"], 

    # help
    "help":                 stereo["help"],
    "info":                 stereo["help"],           
    "options":              stereo["help"],           
}
