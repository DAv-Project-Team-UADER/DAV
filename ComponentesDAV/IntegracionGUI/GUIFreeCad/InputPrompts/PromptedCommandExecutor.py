#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Execute Browser command entries with prompted parameter collection."""

from __future__ import annotations

import inspect
from typing import Any, Iterable

from InputPrompts.ParameterCollector import ParameterCollector
from InputPrompts.PromptResult import PromptResult


class PromptedCommandExecutor:
    """Callable executor for Browser(on_execute=...)."""

    def __init__(
        self,
        Language: str = "es",
        Parent=None,
        DelayMs: int = 30,
        Collector: ParameterCollector | None = None,
    ) -> None:
        self.Collector = Collector or ParameterCollector(
            Language=Language,
            Parent=Parent,
            DelayMs=DelayMs,
        )
        self.LastResult: PromptResult = PromptResult.Pending()

    def __call__(self, Entry: Any) -> Any | None:
        """Execute a Browser ContextEntry."""
        return self.ExecuteEntry(Entry)

    def ExecuteEntry(
        self,
        Entry: Any,
        SimulatedFinalTexts: Iterable[str] | None = None,
    ) -> Any | None:
        """Collect parameters if needed and execute Entry.Target."""
        if not self._IsCallableEntry(Entry):
            self.LastResult = PromptResult.Fail("Context entry is not callable.")
            self._PrintError(self.LastResult.Error)
            return None

        function = self._GetEntryTarget(Entry)
        collection_result = self.Collector.CollectForFunction(
            function,
            SimulatedFinalTexts=SimulatedFinalTexts,
        )
        self.LastResult = collection_result

        if collection_result.Cancelled:
            self._PrintMessage("[DAV] Command cancelled by user.")
            return None
        if not collection_result.Success:
            self._PrintError(f"[DAV] Command not executed: {collection_result.Error}")
            return None

        kwargs = collection_result.Value or {}
        try:
            if kwargs:
                result = function(**kwargs)
            else:
                result = function()
        except Exception as error:
            self.LastResult = PromptResult.Fail(str(error))
            self._PrintError(f"[DAV] Error executing command: {error}")
            return None

        self._PrintMessage(f"[DAV] Command executed: {getattr(Entry, 'InternalKey', function)}")
        return result

    @staticmethod
    def _IsCallableEntry(Entry: Any) -> bool:
        is_callable = getattr(Entry, "IsCallable", None)
        if callable(is_callable):
            return bool(is_callable())
        return callable(PromptedCommandExecutor._GetEntryTarget(Entry))

    @staticmethod
    def _GetEntryTarget(Entry: Any):
        target = getattr(Entry, "Target", None)
        if inspect.ismethod(target) and getattr(target, "__self__", None) is Entry:
            return target.__func__
        return target

    @staticmethod
    def _PrintMessage(Text: str) -> None:
        try:
            import FreeCAD as App

            App.Console.PrintMessage(Text.rstrip() + "\n")
        except ImportError:
            print(Text)

    @staticmethod
    def _PrintError(Text: str) -> None:
        try:
            import FreeCAD as App

            App.Console.PrintError(Text.rstrip() + "\n")
        except ImportError:
            print(Text)
