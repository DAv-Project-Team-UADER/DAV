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
    print('=== Ellipse ===')
    print('  create by center - Crea una elipse completa especificando centro,')
    print('                    radio mayor y radio menor.')
    print('                    Requiere: croquis activo, centro X/Y,')
    print('                         radio mayor y radio menor.')
    print('  create by 3 points - Crea una elipse a partir de los extremos')
    print('                      de un eje y un tercer punto de amplitud.')
    print('                      Requiere: croquis activo y tres puntos de referencia.')
    print('  arc of ellipse - Crea un arco de elipse definiendo centro,')
    print('                  radios y ángulos inicial y final.')
    print('                  Requiere: croquis activo, centro X/Y,')
    print('                       radio mayor, radio menor,')
    print('                       ángulo inicial y ángulo final.')
    print('  arc of hyperbola - Crea un arco de hipérbola usando')
    print('                    centro, radios y parámetros de recorte.')
    print('                    Requiere: croquis activo, centro X/Y,')
    print('                         radio mayor, radio menor,')
    print('                         parámetro inicial y final.')
    print('  arc of parabola - Crea un arco de parábola a partir')
    print('                   del foco, vértice y parámetros de recorte.')
    print('                   Requiere: croquis activo, foco X/Y,')
    print('                        vértice X/Y, parámetro inicial')
    print('                        y parámetro final.')