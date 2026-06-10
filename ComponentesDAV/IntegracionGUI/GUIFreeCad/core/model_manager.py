"""Vosk model verification and download (small bundled, large on demand)."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Callable
from urllib.request import urlretrieve

from core.settings import MODELS_DIR

MODEL_BASE_URL = "https://alphacephei.com/vosk/models/"

# language code -> (small_folder, large_folder)
MODEL_CATALOG: dict[str, tuple[str, str]] = {
    "en": ("vosk-model-small-en-us-0.15", "vosk-model-en-us-0.22"),
    "es": ("vosk-model-small-es-0.42", "vosk-model-es-0.42"),
    "pt": ("vosk-model-small-pt-0.3", "vosk-model-pt-fb-v0.1.1-20220516_2113"),
}


def _model_path(folder_name: str) -> Path:
    return MODELS_DIR / folder_name


def _is_valid_model(path: Path) -> bool:
    if not path.is_dir():
        return False
    markers = ("am", "graph", "conf", "ivector", "final.mdl", "Gr.fst")
    return any((path / name).exists() for name in markers)


def has_small_model(language: str) -> bool:
    if language not in MODEL_CATALOG:
        return False
    small_name, _ = MODEL_CATALOG[language]
    return _is_valid_model(_model_path(small_name))


def has_large_model(language: str) -> bool:
    if language not in MODEL_CATALOG:
        return False
    _, large_name = MODEL_CATALOG[language]
    return _is_valid_model(_model_path(large_name))


def verify_small_models() -> dict[str, bool]:
    """Check all bundled small models. Returns {lang: available}."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    return {lang: has_small_model(lang) for lang in MODEL_CATALOG}


def get_active_model_path(language: str, size: str) -> Path | None:
    """Resolve model path for language and size preference."""
    if language not in MODEL_CATALOG:
        return None
    small_name, large_name = MODEL_CATALOG[language]
    if size == "large" and has_large_model(language):
        return _model_path(large_name)
    if has_small_model(language):
        return _model_path(small_name)
    if size == "large" and has_large_model(language):
        return _model_path(large_name)
    return None


def download_large_model(
    language: str,
    progress_callback: Callable[[int, int], None] | None = None,
) -> Path:
    """Download and extract the large model for a language."""
    if language not in MODEL_CATALOG:
        raise ValueError(f"Unsupported language: {language}")

    _, large_name = MODEL_CATALOG[language]
    dest_dir = _model_path(large_name)
    zip_path = MODELS_DIR / f"{large_name}.zip"
    url = f"{MODEL_BASE_URL}{large_name}.zip"

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    def _reporthook(block_num: int, block_size: int, total_size: int) -> None:
        if progress_callback and total_size > 0:
            downloaded = block_num * block_size
            progress_callback(min(downloaded, total_size), total_size)

    urlretrieve(url, zip_path, reporthook=_reporthook)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(MODELS_DIR)

    zip_path.unlink(missing_ok=True)

    extracted = MODELS_DIR / large_name
    if not extracted.exists():
        candidates = [p for p in MODELS_DIR.iterdir() if p.is_dir() and large_name in p.name]
        if candidates:
            extracted = candidates[0]
            if dest_dir != extracted and not dest_dir.exists():
                shutil.move(str(extracted), str(dest_dir))

    if not _is_valid_model(dest_dir):
        raise RuntimeError(f"Downloaded model invalid: {large_name}")

    return dest_dir
