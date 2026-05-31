# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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
# SPDX-License-Identifier: GPL-3.0-or-later

def ayuda():
    print("Comandos disponibles en Expressions:")
    print("  copyactdoc     - Copia todas las expresiones del documento activo para poder pegarlas en otro documento.")
    print("  copyalldoc     - Copia todas las expresiones de todos los documentos abiertos en la sesión actual.")
    print("  copyselected   - Las expresiones de los objetos seleccionados quedan en el portapapeles de expresiones.")
    print("  paste          - Las expresiones copiadas se aplican a los objetos del documento activo.")