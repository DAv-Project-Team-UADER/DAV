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

from .File import file

TraduceToEs = {
    "nuevo": file["new"],
    "nuevo archivo": file["new"],

    "abrir": file["open"],
    "abrir archivo": file["open"],

    "guardar": file["save"],
    "guardar archivo": file["save"],

    "guardar como": file["saveas"],
    "guardar documento como": file["saveas"],

    "guardar copia": file["savecopy"],
    "duplicar archivo": file["savecopy"],

    "revertir": file["revert"],
    "restaurar": file["revert"],

    "combinar": file["merge"],
    "unir proyectos": file["merge"],

    "importar": file["import"],
    "importar archivo": file["import"],

    "exportar": file["export"],
    "exportar archivo": file["export"],

    "recientes": file["recent"],
    "archivos recientes": file["recent"],

    "cargar imagen": file["loadimage"],
    "abrir imagen": file["loadimage"],

    "help": file["help"],
    "ayuda": file["help"],
    "opciones": file["help"],
}
