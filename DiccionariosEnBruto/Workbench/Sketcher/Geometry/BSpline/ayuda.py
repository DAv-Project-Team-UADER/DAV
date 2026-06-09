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
    print('=== B-Spline ===')
    print('  create - Crea una curva B-Spline a partir de puntos de control o nudos de interpolación.')
    print('          Permite curvas abiertas o periódicas (cerradas).')
    print('          Requiere: croquis activo, lista de puntos, modo (control_points o knots),')
    print('               grado de curva y parámetro periódico.')
    print('  interpolation - Crea una B-Spline que pasa exactamente por los puntos indicados.')
    print('                 Utiliza interpolación de nudos.')
    print('                 Requiere: croquis activo, lista de puntos y parámetro periódico.')
    print('  periodic - Crea una B-Spline periódica (cerrada) a partir de puntos de control.')
    print('            Requiere: croquis activo, lista de puntos de control y grado de curva.')
    print('  periodic interpolation - Crea una B-Spline cerrada que interpola exactamente')
    print('                          los puntos especificados.')
    print('                          Requiere: croquis activo y lista de puntos.')
    