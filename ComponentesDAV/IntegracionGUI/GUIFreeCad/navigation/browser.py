#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""
Browser: voice navigation engine over dictionary folders.

Implemented so far (Developer 1 + Developer 2):
  - Preferences.SetLanguage → En / Es / PT
  - BaseContext: fixed top-level commands loaded from base.py via Keychain
  - Context:     current-level spoken commands (TraduceTo*)
  - Language-change callback: reloads from base.py automatically
  - ProcessPhrase: direct BaseContext jump (Requirement 2)

TODO Developer 3 – Search engine (descend + ascend):
  - Implement _DescendToSubContext: enter a sub-folder context manually
  - Implement _SearchUpwardAndExecute: if command not in current Context,
    save OriginalContext, walk the stack upward, execute if found,
    restore to OriginalContext if not found anywhere
  - Wire both into ProcessPhrase below (marked TODO)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from core.language_code import LanguageCode
from core.preferences import Preferences, preferences
from navigation.context_entry import ContextEntry, FindBySpoken
from navigation.dictionary_loader import DictionaryLoader


@dataclass
class _ContextFrame:
    """One level in the navigation stack (needed by Developer 3)."""

    Folder: Path
    ModuleDict: dict[str, Any]
    InternalName: str


@dataclass
class BrowserResult:
    """Outcome of ProcessPhrase."""

    Success: bool
    Action: str
    Message: str = ""


class Browser:
    """
    Voice navigation engine for the DAV dictionary structure.

    Public lists (task naming):
      - BaseContext: top-level Base commands (unchanged after init)
      - Context:     current navigable spoken commands
      - OriginalContext: snapshot during upward search (Developer 3)

    Constructor accepts an optional ``_loader`` for unit-testing without a
    real dictionary on disk (inject a mock DictionaryLoader).
    """

    def __init__(
        self,
        dictionary_root: Path | str | None = None,
        *,
        prefs: Preferences | None = None,
        on_execute: Callable[[ContextEntry], None] | None = None,
        _loader: DictionaryLoader | None = None,
    ) -> None:
        self._prefs = prefs or preferences
        self._on_execute = on_execute
        self._loader = _loader or DictionaryLoader(
            dictionary_root or self._DefaultDictionaryRoot()
        )
        self._language = self._prefs.SetLanguage
        self._stack: list[_ContextFrame] = []
        self._base_translate: dict[str, Any] = {}
        self._base_module: dict[str, Any] = {}

        self.BaseContext: list[ContextEntry] = []
        self.Context: list[ContextEntry] = []
        self.OriginalContext: list[ContextEntry] | None = None

        self._prefs.RegisterLanguageChange(self._OnLanguageChanged)
        self.ResetFromBase()

    @staticmethod
    def _DefaultDictionaryRoot() -> Path:
        """
        Default path: DAV/ejemplo de diccionario terminado (repo root).
        If that folder does not exist DictionaryLoader.IsReady will be False
        and Browser starts with empty contexts — no crash.
        """
        here = Path(__file__).resolve()
        for parent in (here.parents[3], here.parents[4], here.parents[2]):
            candidate = parent / "ejemplo de diccionario terminado"
            if candidate.is_dir():
                return candidate
        return here.parents[3] / "ejemplo de diccionario terminado"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def SetLanguage(self) -> LanguageCode:
        return self._language

    @SetLanguage.setter
    def SetLanguage(self, value: LanguageCode) -> None:
        self._prefs.SetLanguage = value

    def ResetFromBase(self) -> None:
        """Reload BaseContext and Context from base.py (current language)."""
        self._language = self._prefs.SetLanguage
        self._base_module = self._loader.LoadBaseModuleDict()
        self._base_translate = self._loader.LoadTranslateMap(
            self._loader.DictionaryRoot, self._language
        )
        self._stack = [
            _ContextFrame(
                Folder=self._loader.DictionaryRoot,
                ModuleDict=self._base_module,
                InternalName="Base",
            )
        ]
        self.BaseContext = self._BuildBaseContextEntries()
        self.Context = self._BuildContextForFrame(self._stack[-1])
        self.OriginalContext = None

    def ProcessPhrase(self, spoken: str) -> BrowserResult:
        """
        Handle one voice token.

        Developer 2 (implemented):
          - If spoken matches a BaseContext command → jump directly (Req. 2)

        TODO Developer 3:
          - If spoken matches current Context and target is a sub-context → descend
          - If spoken matches current Context and target is callable → execute
          - If not found in Context → save OriginalContext, search upward,
            execute if found, restore if not found (Req. 1)
        """
        normalized = DictionaryLoader.NormalizeSpoken(spoken)
        if not normalized:
            return BrowserResult(False, "empty", "Empty phrase")

        # Requirement 2 (Developer 2): direct jump for BaseContext commands
        base_hit = self._ResolveBaseJump(normalized)
        if base_hit is not None:
            self._ApplyBaseJump(base_hit)
            return BrowserResult(
                True,
                "base_jump",
                f"Context set to {base_hit.InternalKey}",
            )

        entry = FindBySpoken(self.Context, normalized)
        if entry is not None:
            if entry.IsSubContext():
                self._DescendToSubContext(entry)
                return BrowserResult(True, "descend", f"Context set to {entry.InternalKey}")
            if entry.IsCallable():
                self._ExecuteEntry(entry)
                return BrowserResult(True, "execute", f"Executed {entry.InternalKey}")

        return self._SearchUpwardAndExecute(normalized)

    # ------------------------------------------------------------------
    # Internal helpers (Developer 2)
    # ------------------------------------------------------------------

    def _OnLanguageChanged(self, _previous: LanguageCode, _new: LanguageCode) -> None:
        self.ResetFromBase()

    def _BuildBaseContextEntries(self) -> list[ContextEntry]:
        entries: list[ContextEntry] = []
        for internal_key, target in self._base_module.items():
            entries.append(
                ContextEntry(
                    Spoken=internal_key,
                    InternalKey=internal_key,
                    Target=target,
                )
            )
        return entries

    def _BuildContextForFrame(self, frame: _ContextFrame) -> list[ContextEntry]:
        entries: list[ContextEntry] = []
        seen_spoken: set[str] = set()

        translate = self._loader.LoadTranslateMap(frame.Folder, self._language)
        for spoken, target in translate.items():
            key = self._InferInternalKey(spoken, target, frame.ModuleDict)
            entries.append(ContextEntry(Spoken=spoken, InternalKey=key, Target=target))
            seen_spoken.add(DictionaryLoader.NormalizeSpoken(spoken))

        for internal_key, target in frame.ModuleDict.items():
            norm = DictionaryLoader.NormalizeSpoken(internal_key)
            if norm in seen_spoken:
                continue
            entries.append(
                ContextEntry(
                    Spoken=internal_key,
                    InternalKey=internal_key,
                    Target=target,
                )
            )
        return entries

    def _InferInternalKey(
        self, spoken: str, target: Any, module_dict: dict[str, Any]
    ) -> str:
        for key, value in module_dict.items():
            if value is target:
                return key
        return spoken

    def _ResolveBaseJump(self, normalized_spoken: str) -> ContextEntry | None:
        """Return a BaseContext entry if the spoken word maps to a base command."""
        for spoken, target in self._base_translate.items():
            if DictionaryLoader.NormalizeSpoken(spoken) != normalized_spoken:
                continue
            if isinstance(target, dict):
                for key, value in self._base_module.items():
                    if value is target:
                        return ContextEntry(
                            Spoken=spoken,
                            InternalKey=key,
                            Target=target,
                        )
        for entry in self.BaseContext:
            norm = DictionaryLoader.NormalizeSpoken(entry.Spoken)
            if norm == normalized_spoken and entry.IsSubContext():
                return entry
            if DictionaryLoader.NormalizeSpoken(entry.InternalKey) == normalized_spoken:
                if entry.IsSubContext():
                    return entry
        return None

    def _ApplyBaseJump(self, entry: ContextEntry) -> None:
        """Jump directly to a BaseContext entry."""
        if entry.IsSubContext():
            self._stack = [self._stack[0]]
            self._DescendToSubContext(entry)
        elif entry.IsCallable():
            self._ExecuteEntry(entry)

    def _DescendToSubContext(self, entry: ContextEntry) -> None:
        """Descend manually into a sub-folder context."""
        frame = _ContextFrame(
            Folder=self._loader.ResolveSubFolder(self._stack[-1].Folder, entry.InternalKey),
            ModuleDict=entry.Target,
            InternalName=entry.InternalKey,
        )
        self._stack.append(frame)
        self.Context = self._BuildContextForFrame(frame)

    def _SearchUpwardAndExecute(self, normalized_spoken: str) -> BrowserResult:
        """Automatic ascending search."""
        self.OriginalContext = self._SnapshotContext(self.Context)
        temp_stack = list(self._stack)
        
        while len(temp_stack) > 1:
            temp_stack.pop()
            parent_frame = temp_stack[-1]
            parent_context = self._BuildContextForFrame(parent_frame)
            
            entry = FindBySpoken(parent_context, normalized_spoken)
            if entry is not None:
                if entry.IsCallable():
                    self._ExecuteEntry(entry)
                    self._stack = temp_stack
                    self.Context = parent_context
                    self.OriginalContext = parent_context
                    return BrowserResult(True, "execute", f"Ascending: executed {entry.InternalKey}")
                elif entry.IsSubContext():
                    self._stack = temp_stack
                    self.Context = parent_context
                    self._DescendToSubContext(entry)
                    self.OriginalContext = self.Context
                    return BrowserResult(True, "descend", f"Ascending: descended into {entry.InternalKey}")
        
        self.Context = self.OriginalContext
        return BrowserResult(False, "not_found", "Command not found in upward search")

    def _ExecuteEntry(self, entry: ContextEntry) -> None:
        """Execute a leaf command entry."""
        if self._on_execute is not None:
            self._on_execute(entry)
        elif entry.IsCallable():
            entry.Target()

    @staticmethod
    def _SnapshotContext(entries: list[ContextEntry]) -> list[ContextEntry]:
        return list(entries)
