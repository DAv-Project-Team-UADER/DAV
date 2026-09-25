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

"""Open the user manual (PDF) in the language DAV is using."""

import os
import subprocess
import sys
from pathlib import Path

# Un manual por idioma de DAV.
_MANUALS = {
    "es": "Manual_Usuario.pdf",
    "en": "User_Manual.pdf",
    "pt": "Manual_do_Usuario.pdf",
}


def _language() -> str:
    """Return the DAV language ("es", "en" or "pt"), Spanish when unknown."""
    try:
        from InputPrompts.InputPromptI18n import ResolveLanguage

        return ResolveLanguage()
    except Exception:
        return "es"


def manualPath(language: str | None = None) -> Path | None:
    """Find the manual PDF for ``language`` in the repository or installation.

    Args:
        language: ``"es"``, ``"en"`` or ``"pt"``. Defaults to the DAV language.

    Returns:
        The PDF path, or None when it is not there.
    """
    name = _MANUALS.get(language or _language(), _MANUALS["en"])
    # se sube desde este archivo: el PDF vive en la raíz del repo / de la instalación
    for folder in Path(__file__).resolve().parents:
        for candidate in (folder / name, folder / "docs" / name):
            if candidate.is_file():
                return candidate
    return None


def openManual() -> None:
    """Open the user manual in the system PDF viewer.

    Spanish opens ``Manual_Usuario.pdf``, English ``User_Manual.pdf`` and
    Portuguese ``Manual_do_Usuario.pdf``.
    """
    language = _language()
    path = manualPath(language)
    if path is None:
        print(f"[DAV] Error: no se encontró el manual ({_MANUALS.get(language, _MANUALS['en'])}).")
        return
    if sys.platform.startswith("win"):
        os.startfile(str(path))  # noqa: S606 - abre el PDF con el visor del sistema
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])
