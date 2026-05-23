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

from Archivos.ayuda      import ayuda as ayuda_archivos
from Ventanas.ayuda      import ayuda as ayuda_ventanas
from Intercambio.ayuda   import ayuda as ayuda_intercambio
from Herramientas.ayuda  import ayuda as ayuda_herramientas

def ayuda():
    ayuda_archivos()
    ayuda_ventanas()
    ayuda_intercambio()
    ayuda_herramientas()
