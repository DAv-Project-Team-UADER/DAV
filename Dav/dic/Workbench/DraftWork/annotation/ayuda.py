def ayuda():
    print("Comandos disponibles en Annotation")
    
    print("- text: Crea un texto plano (ShapeString, sin extruir) por voz.")
    print("  Requiere: Deletrear el texto, decir la altura de las letras y la posición (x, y).")
    
    print("- shape_string: Crea un objeto físico (geometría) a partir de un texto.")
    print("  Requiere: Un texto, una fuente, un tamaño y una coordenada de origen.")
    print("")
    print("- label: Crea una etiqueta con texto y una línea de referencia apuntando a un objeto.")
    print("  Requiere: Un objeto o subelemento seleccionado en la vista 3D.")