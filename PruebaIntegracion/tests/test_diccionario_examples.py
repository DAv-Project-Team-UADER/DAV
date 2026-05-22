def test_cargador_explorer_examples():
    from PruebaIntegracion.core.CargadorConTraducciones import CargadorConTraducciones
    from PruebaIntegracion.core.Navegador import Navegador

    c = CargadorConTraducciones()
    roots = c.cargar()
    assert 'ExplorerExamples' in roots

    nodo = roots['ExplorerExamples']
    # Debe exponer las funciones new y open
    assert 'new' in nodo.elementos
    assert 'open' in nodo.elementos

    nav = Navegador(nodo)
    # Llamar a new
    res = nav.llamar('new', 'prueba', context_keys=['ExplorerExamples'])
    assert isinstance(res, dict)
    assert res['action'] == 'new' and res['name'] == 'prueba'

    # Llamar a open
    res2 = nav.llamar('open', '/tmp/fichero', context_keys=['ExplorerExamples'])
    assert res2['action'] == 'open' and res2['path'] == '/tmp/fichero'
