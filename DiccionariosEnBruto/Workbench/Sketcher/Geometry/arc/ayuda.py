def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  center - Dibuja un segmento de arco especificando el centro, el radio, el ángulo inicial y el ángulo final.')
    print('           Requiere: Centro X, Centro Y, Radio, Ángulo inicial y Ángulo final (en grados).')
    print('           Nota: Devuelve un objeto de tipo arco agregado al croquis.')
    print('')
    print('  3point - Dibuja un segmento de arco a partir de dos puntos finales y otro punto intermedio sobre la circunferencia.')
    print('           Requiere: Coordenadas de inicio (X1, Y1), un punto intermedio (X2, Y2) y fin (X3, Y3).')
    print('           Nota: El orden es fundamental (inicio, curva, fin). Se requiere tener un croquis en modo edición.')