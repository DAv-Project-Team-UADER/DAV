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

from .file import file

TraduceToPt = {
    ""novo": file["new"],
    "novo arquivo": file["new"],

    "abrir": file["open"],
    "abrir arquivo": file["open"],

    "salvar": file["save"],
    "salvar arquivo": file["save"],

    "salvar como": file["saveas"],
    "salvar documento como": file["saveas"],

    "salvar cópia": file["savecopy"],
    "duplicar arquivo": file["savecopy"],

    "reverter": file["revert"],
    "restaurar": file["revert"],

    "mesclar": file["merge"],
    "unir projetos": file["merge"],

    "importar": file["import"],
    "importar arquivo": file["import"],

    "exportar": file["export"],
    "exportar arquivo": file["export"],

    "recentes": file["recent"],
    "arquivos recentes": file["recent"],

    "carregar imagem": file["loadimage"],
    "abrir imagem": file["loadimage"],

    "ajuda": file["help"],
    "informação": file["help"],
    "opções": file["help"],
}
