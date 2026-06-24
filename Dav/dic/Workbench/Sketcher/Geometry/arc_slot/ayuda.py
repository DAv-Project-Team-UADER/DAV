def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  arc_ends  - Crea una ranura curva con bordes redondeados.')
    print('              Requiere: Objeto croquis activo, coordenadas del centro, radio central, ángulos de inicio/fin y radio de los semicírculos.')
    print('')
    print('  flat_ends - Crea una ranura curva con bordes planos.')
    print('              Requiere: Objeto croquis activo, coordenadas del centro, radios interno/externo y ángulos de inicio/fin.')
    print('')
    print('              Nota: Ambas variantes insertan geometrías y restricciones formando un contorno cerrado válido.')