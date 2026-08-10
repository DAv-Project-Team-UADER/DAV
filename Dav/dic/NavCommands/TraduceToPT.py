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
# SPDX-License-Identifier: GPL-3.0-or-later

"""Portuguese spoken-word mapping for Browser navigation commands."""

from .NavActions import NavActions

TraduceToPT = {
    # Subir um nível na navegação
    "subir":          NavActions["up"],
    "voltar":         NavActions["up"],
    "atras":          NavActions["up"],
    "atrás":          NavActions["up"],
    "sair":           NavActions["up"],
    "regressar":      NavActions["up"],
    "retroceder":     NavActions["up"],

    # Mostrar o contexto atual
    "contexto":       NavActions["show_context"],
    "onde estou":     NavActions["show_context"],
    "o que posso dizer": NavActions["show_context"],
    "opcoes disponiveis": NavActions["show_context"],
    "opções disponíveis": NavActions["show_context"],
    "mostrar contexto": NavActions["show_context"],
    "localizacao":    NavActions["show_context"],
    "localização":    NavActions["show_context"],
}
