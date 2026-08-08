"""Shared voice history log for FreeCAD and the DAV window."""

from __future__ import annotations

from pathlib import Path


def _history_file() -> Path:
    here = Path(__file__).resolve()
    for ancestor in here.parents:
        candidate = ancestor / "config" / "voice_history.log"
        if candidate.parent.is_dir():
            return candidate
    return here.parents[1] / "config" / "voice_history.log"


def reset_voice_history() -> Path:
    path = _history_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    return path


def append_voice_history(text: str) -> Path:
    path = _history_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(text.rstrip() + "\n")
    return path


def read_voice_history_from(offset: int) -> tuple[list[str], int]:
    path = _history_file()
    if not path.exists():
        return [], 0
    with path.open("rb") as fh:
        fh.seek(offset)
        data = fh.read()
        new_offset = fh.tell()
    if not data:
        return [], new_offset
    text = data.decode("utf-8", errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    return lines, new_offset


def _context_file() -> Path:
    return _history_file().parent / "context_state.json"


def export_context_state(state: dict) -> None:
    import json
    path = _context_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def read_context_state() -> dict:
    import json
    path = _context_file()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _status_file() -> Path:
    return _history_file().parent / "voice_status.json"


def export_voice_status(status: str, detail: str = "") -> None:
    import json
    path = _status_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"status": status, "detail": detail}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_voice_status() -> tuple[str, str]:
    import json
    path = _status_file()
    if not path.exists():
        return "inactive", "Motor de voz no iniciado"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("status", "inactive"), data.get("detail", "")
    except Exception:
        return "inactive", "Error leyendo estado de voz"


def _queue_file() -> Path:
    return _history_file().parent / "command_queue.txt"


def write_command_queue(command: str) -> None:
    path = _queue_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(command.strip() + "\n")


def pop_command_queue() -> str | None:
    path = _queue_file()
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8").strip()
        if text:
            lines = [l for l in text.splitlines() if l.strip()]
            if lines:
                cmd = lines[0]
                remaining = lines[1:]
                path.write_text("\n".join(remaining) + ("\n" if remaining else ""), encoding="utf-8")
                return cmd
        return None
    except Exception:
        return None

