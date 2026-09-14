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

from typing import Optional, Tuple, Any

from PruebaIntegracion.core.ContextNode import ContextNode
from PruebaIntegracion.core.FunctionWrapper import FunctionWrapper


class Navigator:
    """Manages the current context and function lookup in the hierarchy."""

    def __init__(self, root: ContextNode):
        if not isinstance(root, ContextNode):
            raise TypeError("The root must be a ContextNode")
        self.root = root
        self.current_context: ContextNode = root

    def set_context(self, node: ContextNode) -> None:
        """Sets `current_context` to `node` (must belong to the tree)."""
        self.current_context = node

    def navigate(self, path: str) -> Optional[ContextNode]:
        """Navigates through a hyphen-separated path (e.g., 'Drawing-Geometry').
        Returns the final node if valid, otherwise None.
        """
        parts = [p.strip() for p in path.split("-") if p.strip()]
        node = self.current_context
        for part in parts:
            child = node.get_child(part)
            if child is None:
                return None
            node = child
        self.current_context = node
        return node

    def find_function_ascending(self, real_name: str) -> Optional[Tuple[ContextNode, FunctionWrapper]]:
        """Searches for `real_name` starting from `current_context` and moving up to the root.
        Returns a tuple (found_node, wrapper) or None if it doesn't exist.
        """
        node = self.current_context
        while node is not None:
            val = node.elements.get(real_name)
            if isinstance(val, FunctionWrapper):
                return node, val
            node = node.parent
        return None

    def call(self, real_name: str, *args: Any, context_keys: Optional[list[str]] = None, **kwargs: Any) -> Any:
        """Finds and executes the function `real_name`. Updates the context to the node where it was found."""
        found = self.find_function_ascending(real_name)
        if not found:
            raise LookupError(f"Function '{real_name}' not found from the current context.")
        node, wrapper = found
        # Update context to the node where the function was found
        self.current_context = node
        return wrapper.execute(*args, context_keys=context_keys, **kwargs)

    def get_current_context(self) -> ContextNode:
        return self.current_context

    def __repr__(self) -> str:
        return f"Navigator(current_context={self.current_context.name!r})"