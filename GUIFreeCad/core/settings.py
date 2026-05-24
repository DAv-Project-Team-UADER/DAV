"""Persistent application settings."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULTS: dict[str, Any] = {
    "language": "es",
    "model_size": "small",
    "theme": "light",
    "startup_enabled": False,
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

    def as_dict(self) -> dict[str, Any]:
        return deepcopy(self._data)


settings = Settings()
