# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

def ayuda():
    print("=== Subgrupo TechDraw: AddLines ===")
    print("  'twoLines'  : Agrega una línea de eje central entre dos aristas. | Req: Dos aristas seleccionadas")
    print("  'twoPoints' : Agrega una línea de eje central entre dos puntos. | Req: Dos vértices seleccionados")
    print("  'cosmetic'  : Traza una línea cosmética de referencia entre dos puntos. | Req: Vista base activa")
    print("  'decorate'  : Permite alterar el color, grosor o visibilidad de aristas. | Req: Aristas seleccionadas")
    print("  'center'    : Agrega una línea central o eje de simetría a una cara. | Req: Cara seleccionada")