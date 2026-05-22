import os
import sys
from pathlib import Path

# Asegurar que el repo root está en sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pytest
from PruebaIntegracion.core.ParamSpec import ParamSpec


def test_paramspec_accepts_correct_type():
    spec = ParamSpec(nombre='valor', tipo=float, requerido=True)
    # No debe lanzar excepción
    spec.validar(1.23)


def test_paramspec_rejects_wrong_type():
    spec = ParamSpec(nombre='valor', tipo=float, requerido=True)
    with pytest.raises(Exception):
        spec.validar('no-es-flotante')
