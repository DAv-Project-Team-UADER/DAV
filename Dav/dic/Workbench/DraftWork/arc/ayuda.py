def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  center - Crea un arco circular definiendo centro, radio y ángulos.')
    print('           Requiere: center (Vector), radius (float), start_angle (float), end_angle (float).')
    print('           Nota: Los ángulos usualmente se expresan en grados.')
    print('')
    print('  points - Crea un arco de circunferencia que pasa exactamente por tres puntos.')
    print('           Requiere: pointslist (Lista de 3 Vectores).')
    print('           Nota: El orden de los puntos define la dirección del arco.')