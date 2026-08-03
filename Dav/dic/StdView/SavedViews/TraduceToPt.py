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

TraduceToPt = {
    # Clear
    "limpar":    savedviews["clear"],
    "apagar":    savedviews["clear"],
    "remover":   savedviews["clear"],
    "reiniciar": savedviews["clear"],

    # Freeze
    "congelar":  savedviews["freeze"],
    "bloquear":  savedviews["freeze"],
    "fixar":     savedviews["freeze"],
    "parar":     savedviews["freeze"],

    # Restore
    "restaurar": savedviews["restore"],
    "recuperar": savedviews["restore"],
    "reiniciar vista": savedviews["restore"],
    "trazer de volta": savedviews["restore"],

    # Recall
    "recordar":  savedviews["recall"],
    "lembrar":   savedviews["recall"],
    "recuperar vista": savedviews["recall"],
    "chamar":    savedviews["recall"],

    # Load
    "carregar":  savedviews["load"],
    "abrir":     savedviews["load"],
    "trazer":    savedviews["load"],
    "importar":  savedviews["load"],

    # Save
    "salvar":    savedviews["save"],
    "guardar":   savedviews["save"],
    "manter":    savedviews["save"],
    "registrar": savedviews["save"],

    # Store
    "armazenar": savedviews["store"],
    "arquivar":  savedviews["store"],
    "registrar": savedviews["store"],
    "guardar vista": savedviews["store"],

    # Help
    "ajuda":     savedviews["help"],
    "informações": savedviews["help"],
    "opções":    savedviews["help"]
}
