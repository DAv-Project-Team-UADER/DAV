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

TraduceToEs = {
    # camerapos
    "posición cámara":       stereo["camerapos"],
    "posición vista cámara": stereo["camerapos"],  
    "guardar posición vista": stereo["camerapos"], 

    # stereocolumns
    "columnas estereo":      stereo["stereocolumns"],
    "columnas entrelazadas": stereo["stereocolumns"],  
    "modo columnas":         stereo["stereocolumns"],  

    # stereorows
    "filas estereo":         stereo["stereorows"],
    "filas entrelazadas":    stereo["stereorows"],     
    "modo filas":            stereo["stereorows"],  

    # stereooff
    "estereo apagado":       stereo["stereooff"],
    "desactivar estereo":    stereo["stereooff"],      
    "apagar estereo":        stereo["stereooff"],    

    # stereoquad
    "estereo cuádruple":     stereo["stereoquad"],
    "buffer cuádruple":      stereo["stereoquad"],     
    "modo cuádruple":        stereo["stereoquad"],   

    # stereoanaglyph
    "anaglifo estereo":      stereo["stereoanaglyph"],
    "estereo rojo verde":    stereo["stereoanaglyph"], 
    "modo anaglifo":         stereo["stereoanaglyph"], 
    
    # help
    "ayuda":                 stereo["help"],
    "informacion":           stereo["help"],           
    "opciones":              stereo["help"],            
}
