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

"""Sentinel actions for Browser navigation (not FreeCAD commands).

Browser reacts to these verbs on every phrase, before looking the phrase up
in the current spoken context: go up one level, describe where the user
currently is, and confirm or discard the phrase being dictated. They are
represented as distinct no-arg callables (not raw strings) so Browser can
match them by identity and the spoken words stay entirely in
NavCommands/TraduceTo*.py — no word is hardcoded in browser.py.
"""


def GoUp() -> None:
    """Sentinel: ascend one level in the navigation stack."""
    return None


def ShowContext() -> None:
    """Sentinel: describe the current navigation context."""
    return None


def Send() -> None:
    """Sentinel: confirm the phrase dictated so far.

    Cierra la frase que el usuario venia dictando (el ``enviar`` al final de
    «archivo nuevo enviar»). Vive aca, y no en el codigo, para que agregar un
    sinonimo sea editar un TraduceTo*.py como con cualquier otro comando.
    """
    return None


def Cancel() -> None:
    """Sentinel: discard the phrase in progress."""
    return None


NavActions = {
    "up":            GoUp,
    "show_context":  ShowContext,
    "send":          Send,
    "cancel":        Cancel,
}
