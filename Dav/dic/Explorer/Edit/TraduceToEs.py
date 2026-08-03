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

from .Edit import edit

TraduceToEs = {
    # Comandos de Deshacer / Rehacer
    "deshacer":         edit["undo"],
    "revertir":         edit["undo"],
    "volver atrás":     edit["undo"],
    "rehacer":          edit["redo"],
    "avanzar":          edit["redo"],

    # Comandos de Portapapeles y Selección
    "cortar":           edit["cut"],
    "copiar":           edit["copy"],
    "pegar":            edit["paste"],
    "duplicar":         edit["duplicate"],
    "clonar":           edit["duplicate"],
    "seleccionar todo": edit["selectall"],
    "capturar todo":    edit["selectall"],
    "eliminar":         edit["delete"],
    "quitar":           edit["delete"],
    "borrar":           edit["delete"],

    # Comandos de Transformación y Posicionamiento
    "colocación":       edit["placement"],
    "posición":         edit["placement"],
    "establecer posición": edit["placement"],
    "transformar":      edit["transform"],
    "mover":            edit["transform"],
    "alinear":          edit["align"],
    "alineación":       edit["align"],

    # Interfaz y Configuración
    "preferencias":     edit["preferences"],
    "configuración":    edit["preferences"],
    "propiedades":      edit["properties"],
    "detalles":         edit["properties"],
    "enviar a python":  edit["sendtopython"],
    "consola python":   edit["sendtopython"],
    "modo edición":     edit["editmode"],
    "modo modificar":   edit["editmode"],

    # Estandarización de Ayuda
    "ayuda":            edit["help"],
    "información":      edit["help"],
    "opciones":         edit["help"]
}

