#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.
from __future__ import annotations

from typing import Any, Dict, Optional, Iterable

from PruebaIntegracion.core.FunctionWrapper import FunctionWrapper


class ContextNode:
    """Node in the tools hierarchy.

    - `elements` maps real names -> FunctionWrapper or ContextNode
    - `translations` maps spoken_word -> real_name
    - `parent` reference to the parent node (or None if root)
    """

    def __init__(self, name: str, parent: Optional[ContextNode] = None):
        self.name = name
        self.parent = parent
        self.elements: Dict[str, Any] = {}
        self.translations: Dict[str, str] = {}

    def add_function(self, key: str, wrapper: FunctionWrapper) -> None:
        """Adds a wrapped function to the node under the given key."""
        self.elements[key] = wrapper

    def add_subcontext(self, key: str, node: "ContextNode") -> None:
        """Adds a subcontext (another ContextNode)."""
        node.parent = self
        self.elements[key] = node

    def add_translation(self, spoken_word: str, real_name: str) -> None:
        """Adds a local translation from spoken word to real name."""
        self.translations[spoken_word] = real_name

    def get_real_name(self, spoken_word: str) -> Optional[str]:
        """Looks up the translation in this node; returns None if not found."""
        return self.translations.get(spoken_word)

    def get_all_keys(self) -> Iterable[str]:
        """Returns all real keys available in this node (not translations)."""
        yield from self.elements.keys()

    def get_child(self, key: str) -> Optional["ContextNode"]:
        """If `key` corresponds to a subcontext, returns the ContextNode, otherwise None."""
        val = self.elements.get(key)
        if isinstance(val, ContextNode):
            return val
        return None

    def __repr__(self) -> str:
        return f"ContextNode({self.name!r}, elements={list(self.elements.keys())})"

