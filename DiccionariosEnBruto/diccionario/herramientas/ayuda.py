# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo PartDesign: herramientas ===")
    print("  'body'          : Crea un nuevo Body en el documento activo. | Req: Documento activo")
    print("  'nuevocroquis'  : Crea un nuevo Sketch en el Body activo. | Req: Body activo seleccionado")
    print("  'booleana'      : Operación booleana entre Bodies. | Req: Al menos 2 Bodies en el documento")
    print("  'clonar'        : Clona una Feature del Body activo. | Req: Feature seleccionada en el Body")
    print("  'eje'           : Abre el Asistente de diseño de ejes. | Req: Documento activo (requiere matplotlib)")
    print("  'movertip'      : Mueve el Tip del modelo a la Feature seleccionada. | Req: Feature seleccionada")
    print("  'moverfeature'  : Mueve una Feature a otro Body. | Req: Feature y Body destino seleccionados")
    print("  'moverarbolfeat': Mueve una Feature a otra posición en el árbol. | Req: Feature seleccionada")
    print("  'binder'        : Crea un SubShapeBinder. | Req: Body activo + objeto fuente con Shape")
