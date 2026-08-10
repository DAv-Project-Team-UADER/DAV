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

Search engine (descend + ascend):
  - _DescendToSubContext: enter a sub-folder context manually
  - _SearchUpwardAndExecute: if command not in current Context,
    save OriginalContext, walk the stack upward, execute if found,
    restore to OriginalContext if not found anywhere

Multi-word phrases that name a sub-context and a command inside it in one
shot ("nuevo archivo" without first saying "archivo") are NOT resolved
automatically: the user must descend explicitly, then say the leaf command.

Navigation words (subir/volver/contexto/...) are NOT hardcoded here: they
live in Dav/dic/NavCommands/TraduceTo*.py like any other spoken dictionary,
and are matched by identity against NavActions.GoUp / NavActions.ShowContext.
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
        on_descend: Callable[[ContextEntry], None] | None = None,
        _loader: DictionaryLoader | None = None,
    ) -> None:
        self._prefs = prefs or preferences
        self._on_execute = on_execute
        self._on_descend = on_descend
        self._loader = _loader or DictionaryLoader(
            dictionary_root or self._DefaultDictionaryRoot()
        )
        self._language = self._prefs.SetLanguage
        self._stack: list[_ContextFrame] = []
        self._base_translate: dict[str, Any] = {}
        self._base_module: dict[str, Any] = {}
        self._nav_translate: dict[str, Any] = {}

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

    @property
    def CurrentContextName(self) -> str:
        """Internal name of the context the user is currently in."""
        return self._stack[-1].InternalName if self._stack else "Base"

    @property
    def ContextPath(self) -> str:
        """Breadcrumb of the navigation stack, e.g. ``Base > explorer > file``."""
        return " > ".join(frame.InternalName for frame in self._stack)

    def DescribeContext(self) -> str:
        """Human-readable summary of where you are and what you can say.

        Lists the spoken words available in the current context, marking
        sub-menus (descend) apart from directly executable commands. Used by
        the voice adapter to print the context as the user moves around.
        """
        submenus: list[str] = []
        commands: list[str] = []
        seen_targets: list[Any] = []
        for entry in self.Context:
            # Un mismo destino suele tener varios alias (la palabra hablada
            # "nuevo" y la clave interna "new"). _BuildContextForFrame agrega
            # primero las habladas del TraduceTo, así que nos quedamos con la
            # primera vista por destino (la español) y omitimos el resto.
            if any(self._SameTarget(entry.Target, t) for t in seen_targets):
                continue
            seen_targets.append(entry.Target)
            if entry.IsSubContext():
                submenus.append(entry.Spoken)
            elif entry.IsCallable():
                commands.append(entry.Spoken)

        lines = [f"[DAV] Contexto: {self.ContextPath}"]
        if submenus:
            lines.append("  Submenús (entrar): " + ", ".join(sorted(submenus)))
        if commands:
            lines.append("  Comandos (ejecutar): " + ", ".join(sorted(commands)))
        if self._IsDescended():
            up_word = self._FirstSpokenForNavAction("up")
            if up_word:
                lines.append(f"  Decí «{up_word}» para subir un nivel.")
        if not submenus and not commands:
            lines.append("  (sin comandos en este contexto)")
        return "\n".join(lines)

    def ResetFromBase(self) -> None:
        """Reload BaseContext and Context from base.py (current language)."""
        self._language = self._prefs.SetLanguage
        self._base_module = self._loader.LoadBaseModuleDict()
        self._base_translate = self._loader.LoadTranslateMap(
            self._loader.DictionaryRoot, self._language
        )
        self._nav_translate = self._loader.LoadTranslateMap(
            self._loader.DictionaryRoot / "NavCommands", self._language
        )
        self._nav_actions = self._loader.LoadModuleDictByName("NavCommands.NavActions", "NavActions")
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

        # Comandos de navegación (subir, mostrar contexto, ...): se resuelven
        # contra Dav/dic/NavCommands/TraduceTo*.py, no contra un set fijo en
        # código. Funcionan en cualquier contexto, sin depender de en qué
        # nivel del árbol de comandos FreeCAD esté parado el usuario.
        nav_action = self._ResolveNavAction(normalized)
        if nav_action is not None:
            return self._ExecuteNavAction(nav_action)

        # El contexto actual tiene prioridad sobre el salto base: si ya
        # descendimos a un subcontexto, una palabra que también existe en el
        # Base (p. ej. "archivo" sirve para entrar a explorer y, dentro de
        # explorer, para bajar a "file") debe resolverse contra el nivel
        # actual primero. Así "archivo → archivo → nuevo" baja por niveles en
        # vez de quedar saltando siempre al mismo contexto base.
        if self._IsDescended():
            entry = FindBySpoken(self.Context, normalized)
            if entry is not None:
                if entry.IsSubContext():
                    if self._DescendToSubContext(entry):
                        return BrowserResult(True, "descend", f"Context set to {entry.InternalKey}")
                    return BrowserResult(False, "descend_failed", f"No se pudo entrar a {entry.InternalKey}")
                if entry.IsCallable():
                    self._ExecuteEntry(entry)
                    return BrowserResult(True, "execute", f"Executed {entry.InternalKey}")

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
                if self._DescendToSubContext(entry):
                    return BrowserResult(True, "descend", f"Context set to {entry.InternalKey}")
                return BrowserResult(False, "descend_failed", f"No se pudo entrar a {entry.InternalKey}")
            if entry.IsCallable():
                self._ExecuteEntry(entry)
                return BrowserResult(True, "execute", f"Executed {entry.InternalKey}")

        return self._SearchUpwardAndExecute(normalized)

    def _IsDescended(self) -> bool:
        """True si estamos dentro de un subcontexto (no en el nivel base)."""
        return len(self._stack) > 1

    def _AscendOneLevel(self) -> str:
        """Sube un nivel: descarta el frame actual y reconstruye el padre.

        Returns:
            El nombre interno del contexto al que se volvió.
        """
        self._stack.pop()
        parent = self._stack[-1]
        self.Context = self._BuildContextForFrame(parent)
        self.OriginalContext = None
        return parent.InternalName

    # ------------------------------------------------------------------
    # Navigation words (NavCommands) — not hardcoded, read from
    # Dav/dic/NavCommands/TraduceTo*.py and matched by identity against
    # NavActions.GoUp / NavActions.ShowContext.
    # ------------------------------------------------------------------

    def _ResolveNavAction(self, normalized_spoken: str) -> str | None:
        """Return the NavActions key ('up', 'show_context', ...) for a
        spoken phrase, or None if it does not name a navigation command."""
        for spoken, target in self._nav_translate.items():
            if DictionaryLoader.NormalizeSpoken(spoken) != normalized_spoken:
                continue
            for key, value in self._nav_actions.items():
                if value is target:
                    return key
        return None

    def _ExecuteNavAction(self, action_key: str) -> BrowserResult:
        if action_key == "up":
            if self._IsDescended():
                parent = self._AscendOneLevel()
                return BrowserResult(True, "back", f"Context set to {parent}")
            return BrowserResult(False, "back", "Already at root context")
        if action_key == "show_context":
            return BrowserResult(True, "show_context", self.DescribeContext())
        return BrowserResult(False, "nav_unknown", f"Unknown nav action '{action_key}'")

    def _FirstSpokenForNavAction(self, action_key: str) -> str | None:
        """First spoken word mapped to a NavActions key, for user-facing hints."""
        target = self._nav_actions.get(action_key)
        if target is None:
            return None
        for spoken, value in self._nav_translate.items():
            if value is target:
                return spoken
        return None

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
        seen_keys: set[str] = set()
        seen_targets: list[Any] = []

        translate = self._loader.LoadTranslateMap(frame.Folder, self._language)
        for spoken, target in translate.items():
            key = self._InferInternalKey(spoken, target, frame.ModuleDict)
            entries.append(ContextEntry(Spoken=spoken, InternalKey=key, Target=target))
            seen_spoken.add(DictionaryLoader.NormalizeSpoken(spoken))
            seen_keys.add(DictionaryLoader.NormalizeSpoken(key))
            seen_targets.append(target)

        # El diccionario interno (module_dict) es un *fallback* en inglés
        # para claves que todavía no tienen traducción. Si la clave interna
        # ya tiene alias hablado (por texto o por destino ya visto vía
        # _InferInternalKey), no se debe repetir como entrada aparte: eso es
        # lo que hacía aparecer "explorer" junto a "explorador" en el log.
        for internal_key, target in frame.ModuleDict.items():
            norm_word = DictionaryLoader.NormalizeSpoken(internal_key)
            if norm_word in seen_spoken or norm_word in seen_keys:
                continue
            if any(self._SameTarget(target, t) for t in seen_targets):
                continue
            entries.append(
                ContextEntry(
                    Spoken=internal_key,
                    InternalKey=internal_key,
                    Target=target,
                )
            )
        return entries

    @staticmethod
    def _SameTarget(a: Any, b: Any) -> bool:
        """True si dos destinos son "el mismo" submenú/comando.

        Compara por identidad primero (caso normal). Si ambos son dict
        (subcontexto), también compara por claves: dos re-importaciones del
        mismo módulo de diccionario (p. ej. por rutas de sys.path
        duplicadas) producen dos objetos distintos mismo con idéntico
        contenido, y no deben listarse como dos submenús separados.
        """
        if a is b:
            return True
        if isinstance(a, dict) and isinstance(b, dict):
            return a.keys() == b.keys()
        return False

    #: Alias publico de _SameTarget. Quien recorre Context desde afuera (la GUI,
    #: el adapter) necesita deduplicar igual que el Browser; sin esto terminan
    #: llamando al privado, como venia haciendo BrowserVoiceAdapter.
    IsSameTarget = _SameTarget

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

    def _DescendToSubContext(self, entry: ContextEntry) -> bool:
        """Descend manually into a sub-folder context.

        Returns:
            True si se pudo resolver y apilar el subcontexto. False si
            ResolveSubFolder no encontró una carpeta real para la clave
            (dato roto en el diccionario): se registra el error y el
            Browser se queda en el contexto actual en vez de apilar un
            frame que apuntaría a la misma carpeta que su padre.
        """
        try:
            folder = self._loader.ResolveSubFolder(
                self._stack[-1].Folder, entry.InternalKey, entry.Target
            )
        except FileNotFoundError as error:
            print(f"[DAV-Browser] {error}")
            return False
        frame = _ContextFrame(
            Folder=folder,
            ModuleDict=entry.Target,
            InternalName=entry.InternalKey,
        )
        self._stack.append(frame)
        self.Context = self._BuildContextForFrame(frame)
        
        if self._on_descend is not None:
            self._on_descend(entry)
            
        return True

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
                    descended = self._DescendToSubContext(entry)
                    self.OriginalContext = self.Context
                    if descended:
                        return BrowserResult(True, "descend", f"Ascending: descended into {entry.InternalKey}")
                    return BrowserResult(False, "descend_failed", f"No se pudo entrar a {entry.InternalKey}")
        
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
