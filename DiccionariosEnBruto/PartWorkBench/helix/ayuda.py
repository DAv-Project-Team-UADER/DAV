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
    print('  helice / primitive helix - Crea una hélice paramétrica (espiral en 3D).')
    print('         Requiere: Pitch  (float) — distancia entre vueltas consecutivas. Default: 1 mm.')
    print('                   Height (float) — altura total de la hélice. Default: 2 mm.')
    print('                   Radius (float) — radio inicial. Default: 1 mm.')
    print('                   Angle  (float) — ángulo cónico (0 = cilíndrica, >0 = cónica). Default: 0 grados.')
    print('         Nota: Genera una primitiva de alambre (wire), no sólida.')
    print('               Se usa frecuentemente como trayectoria para Sweep o roscas.')
    print('               Disponible desde Part -> Primitives.')
