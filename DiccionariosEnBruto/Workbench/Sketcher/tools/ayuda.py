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
    print('Comandos disponibles en tools:')
    print('  deleteconstraints - Elimina todas las restricciones | Req: Sketch en edición')
    print('  deletegeometry    - Elimina toda la geometría y restricciones | Req: Sketch en edición')
    print('  merge             - Une geometría de múltiples bocetos | Req: Al menos dos bocetos seleccionados')
    print('  reorient          - Reorienta el sketch seleccionado a otra cara | Req: Sketch seleccionado')
    print('  removeaxes        - Elimina el alineamiento a los ejes del objeto | Req: Objeto con ejes alineados')
