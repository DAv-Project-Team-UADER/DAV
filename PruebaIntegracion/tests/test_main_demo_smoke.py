import os
import sys
from pathlib import Path
import subprocess

# Asegurar que el repo root está en sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def test_main_demo_subprocess_smoke():
    # Ejecutar el main en modo demo con pocas iteraciones
    cmd = [sys.executable, '-m', 'PruebaIntegracion.main', '--demo', '--max-iter', '1']
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    assert proc.returncode == 0, f"Main demo falló: {proc.stderr}\n{proc.stdout}"
    out = proc.stdout + proc.stderr
    assert 'Demo' in out or 'crear_punto' in out or 'Token escuchado' in out
