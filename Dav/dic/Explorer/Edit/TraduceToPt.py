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

from .Edit import edit

TraduceToPt = {
    # Comandos de Desfazer / Refazer
    "desfazer":         edit["undo"],
    "reverter":         edit["undo"],
    "voltar":           edit["undo"],
    "refazer":          edit["redo"],
    "avançar":          edit["redo"],

    # Comandos de Área de Transferência e Seleção
    "cortar":           edit["cut"],
    "copiar":           edit["copy"],
    "colar":            edit["paste"],
    "duplicar":         edit["duplicate"],
    "clonar":           edit["duplicate"],
    "selecionar tudo":  edit["selectall"],
    "capturar tudo":    edit["selectall"],
    "excluir":          edit["delete"],
    "remover":          edit["delete"],
    "apagar":           edit["delete"],

    # Comandos de Transformação e Posicionamento
    "colocação":        edit["placement"],
    "posição":          edit["placement"],
    "definir posição":  edit["placement"],
    "transformar":      edit["transform"],
    "mover":            edit["transform"],
    "alinhar":          edit["align"],
    "alinhamento":      edit["align"],

    # Interface e Configuração
    "preferências":     edit["preferences"],
    "configurações":    edit["preferences"],
    "propriedades":     edit["properties"],
    "detalhes":         edit["properties"],
    "enviar para python": edit["sendtopython"],
    "console python":   edit["sendtopython"],
    "modo edição":      edit["editmode"],
    "modo modificar":   edit["editmode"],

    # Padronização de Ajuda
    "ajuda":            edit["help"],
    "informações":      edit["help"],
    "opções":           edit["help"]
}
