"""Network connectivity helpers."""

from __future__ import annotations

import socket
import urllib.request


def has_internet(timeout: float = 3.0) -> bool:
    """Return True if a connection to a public host can be established."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        pass
    try:
        with urllib.request.urlopen(
            "https://alphacephei.com/vosk/models/model-list.json",
            timeout=timeout,
        ):
            return True
    except OSError:
        return False
