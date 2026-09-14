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

import importlib
import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Iterable

from PruebaIntegracion.core.FunctionWrapper import FunctionWrapper
from PruebaIntegracion.core.ContextNode import ContextNode


class LoaderWithTranslations:
    """Loads the `dic/` hierarchy from Python modules and translations.

    Conventions:
    - Each folder represents a `ContextNode`.
    - Semantic modules can expose a root dictionary with the same
      name as the file to model a command dictionary.
    - `TranslateTo*.py` files can expose `TRANSLATIONS` as a dict.
    - Other `.py` files are inspected and only callables with `_param_specs` are loaded.
    """

    def __init__(self, dic_directory: str | Path | None = None) -> None:
        self._package_root = Path(__file__).resolve().parent.parent
        if dic_directory is not None:
            self.source_directories = (Path(dic_directory),)
        else:
            directories: list[Path] = []
            dictionary = self._package_root / "dictionary"
            if dictionary.exists():
                directories.append(dictionary)
            directories.append(self._package_root / "dic")
            self.source_directories = tuple(directories)
        self.dic_directory = self.source_directories[0] if self.source_directories else self._package_root / "dic"

    def load(self) -> Dict[str, ContextNode]:
        roots: Dict[str, ContextNode] = {}
        for source in self.source_directories:
            if not source.exists():
                continue
            for child in sorted(source.iterdir(), key=lambda p: p.name.lower()):
                if child.is_dir() and not child.name.startswith("_"):
                    roots[child.name] = self._load_directory(child, parent=None)
                elif child.suffix.lower() == ".py" and child.name != "__init__.py" and not child.name.startswith("_"):
                    node = self._load_root_module(child)
                    if node is not None:
                        roots[node.name] = node
        return roots

    def _load_directory(self, directory: Path, parent: ContextNode | None) -> ContextNode:
        node = ContextNode(directory.name, parent=parent)

        for file in sorted(directory.iterdir(), key=lambda p: p.name.lower()):
            if file.is_dir() and not file.name.startswith("_"):
                subnode = self._load_directory(file, parent=node)
                node.add_subcontext(file.name, subnode)
                continue

            if file.suffix.lower() != ".py" or file.name == "__init__.py":
                continue

            if self._load_semantic_structure(file, node):
                continue

            if file.name.lower().startswith("translateto"):
                self._load_translations(file, node)
            else:
                self._load_functions(file, node)

        return node

    def _load_root_module(self, file: Path) -> ContextNode | None:
        module = self._import_module(file)
        if module is None:
            return None

        structure = self._extract_semantic_structure(module, file.stem)
        if structure is None:
            return None

        node = ContextNode(file.stem)
        self._load_from_dictionary(node, structure)
        return node

    def _load_semantic_structure(self, file: Path, node: ContextNode) -> bool:
        module = self._import_module(file)
        if module is None:
            return False

        structure = self._extract_semantic_structure(module, file.stem)
        if structure is None:
            return False

        self._load_from_dictionary(node, structure)
        return True

    def _extract_semantic_structure(self, module: ModuleType, expected_name: str) -> dict[str, Any] | None:
        candidate = getattr(module, expected_name, None)
        if isinstance(candidate, dict):
            return candidate

        for name, obj in vars(module).items():
            if name.startswith("_"):
                continue
            if isinstance(obj, dict):
                return obj

        return None

    def _load_from_dictionary(self, node: ContextNode, structure: dict[str, Any]) -> None:
        for key, value in structure.items():
            if isinstance(value, dict):
                subnode = ContextNode(key, parent=node)
                self._load_from_dictionary(subnode, value)
                node.add_subcontext(key, subnode)
                node.add_translation(key.strip().lower(), key)
                continue

            if isinstance(value, FunctionWrapper):
                node.add_function(key, value)
                node.add_translation(key.strip().lower(), key)
                continue

            if callable(value):
                node.add_function(key, FunctionWrapper(value))
                node.add_translation(key.strip().lower(), key)
                continue

            if isinstance(value, str):
                node.add_translation(key.strip().lower(), value.strip())

    def _load_translations(self, file: Path, node: ContextNode) -> None:
        module = self._import_module(file)
        if module is None:
            return

        translations = getattr(module, "TRANSLATIONS", None)
        if isinstance(translations, dict):
            for spoken_word, real_name in translations.items():
                if isinstance(spoken_word, str) and isinstance(real_name, str):
                    node.add_translation(spoken_word.strip().lower(), real_name.strip())

    def _load_functions(self, file: Path, node: ContextNode) -> None:
        module = self._import_module(file)
        if module is None:
            return

        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            if callable(obj) and hasattr(obj, "_param_specs"):
                wrapper = FunctionWrapper(obj)
                node.add_function(name, wrapper)

    def _import_module(self, file: Path) -> ModuleType | None:
        resolved_path = file.resolve()
        try:
            relative_package = resolved_path.relative_to(self._package_root.resolve())
        except ValueError:
            relative_package = None

        if relative_package is not None:
            module_name = ".".join((self._package_root.name, *relative_package.with_suffix("").parts))
            try:
                return importlib.import_module(module_name)
            except Exception:
                pass

        unique_name = f"PruebaIntegracion.dic_{file.stem}_{abs(hash(str(resolved_path)))}"
        spec = importlib.util.spec_from_file_location(unique_name, resolved_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not import file {file}")

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            return None
        return module

