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

"""Resolve dictionary keys to SVG icon paths."""

from __future__ import annotations

import os
from pathlib import Path


class IconLocator:
    """Finds the SVG of a dictionary key, indexing each source once.

    The previous implementation walked the whole dictionary tree **per button
    and per re-render**, with no cache. Here the index is built lazily on the
    first lookup and reused, over the two places icons actually live:

    ``InterfazDAV/Icons`` (own icons, win ties) · ``Dav/dic`` (494 files)

    Args:
        SearchRoots: directories to index, highest priority first. When
            omitted they are resolved from this file's location.

    Example::

        locator = IconLocator()
        path = locator.Find("extrude")   # "" when there is no icon
    """

    def __init__(self, SearchRoots: list[Path] | None = None) -> None:
        self._roots = SearchRoots if SearchRoots is not None else self._DefaultRoots()
        self._index: dict[str, str] | None = None

    @staticmethod
    def _DefaultRoots() -> list[Path]:
        """Icon directories, resolved relative to this file."""
        here = Path(__file__).resolve().parent

        roots = [here / "Icons"]

        # Dav/dic: subir ancestros hasta encontrarlo (layout DavCore). Se
        # valida el contenido porque ComponentesDAV/Dav/dic es un placeholder
        # vacio que aparece antes en la cadena y no tiene iconos — la misma
        # trampa que resuelve _is_dictionary_dir() en dav_commands.py.
        for ancestor in here.parents:
            candidate = ancestor / "Dav" / "dic"
            if candidate.is_dir() and (candidate / "base.py").is_file():
                roots.append(candidate)
                break

        return [r for r in roots if r.is_dir()]

    def _BuildIndex(self) -> dict[str, str]:
        """Map ``nombre-sin-extension`` → ruta, recorriendo cada raiz una vez.

        La primera raiz que define un nombre gana, para que un icono propio
        de InterfazDAV pueda pisar al del arbol de diccionarios.
        """
        index: dict[str, str] = {}
        for root in self._roots:
            for dirpath, _dirnames, filenames in os.walk(root):
                for filename in filenames:
                    if not filename.lower().endswith(".svg"):
                        continue
                    index.setdefault(filename[:-4], os.path.join(dirpath, filename))
        return index

    def Find(self, Key: str) -> str:
        """Path to the icon for that key.

        Args:
            Key: internal dictionary key, e.g. ``"extrude"``.

        Returns:
            Absolute path to the SVG, or ``""`` when there is none. The caller
            decides the fallback; this never raises.
        """
        if not Key:
            return ""
        if self._index is None:
            self._index = self._BuildIndex()
        return self._index.get(Key, "")

    def Invalidate(self) -> None:
        """Drop the cached index so the next lookup re-scans the roots."""
        self._index = None
