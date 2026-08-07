#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Load base.py and TraduceTo* modules using Keychain + package import."""

from __future__ import annotations

import importlib
import sys
import unicodedata
from pathlib import Path
from types import ModuleType
from typing import Any

from core.language_code import LanguageCode

_KEYCHAIN_ROOT = Path(__file__).resolve().parents[3]
if str(_KEYCHAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_KEYCHAIN_ROOT))

from Keychain.Keychain import Keychain  # noqa: E402


class DictionaryLoader:
    """
    Reads dictionary folders (base.py + TraduceTo* files).

    If the dictionary root does not exist yet, IsReady is False and all
    load methods return empty collections instead of raising.
    This allows Browser to start without a configured dictionary and wait
    for Developer 3 / the team to wire the real dictionary folder.
    """

    def __init__(self, dictionary_root: Path | str) -> None:
        self.DictionaryRoot = Path(dictionary_root).resolve()
        self.IsReady: bool = self.DictionaryRoot.is_dir()
        if not self.IsReady:
            print(
                f"[DAV-Browser] Dictionary root not found: {self.DictionaryRoot}\n"
                "  Configure a real dictionary path to enable voice navigation."
            )
            return
        root_text = str(self.DictionaryRoot)
        if root_text not in sys.path:
            sys.path.insert(0, root_text)

    def LoadBaseModuleDict(self) -> dict[str, Any]:
        if not self.IsReady:
            return {}
        try:
            module = importlib.import_module("base")
        except Exception as error:  # noqa: BLE001 - aislar base.py roto
            print(
                f"[DAV-Browser] No se pudo cargar 'base.py' en {self.DictionaryRoot}: "
                f"{error.__class__.__name__}: {error}. El motor arranca con "
                "BaseContext vacío."
            )
            return {}
        base = getattr(module, "Base", None)
        if not isinstance(base, dict):
            raise ValueError("base.py must define dict Base = {...}")
        return dict(base)

    def LoadModuleDictByName(self, module_name: str, attr_name: str) -> dict[str, Any]:
        """Import a module by dotted name (relative to DictionaryRoot) and
        return the dict attribute ``attr_name`` from it, or {} if unavailable.

        Used for fixed infrastructure modules (e.g. NavCommands.NavActions)
        that are not per-folder TraduceTo*/base.py files but still need to
        be resolved through the same sys.path as the rest of the dictionary
        tree, so they are not accidentally hardcoded elsewhere.
        """
        if not self.IsReady:
            return {}
        try:
            module = importlib.import_module(module_name)
        except Exception as error:  # noqa: BLE001 - aislar módulo roto
            print(
                f"[DAV-Browser] No se pudo cargar '{module_name}': "
                f"{error.__class__.__name__}: {error}."
            )
            return {}
        table = getattr(module, attr_name, None)
        return dict(table) if isinstance(table, dict) else {}

    def LoadTranslateMap(self, folder: Path, language: LanguageCode) -> dict[str, Any]:
        if not self.IsReady:
            return {}
        for stem in language.AlternateTranslateSuffixes:
            path = folder / f"{stem}.py"
            if not path.is_file():
                continue
            # Si un diccionario está roto (import relativo inválido, sintaxis,
            # etc.) no se debe tumbar todo el motor: se omite y se sigue con
            # el resto. Browser tolera un mapa vacío sin fallar.
            try:
                module = self._ImportTranslateModule(path, stem)
            except Exception as error:  # noqa: BLE001 - aislar diccionario roto
                print(
                    f"[DAV-Browser] No se pudo cargar el diccionario '{path}': "
                    f"{error.__class__.__name__}: {error}. Se omite y se "
                    "continúa con los diccionarios disponibles."
                )
                continue
            table = getattr(module, stem, None)
            if isinstance(table, dict):
                return dict(table)
        return {}

    def LoadTranslateSpokenKeys(self, folder: Path, language: LanguageCode) -> list[str]:
        if not self.IsReady:
            return []
        for stem in language.AlternateTranslateSuffixes:
            path = folder / f"{stem}.py"
            if not path.is_file():
                continue
            try:
                return Keychain(str(path)).GetAllKeys()
            except ValueError:
                continue
        return []

    def LoadModuleDictForKey(self, parent_folder: Path, internal_key: str) -> dict[str, Any]:
        if not self.IsReady:
            return {}
        child = parent_folder / internal_key
        if not child.is_dir():
            raise FileNotFoundError(f"No subfolder for key '{internal_key}' in {parent_folder}")

        if parent_folder == self.DictionaryRoot:
            module_name = f"explorer.{internal_key}"
            if internal_key == "print":
                mod = importlib.import_module("explorer.print.print_cmds")
                table = getattr(mod, "print_cmds", None)
            else:
                mod = importlib.import_module(f"{module_name}.{internal_key}")
                table = getattr(mod, internal_key, None)
            if isinstance(table, dict):
                return dict(table)
            raise ValueError(f"No command dict for {internal_key}")

        rel = child.relative_to(self.DictionaryRoot)
        parts = list(rel.parts)
        if internal_key == "print":
            mod = importlib.import_module(".".join(parts + ["print_cmds"]))
            table = getattr(mod, "print_cmds", None)
        else:
            mod = importlib.import_module(".".join(parts + [internal_key]))
            table = getattr(mod, internal_key, None)
        if isinstance(table, dict):
            return dict(table)
        raise ValueError(f"No command dict in {child}")

    def ResolveSubFolder(
        self, parent_folder: Path, internal_key: str, target: Any = None
    ) -> Path:
        # _InferInternalKey solo devuelve una clave confiable (explorer,
        # preferences, sketcher...) cuando el destino está anidado como valor
        # en el dict del nivel actual; si no, cae al spoken en español
        # ("vista estándar"), que no es nombre de carpeta ni de módulo.
        # Por eso primero resolvemos por identidad de objeto: cada carpeta
        # hermana expone su dict maestro con el mismo nombre (StdView/
        # StdView.py → StdView, Sketcher/sketcher.py → sketcher), así que
        # comparamos `is target`. Esto aplica en cualquier profundidad del
        # árbol, no solo al descender desde la raíz.
        if target is not None:
            by_identity = self._FindChildByTargetIdentity(parent_folder, target)
            if by_identity is not None:
                return by_identity
        # Carpeta hermana directa por nombre (case-insensitive), útil cuando
        # internal_key sí es confiable (p. ej. "explorer", "sketcher").
        direct = self._FindChildCaseInsensitive(parent_folder, internal_key)
        if direct is not None:
            return direct
        if parent_folder == self.DictionaryRoot:
            # Caso especial: los submenús propios de Explorer (file, edit,
            # windows...) viven anidados dentro de la carpeta Explorer/.
            nested = self.DictionaryRoot / "explorer" / internal_key
            if nested.is_dir():
                return nested
            explorer_pkg = self.DictionaryRoot / "explorer"
            if explorer_pkg.is_dir():
                return explorer_pkg
        child = parent_folder / internal_key
        if child.is_dir():
            return child
        raise FileNotFoundError(
            f"No se pudo resolver una subcarpeta para '{internal_key}' "
            f"dentro de {parent_folder}. Se esperaba una carpeta hermana "
            "identificable por nombre o por identidad del dict de destino."
        )

    _SKIP_MODULE_STEMS = frozenset({"ayuda", "help", "__init__"})

    def _FindChildByTargetIdentity(self, parent_folder: Path, target: Any) -> Path | None:
        rel_parent = parent_folder.relative_to(self.DictionaryRoot)
        parent_parts = [] if rel_parent == Path(".") else list(rel_parent.parts)
        for child in parent_folder.iterdir():
            if not child.is_dir() or child.name.startswith(("_", ".")):
                continue
            for module_file in child.glob("*.py"):
                stem = module_file.stem
                if stem in self._SKIP_MODULE_STEMS or stem.startswith("TraduceTo"):
                    continue
                module_name = ".".join(parent_parts + [child.name, stem])
                try:
                    module = importlib.import_module(module_name)
                except Exception:  # noqa: BLE001 - módulo candidato inválido, seguir buscando
                    continue
                if any(value is target for value in vars(module).values()):
                    return child
        return None

    @staticmethod
    def _FindChildCaseInsensitive(parent_folder: Path, internal_key: str) -> Path | None:
        target = internal_key.lower()
        for child in parent_folder.iterdir():
            if child.is_dir() and child.name.lower() == target:
                return child
        return None

    @staticmethod
    def NormalizeSpoken(text: str) -> str:
        decomposed = unicodedata.normalize("NFKD", text)
        stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
        return " ".join(stripped.lower().split())

    def _ImportTranslateModule(self, path: Path, stem: str) -> ModuleType:
        # resolve() returns the actual filesystem casing on Windows, so the
        # computed module name matches what is already cached in sys.modules.
        resolved_path = path.resolve()
        resolved_root = self.DictionaryRoot.resolve()
        rel = resolved_path.relative_to(resolved_root).with_suffix("")
        module_name = ".".join(rel.parts)
        return importlib.import_module(module_name)
