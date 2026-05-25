# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

def ayuda():
    print("=== Subgrupo TechDraw: dimensions ===")
    print("  'horizontal' : Inserta una cota de distancia horizontal en el plano. | Req: Geometria elegida en la vista")
    print("  'extent'     : Inserta una cota de extension horizontal maxima. | Req: Vista proyectada activa")
    print("  'length'     : Inserta una cota de longitud axonometrica lineal. | Req: Arista seleccionada")
    print("  'radius'     : Inserta una cota de radio para un arco o circulo. | Req: Arco/circulo seleccionado")
    print("  'fit'        : Anade un indicador de ajuste y tolerancia eje-agujero. | Req: Cota de dimension activa")