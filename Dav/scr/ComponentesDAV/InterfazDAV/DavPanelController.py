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

"""Feeds a DavPanel from the file bridge; swappable for the in-process Browser."""

from __future__ import annotations

import json
import os
from pathlib import Path

from PySide6.QtCore import QObject, QTimer

from ContextView import ContextView
from DavPanel import DavPanel


class FileBridgeSource(QObject):
    """Reads the voice state FreeCAD writes to ``GUIFreeCad/config``.

    This is the transitional half of the migration: it isolates every file
    read and the 500 ms polling in one place, so ``DavPanel`` stays free of
    them. Once the panel is docked inside FreeCAD this class is replaced by
    direct ``Browser`` signals and deleted — the panel does not change.

    See ``Dav/docs/plan-unificacion-guis.md`` §4.

    Args:
        ConfigDir: directory holding the bridge files. Resolved from this
            file's location when omitted.
    """

    POLL_MS = 500

    def __init__(self, ConfigDir: Path | None = None) -> None:
        super().__init__()
        self._configDir = ConfigDir or self._DefaultConfigDir()
        self._historyOffset = 0
        self._lastContextRaw: dict | None = None

    @staticmethod
    def _DefaultConfigDir() -> Path:
        here = Path(__file__).resolve().parent
        return here.parent / "IntegracionGUI" / "GUIFreeCad" / "config"

    @property
    def ContextStatePath(self) -> Path:
        return self._configDir / "context_state.json"

    @property
    def CommandQueuePath(self) -> Path:
        return self._configDir / "command_queue.txt"

    @property
    def VoiceHistoryPath(self) -> Path:
        return self._configDir / "voice_history.log"

    @property
    def VoiceStatusPath(self) -> Path:
        return self._configDir / "voice_status.json"

    def ReadContext(self) -> ContextView | None:
        """Active context, or None when it did not change since last read."""
        raw = self._ReadJson(self.ContextStatePath)
        if raw is None or raw == self._lastContextRaw:
            return None
        self._lastContextRaw = raw
        return ContextView.FromDict(raw)

    def ReadStatus(self) -> tuple[str, str]:
        """Voice engine status as ``(status, detail)``."""
        raw = self._ReadJson(self.VoiceStatusPath)
        if not raw:
            return "inactive", ""
        return raw.get("status", "inactive"), raw.get("detail", "")

    def ReadNewHistory(self) -> list[str]:
        """Lines appended to the history log since the previous call."""
        path = self.VoiceHistoryPath
        if not path.exists():
            return []
        try:
            with path.open("rb") as handle:
                handle.seek(self._historyOffset)
                data = handle.read()
                self._historyOffset = handle.tell()
        except OSError:
            return []
        if not data:
            return []
        text = data.decode("utf-8", errors="replace")
        return [line.strip() for line in text.splitlines() if line.strip()]

    def SendCommand(self, Spoken: str) -> None:
        """Queue a phrase for FreeCAD to process, as if it had been spoken."""
        path = self.CommandQueuePath
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(f"{Spoken.strip()}\n")

    @staticmethod
    def _ReadJson(Path_: Path) -> dict | None:
        if not Path_.exists():
            return None
        try:
            return json.loads(Path_.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None


class DavPanelController(QObject):
    """Wires a DavPanel to a state source and keeps it up to date.

    Holds the glue that used to live inside ``MainWindow``: polling, parsing
    and command dispatch. Swapping ``Source`` for a Browser-backed one is the
    whole of migration stage 2 — the panel is untouched.

    Args:
        Panel: the widget to drive.
        Source: state source. A ``FileBridgeSource`` when omitted.

    Example::

        controller = DavPanelController(panel)
        controller.Start()
    """

    #: Prefijo con el que el motor publica lo que reconocio.
    _VOICE_PREFIX = "[DAV] Voz:"

    def __init__(self, Panel: DavPanel, Source: FileBridgeSource | None = None) -> None:
        super().__init__(Panel)
        self._panel = Panel
        self._source = Source or FileBridgeSource()

        self._panel.CommandRequested.connect(self._OnCommandRequested)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.Poll)

    def Start(self) -> None:
        """Begin polling the source."""
        self.Poll()
        self._timer.start(self._source.POLL_MS)

    def Stop(self) -> None:
        """Stop polling."""
        self._timer.stop()

    def Poll(self) -> None:
        """Read the source once and push any change into the panel."""
        status, detail = self._source.ReadStatus()
        self._panel.SetStatus(status, detail)

        for line in self._source.ReadNewHistory():
            if line.startswith(self._VOICE_PREFIX):
                spoken = line.split("Voz:", 1)[1].strip()
                self._panel.SetCurrentText(spoken)
            self._panel.AddToHistory(line, FromVoice=True)

        context = self._source.ReadContext()
        if context is not None:
            self._panel.RenderContext(context)

    def _OnCommandRequested(self, Spoken: str) -> None:
        try:
            self._source.SendCommand(Spoken)
        except OSError as error:
            self._panel.AddToHistory(f"No se pudo enviar «{Spoken}»: {error}", Unknown=True)
