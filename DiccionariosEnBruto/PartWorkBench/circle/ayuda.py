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
    print('Comandos disponibles en este nivel:')
    print('  circle - Crea un circulo completo o arco circular como arista (edge), no como solido.')
    print('            Requiere: Radius (float) — radio del circulo. Default: 2 mm.')
    print('                      Angle1 (float) — angulo de inicio del arco. Default: 0 grados.')
    print('                      Angle2 (float) — angulo de fin del arco. Default: 360 grados.')
    print('            Nota: Con Angle1=0 y Angle2=360 se obtiene un circulo completo.')
    print('                  Con valores distintos se obtiene un arco.')
    print('                  Este objeto es una arista, no una cara ni un solido.')
    print('                  Para crear una cara circular usar Face From Wires.')
