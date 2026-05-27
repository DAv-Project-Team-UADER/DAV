def ayuda():
    print('Comandos disponibles en este nivel:')
    print('  linear - Crea una dimensión lineal, o cota, con su medida.')
    print('           Requiere: punto1, punto2, punto3.')
    print('           Nota: Las coordenadas de cada punto son relativas al origen. Las coordenadas del punto3 definen un punto por donde pasará la recta de la cota.')
    print('')
    print('  flip   - Invierte la orientación del texto de una dimensión Draft rotándolo 180°.')
    print('           Requiere: OBJ (un objeto dimensión).')
    print('           Nota: Modifica la propiedad Normal del objeto. No funciona correctamente con dimensiones angulares.')