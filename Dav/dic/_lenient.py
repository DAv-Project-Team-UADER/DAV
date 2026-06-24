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

"""Lenient command dictionary that never raises KeyError.

A ``TraduceTo*`` file maps spoken words to command callables by looking them
up in a source dict, e.g. ``edit['screenshot']``. While the dictionaries are
still being completed, some of those keys do not exist yet. With a plain dict
a single missing key raises ``KeyError`` at import time and the whole context
(deshacer, copiar, pegar, …) is lost.

``LenientDict`` returns a harmless no-op callable for any missing key instead
of raising, so the rest of the context keeps working. Missing keys are logged
once so the team knows what is still pending.
"""

from __future__ import annotations


def _noop() -> None:
    """Comando vacío usado para claves de diccionario aún no implementadas."""
    return None


class LenientDict(dict):
    """dict that returns a no-op callable for missing keys (no KeyError).

    Example::

        edit = LenientDict({'undo': _undo_cmd})
        edit['screenshot']   # -> no-op callable, no raise
    """

    _warned: set[str] = set()

    def __missing__(self, key):  # noqa: D401 - dict protocol hook
        if key not in LenientDict._warned:
            LenientDict._warned.add(key)
            print(
                f"[DAV-Browser] Comando '{key}' aún no implementado en el "
                "diccionario; se omite (no-op)."
            )
        return _noop
