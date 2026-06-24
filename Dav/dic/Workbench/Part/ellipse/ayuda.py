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
    print('  ellipse - Crea un arco eliptico o elipse completa como arista (edge) 2D.')
    print('           Requiere: MajorRadius (float) — semieje mayor. Default: 4 mm.')
    print('                     MinorRadius (float) — semieje menor. Default: 2 mm.')
    print('                     Angle1      (float) — angulo de inicio. Default: 0 grados.')
    print('                     Angle2      (float) — angulo de fin.   Default: 360 grados.')
    print('           Nota: Con Angle1=0 y Angle2=360 se obtiene la elipse completa.')
    print('                 Con valores parciales se obtiene un arco eliptico.')
    print('                 Es una arista (edge), no un solido.')
    print('                 Disponible desde Part -> Primitives.')