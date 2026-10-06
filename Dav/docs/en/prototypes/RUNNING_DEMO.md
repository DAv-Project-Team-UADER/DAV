# How to run the functional test (demo mode)

This document explains step by step how to run the functional test that validates the flow of loading, translation, navigation and function execution in `PruebaIntegracion` without depending on a microphone or on `Vosk`.

Minimum requirements

- Python 3.8+ (tested with Python 3.11)
- Virtual environment recommended

Optional (for real mode)

- `vosk` and `sounddevice` installed and a downloaded Vosk model.

Relevant files

- `PruebaIntegracion/main.py` — flexible startup (demo or real mode).
- `PruebaIntegracion/dic/` — contains loadable modules (an example `dic/Demo` is included).
- `PruebaIntegracion/core/CargadorConTraducciones.py` — scans `dic/` and builds the tree.
- `PruebaIntegracion/core/ExploradorVoz.py` — main navigation and execution loop.

1. Prepare the environment (optional but recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
# install optional dependencies (real mode only)
pip install vosk sounddevice
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install vosk sounddevice
```

2. Run with Vosk (real mode)

If you want to test with a microphone and Vosk, install the dependencies and pass `--modelo` pointing to the model directory (for example, `modelo/vosk-model-small-es-0.42`). The command is:

```bash
python -m main --modelo modelo/vosk-model-small-es-0.42
```

Notes and troubleshooting

- If `dic/` is empty, `main.py` uses a demo fallback (see `dic/Demo`). Add folders and `TraduceTo*.py` files to extend it.
- If the run keeps waiting, check that the demo script has `enviar` at the end of the selection phrase, because `Command` uses `enviar` as the confirmation.
- For real mode, if `vosk` raises errors when loading the model, make sure the `--modelo` path is correct and that the `vosk` package is installed in the active environment.


