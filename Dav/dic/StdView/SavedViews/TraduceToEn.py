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

from .SavedViews import savedviews

TraduceToEn = {
    # Clear
    "clear":    savedviews["clear"],
    "erase":    savedviews["clear"],
    "remove":   savedviews["clear"],
    "reset":    savedviews["clear"],

    # Freeze
    "freeze":   savedviews["freeze"],
    "lock":     savedviews["freeze"],
    "hold":     savedviews["freeze"],
    "fix":      savedviews["freeze"],

    # Restore
    "restore":  savedviews["restore"],
    "recover":  savedviews["restore"],
    "reset view": savedviews["restore"],
    "bring back": savedviews["restore"],

    # Recall
    "recall":   savedviews["recall"],
    "remember": savedviews["recall"],
    "retrieve": savedviews["recall"],
    "call back": savedviews["recall"],

    # Load
    "load":     savedviews["load"],
    "open":     savedviews["load"],
    "fetch":    savedviews["load"],
    "bring":    savedviews["load"],

    # Save
    "save":     savedviews["save"],
    "store":    savedviews["save"],
    "keep":     savedviews["save"],
    "record":   savedviews["save"],

    # Store
    "store":    savedviews["store"],
    "archive":  savedviews["store"],
    "register": savedviews["store"],
    "keep view":savedviews["store"],

    # Help
    "help":     savedviews["help"],
    "info":     savedviews["help"],
    "options":  savedviews["help"]
}
