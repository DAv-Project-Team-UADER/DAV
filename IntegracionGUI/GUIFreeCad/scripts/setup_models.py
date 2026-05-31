#!/usr/bin/env python3
"""Download small Vosk models (en, es, pt) into models/."""

import sys
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"
BASE_URL = "https://alphacephei.com/vosk/models/"

SMALL_MODELS = [
    "vosk-model-small-en-us-0.15",
    "vosk-model-small-es-0.42",
    "vosk-model-small-pt-0.3",
]


def download_one(name: str) -> None:
    dest = MODELS_DIR / name
    if dest.is_dir() and any(dest.iterdir()):
        print(f"  [skip] {name} already exists")
        return

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = MODELS_DIR / f"{name}.zip"
    url = f"{BASE_URL}{name}.zip"
    print(f"  [download] {url}")
    urlretrieve(url, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(MODELS_DIR)
    zip_path.unlink(missing_ok=True)
    print(f"  [done] {name}")


def main() -> int:
    print("Downloading small Vosk models to:", MODELS_DIR)
    for name in SMALL_MODELS:
        try:
            download_one(name)
        except Exception as exc:
            print(f"  [error] {name}: {exc}", file=sys.stderr)
            return 1
    print("All small models ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
