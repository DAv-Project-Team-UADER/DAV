import os
import sys
from pathlib import Path

# Asegurar que el repo root está en sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from PruebaIntegracion.core.CargadorConTraducciones import CargadorConTraducciones
from PruebaIntegracion.core.Navegador import Navegador


def test_cargador_detecta_demo_y_ejecuta_funcion():
    c = CargadorConTraducciones()
    roots = c.cargar()
    assert 'Demo' in roots, 'No se detectó la carpeta Demo en dic/'
    demo = roots['Demo']
    assert 'crear_punto' in demo.elementos, 'crear_punto no cargada'

    # El Navegador recibe un NodoContexto raíz; usamos el nodo Demo cargado.
    nav = Navegador(demo)
    resultado = nav.llamar('crear_punto', 2.5, context_keys=['Demo'])
    assert isinstance(resultado, dict), 'Resultado esperado dict'
    assert resultado.get('valor') == 2.5
