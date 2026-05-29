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

_KEYCHAIN_ROOT = Path(__file__).resolve().parents[4]
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
        module = importlib.import_module("base")
        base = getattr(module, "Base", None)
        if not isinstance(base, dict):
            raise ValueError("base.py must define dict Base = {...}")
        return dict(base)

    def LoadTranslateMap(self, folder: Path, language: LanguageCode) -> dict[str, Any]:
        if not self.IsReady:
            return {}
        for stem in language.AlternateTranslateSuffixes:
            path = folder / f"{stem}.py"
            if not path.is_file():
                continue
            module = self._ImportTranslateModule(path, stem)
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

    def ResolveSubFolder(self, parent_folder: Path, internal_key: str) -> Path:
        if parent_folder == self.DictionaryRoot:
            nested = self.DictionaryRoot / "explorer" / internal_key
            if nested.is_dir():
                return nested
            explorer_pkg = self.DictionaryRoot / "explorer"
            if explorer_pkg.is_dir():
                return explorer_pkg
        child = parent_folder / internal_key
        if child.is_dir():
            return child
        return parent_folder

    @staticmethod
    def NormalizeSpoken(text: str) -> str:
        decomposed = unicodedata.normalize("NFKD", text)
        stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
        return " ".join(stripped.lower().split())

    def _ImportTranslateModule(self, path: Path, stem: str) -> ModuleType:
        rel = path.relative_to(self.DictionaryRoot).with_suffix("")
        module_name = ".".join(rel.parts)
        return importlib.import_module(module_name)
