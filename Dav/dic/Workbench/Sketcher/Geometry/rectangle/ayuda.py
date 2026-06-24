def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  create - Dibuja un rectángulo en el croquis a partir de las coordenadas de dos esquinas opuestas.')
    print('           Requiere: Coordenadas de la primera esquina (X1, Y1) y coordenadas de la esquina opuesta (X2, Y2) (int/float).')
    print('           Nota: El motor de FreeCAD construye los rectángulos como cuatro segmentos de línea independientes agregados al croquis activo.')
    print('')
    print('  center - Dibuja un rectángulo centrado en el croquis a partir de un punto central y las coordenadas de una de sus esquinas.')
    print('           Requiere: Coordenadas del centro (CX, CY) y coordenadas de una esquina (X_esq, Y_esq) (int/float).')
    print('           Nota: Devuelve cuatro objetos geométricos de tipo segmento de línea agregados al croquis activo que conforman el rectángulo. Es ideal para modelado donde la figura debe estar centrada en el origen geométrico.')