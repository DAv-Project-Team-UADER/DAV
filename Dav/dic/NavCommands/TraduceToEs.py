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

"""Spanish spoken-word mapping for Browser navigation commands."""

from .NavActions import NavActions

TraduceToEs = {
    # Subir un nivel en la navegación
    "subir":          NavActions["up"],
    "volver":         NavActions["up"],
    "atras":          NavActions["up"],
    "atrás":          NavActions["up"],
    "salir":          NavActions["up"],
    "regresar":       NavActions["up"],
    "retroceder":     NavActions["up"],

    # Mostrar el contexto actual (sinónimos porque Vosk confunde
    # "contexto" con "contacto")
    "contexto":       NavActions["show_context"],
    "donde estoy":    NavActions["show_context"],
    "dónde estoy":    NavActions["show_context"],
    "en que estoy":   NavActions["show_context"],
    "en qué estoy":   NavActions["show_context"],
    "que puedo decir": NavActions["show_context"],
    "qué puedo decir": NavActions["show_context"],
    "opciones disponibles": NavActions["show_context"],
    "mostrar contexto": NavActions["show_context"],
    "ubicacion":      NavActions["show_context"],
    "ubicación":      NavActions["show_context"],

    # Confirmar la frase dictada. Antes estas palabras estaban repartidas
    # entre browser.py, browser_voice_adapter.py y SpokenNumberParser, y las
    # listas ya no coincidian: "aceptar" andaba dentro de un prompt numerico
    # pero no fuera, y ni siquiera entraba en la gramatica de Vosk.
    "enviar":         NavActions["send"],
    "aceptar":        NavActions["send"],
    "confirmar":      NavActions["send"],
    "entrar":         NavActions["send"],
    "ok":             NavActions["send"],

    # Descartar la frase en curso
    "cancelar":       NavActions["cancel"],
    "cancela":        NavActions["cancel"],
    "descartar":      NavActions["cancel"],
    "olvidalo":       NavActions["cancel"],
    "olvidálo":       NavActions["cancel"],
}
