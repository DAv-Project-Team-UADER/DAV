#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Tests that voice errors reach the preferences UI (hotfix v1.0.5)."""

from __future__ import annotations

import os
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))

from speech.dav_voice_service import (  # noqa: E402
    DavVoiceService,
    _describe_exit,
    _PreferencesCallbacks,
)


def _serviceWithStatusLog() -> tuple[DavVoiceService, list[str]]:
    """Build a service attached to fake preferences that record every status."""
    statuses: list[str] = []
    service = DavVoiceService()
    service._mode = "preferences"
    service._prefs = _PreferencesCallbacks(
        on_command=lambda _cmd: None,
        on_text=None,
        on_status=statuses.append,
        on_audio=None,
        language="es",
    )
    return service, statuses


class StatusReachesPreferencesTest(unittest.TestCase):
    def test_errors_are_sent_while_the_mic_is_not_accepting_audio(self):
        # Los errores llegan justo cuando el micrófono no está escuchando;
        # antes _safe_call los descartaba y la UI nunca se enteraba.
        service, statuses = _serviceWithStatusLog()
        self.assertFalse(service._accept_callbacks)
        service._emit_prefs_status("error:mic:No hay ningún micrófono disponible")
        self.assertEqual(statuses, ["error:mic:No hay ningún micrófono disponible"])

    def test_closed_ui_does_not_break_the_voice_thread(self):
        service, _ = _serviceWithStatusLog()

        def _deletedWidget(_status):
            raise RuntimeError("Internal C++ object already deleted")

        service._prefs.on_status = _deletedWidget
        service._emit_prefs_status("active")  # no debe propagar la excepción

    def test_no_preferences_attached_is_a_no_op(self):
        service = DavVoiceService()
        service._emit_prefs_status("error:no_model")


class DescribeExitTest(unittest.TestCase):
    def test_exit_codes_are_readable(self):
        self.assertEqual(_describe_exit(None), "sin código")
        self.assertEqual(_describe_exit(5), "código 5")
        self.assertEqual(_describe_exit(-11), "SIGSEGV")
        self.assertIn("AVX", _describe_exit(-4))


@unittest.skipUnless(sys.platform.startswith("linux"), "el proceso aparte solo se usa en Linux")
class CrashedWorkerTest(unittest.TestCase):
    def test_crash_of_the_voice_process_is_reported_to_the_ui(self):
        with tempfile.TemporaryDirectory() as root:
            # Un "python" que se cae con SIGSEGV apenas arranca, como libvosk
            # en una CPU sin AVX o PortAudio sin dispositivos.
            python = Path(root) / ".venv" / "bin" / "python"
            python.parent.mkdir(parents=True)
            python.write_text("#!/bin/sh\nkill -SEGV $$\n", encoding="utf-8")
            python.chmod(0o755)

            service, statuses = _serviceWithStatusLog()
            timer = threading.Timer(10.0, service._stop_event.set)  # por si se cuelga
            timer.start()
            try:
                with mock.patch.dict(os.environ, {"DAV_GUI_FREECAD_ROOT": root}):
                    os.environ.pop("DAV_VOICE_INPROCESS", None)
                    service._listen_entry("/modelo/que/no/se/llega/a/usar")
            finally:
                timer.cancel()

        self.assertEqual(statuses, ["error:mic:El proceso de voz se cerro (SIGSEGV)"])
        self.assertFalse(service._running)


if __name__ == "__main__":
    unittest.main()
