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


def _status_file() -> Path:
    return _history_file().parent / "voice_status.json"


def export_voice_status(status: str, detail: str = "") -> None:
    import json
    path = _status_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"status": status, "detail": detail}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    _publish_status_to_panel(status, detail)


def _publish_status_to_panel(status: str, detail: str) -> None:
    """Refleja el estado en el panel acoplado, si esta montado.

    Se engancha aca porque export_voice_status es el punto unico por el que
    pasa todo cambio de estado del motor; asi el cartel del microfono no
    depende de que alguien se acuerde de avisarle al panel.
    """
    try:
        from integration.dav_dock_panel import get_source
    except ImportError:
        return
    try:
        source = get_source()
        if source is not None:
            source.PublishStatus(status, detail)
    except Exception:  # noqa: BLE001 - el estado no vale un fallo
        pass


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
