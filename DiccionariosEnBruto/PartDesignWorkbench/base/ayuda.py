def ayuda():
    print('Comandos disponibles en base:')
    print('  body            - Crea el contenedor Body para agrupar features de PartDesign')
    print('  newsketch       - Crea un nuevo Sketch dentro del Body activo')
    print('  clone           - Crea una copia dependiente de un Body o feature')
    print('  subshapebinder  - Referencia geometría externa de otro Body dentro del Body activo')
    print('\nPrecondiciones:')
    print('  - newsketch y subshapebinder requieren que exista un Body activo.')
    print('  - clone y subshapebinder requieren tener un elemento seleccionado previamente.')
