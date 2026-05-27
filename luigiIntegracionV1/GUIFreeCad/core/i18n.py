"""Simple JSON-based internationalization."""

from __future__ import annotations

import json
from pathlib import Path

I18N_DIR = Path(__file__).resolve().parent.parent / "i18n"
_cache: dict[str, dict[str, str]] = {}


def _load(lang: str) -> dict[str, str]:
    if lang not in _cache:
        path = I18N_DIR / f"{lang}.json"
        fallback = I18N_DIR / "es.json"
        source = path if path.exists() else fallback
        _cache[lang] = json.loads(source.read_text(encoding="utf-8"))
    return _cache[lang]


def tr(key: str, lang: str, **kwargs: str) -> str:
    strings = _load(lang)
    text = strings.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


def clear_cache() -> None:
    _cache.clear()
