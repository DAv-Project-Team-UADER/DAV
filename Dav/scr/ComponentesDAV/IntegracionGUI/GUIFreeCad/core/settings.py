"""Persistent application settings."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _has_models(path: Path) -> bool:
    """True si la carpeta contiene al menos un modelo Vosk descargado."""
    try:
        return any(p.is_dir() and p.name.startswith("vosk-model") for p in path.iterdir())
    except (OSError, FileNotFoundError):
        return False


def _resolve_models_dir() -> Path:
    """Localiza la carpeta de modelos Vosk respetando DAV_MODELS_DIR.

    Orden de resolución (el layout DavCore ``Dav/models`` tiene prioridad):
      1. Variable de entorno DAV_MODELS_DIR (la setea el launcher).
      2. ``Dav/models`` del layout DavCore, si ya tiene modelos descargados.
      3. ``GUIFreeCad/models`` (modo dev / compatibilidad), si tiene modelos.
      4. ``Dav/models`` aunque esté vacía (setup_models.py descarga ahí).

    Returns:
        La carpeta de modelos a usar. La preferencia es ``Dav/models`` para
        que todo cargue desde un único lugar en el layout DavCore.
    """
    env = os.environ.get("DAV_MODELS_DIR", "").strip()
    if env:
        return Path(env)

    davcore = None
    for ancestor in PROJECT_ROOT.resolve().parents:
        candidate = ancestor / "Dav" / "models"
        if candidate.is_dir():
            davcore = candidate
            break

    # Dav/models con modelos ya descargados gana.
    if davcore is not None and _has_models(davcore):
        return davcore

    # Compatibilidad: GUIFreeCad/models si todavía tiene los modelos ahí.
    legacy = PROJECT_ROOT / "models"
    if _has_models(legacy):
        return legacy

    # Destino por defecto del layout DavCore (vacío -> setup_models descarga).
    return davcore if davcore is not None else legacy


MODELS_DIR = _resolve_models_dir()
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULTS: dict[str, Any] = {
    "language": "es",
    "model_size": "small",
    "theme": "light",
    "startup_enabled": False,
    "auto_voice": False,
}


class Settings:
    def __init__(self) -> None:
        self._data = deepcopy(DEFAULTS)
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.load()

    def load(self) -> None:
        if CONFIG_FILE.exists():
            try:
                stored = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
                if isinstance(stored, dict):
                    self._data.update({k: stored[k] for k in DEFAULTS if k in stored})
            except (json.JSONDecodeError, OSError):
                pass

    def save(self) -> None:
        CONFIG_FILE.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @property
    def language(self) -> str:
        return self._data["language"]

    @language.setter
    def language(self, value: str) -> None:
        if value in ("en", "es", "pt"):
            self._data["language"] = value

    @property
    def model_size(self) -> str:
        return self._data["model_size"]

    @model_size.setter
    def model_size(self, value: str) -> None:
        if value in ("small", "large"):
            self._data["model_size"] = value

    @property
    def theme(self) -> str:
        return self._data["theme"]

    @theme.setter
    def theme(self, value: str) -> None:
        if value in ("light", "dark"):
            self._data["theme"] = value

    @property
    def startup_enabled(self) -> bool:
        return bool(self._data["startup_enabled"])

    @startup_enabled.setter
    def startup_enabled(self, value: bool) -> None:
        self._data["startup_enabled"] = bool(value)

    @property
    def auto_voice(self) -> bool:
        return bool(self._data.get("auto_voice", False))

    @auto_voice.setter
    def auto_voice(self, value: bool) -> None:
        self._data["auto_voice"] = bool(value)

    def as_dict(self) -> dict[str, Any]:
        return deepcopy(self._data)


settings = Settings()
