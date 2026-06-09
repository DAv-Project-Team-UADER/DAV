def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  create - Dibuja un círculo completo en el croquis especificando su centro y su radio.')
    print('           Requiere: Centro X (int/float), Centro Y (int/float) y Radio (int/float).')
    print('           Nota: Devuelve un objeto geométrico de tipo círculo. El radio se define en las unidades del documento.')
    print('')
    print('  3point - Dibuja un círculo completo cuyo perímetro pasa exactamente por tres puntos especificados.')
    print('           Requiere: Coordenadas del primer punto (X1, Y1), segundo (X2, Y2) y tercero (X3, Y3) (int/float).')
    print('           Nota: Se asume que el usuario tiene un croquis abierto en modo edición.')