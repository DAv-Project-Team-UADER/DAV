def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  create - Dibuja un rectángulo en el croquis a partir de las coordenadas de dos esquinas opuestas ("rectángulo por esquinas").')
    print('           Requiere: Coordenadas de la primera esquina (X1, Y1) y de la esquina opuesta (X2, Y2) (int/float).')
    print('           Nota: Abre una ventana que pide cada valor por voz. Las esquinas pueden darse en cualquier orden.')
    print('')
    print('  center - Dibuja un rectángulo a partir de su centro y su tamaño ("rectángulo por centro").')
    print('           Requiere: Coordenadas del centro (X, Y), ancho y alto (int/float).')
    print('           Nota: Abre una ventana que pide cada valor por voz. Ideal cuando la figura debe quedar centrada.')
