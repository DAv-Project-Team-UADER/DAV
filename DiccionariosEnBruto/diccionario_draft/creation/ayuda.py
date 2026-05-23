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
    print("=== Creation ===")
    print("clave  |  requerimientos")
    print("hatch: crea un objeto hatch a partir de un objeto base y un patron de relleno  |  req: un objeto base ")
    print("point: crea un punto en las coordenadas X, Y, Z  |  req: coordenadas X, Y, Z")
    print("polygon: crea un polígono regular  |  req: nfaces (int/caras), radius (float/radio)")
    print("rectangle: crea un rectángulo  |  req: length (float/largo), height (float/ancho)")