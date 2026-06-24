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
    print('  line - Crea un segmento de linea recta entre dos puntos en el espacio 3D.')
    print('          Requiere: X1, Y1, Z1 (float) — coordenadas del punto inicial. Default: (0, 0, 0).')
    print('                    X2, Y2, Z2 (float) — coordenadas del punto final.   Default: (10, 10, 0).')
    print('          Nota: Genera una arista (edge), no un solido.')
    print('                Disponible desde Part -> Primitives.')