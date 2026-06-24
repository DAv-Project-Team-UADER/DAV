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

# ayuda.py - StdView / Tree

def ayuda():
    print("=== Tree ===")
    print("  collapse: Colapsa todos los documentos abiertos en el árbol de modelo, dejando visible sol | Req: Al menos un documento con ítems expandidos en el árbol de mo")
    print("  preselection: Alterna el resaltado previo (pre-selección) de objetos en la vista 3D al pasar e | Req: Un documento abierto con árbol de modelo visible.")
    print("  recordselection: Alterna el registro del historial de selecciones en el árbol de modelo, permitie | Req: Un documento abierto con árbol de modelo visible.")
    print("  singleexpand: Alterna el modo de expansión única en el árbol de modelo: al expandir un nodo, l | Req: Un documento abierto con árbol de modelo visible y múltiples")
    print("  syncplacement: Alterna la sincronización del placement (posición y orientación) de objetos al r | Req: Un documento con objetos que tengan placement y árbol de mod")
    print("  syncselection: Alterna la sincronización automática del árbol de modelo con el objeto seleccion | Req: Un documento abierto con árbol de modelo visible.")
    print("  syncview: Alterna la sincronización automática de la vista 3D activa con el elemento selec | Req: Un documento abierto con árbol de modelo visible.")
