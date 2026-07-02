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

"""Mapeamento de palavras em portugues para o dicionario DAV AssemblyWorkbench."""
 
from .AssemblyWorkbench import assembly
from .joint.joint import joint
from .ayuda import ayuda
 
TraduceToPt = {
    "novo conjunto":       assembly["create"],
    "criar conjunto":      assembly["create"],
    "nova peca":           assembly["newpart"],
    "inserir peca":        assembly["newpart"],
    "inserir link":        assembly["link"],
    "vincular peca":       assembly["link"],
    "resolver":            assembly["solve"],
    "resolver conjunto":   assembly["solve"],
    "vista explodida":     assembly["view"],
    "criar vista":         assembly["view"],
    "simulacao":           assembly["simulation"],
    "criar simulacao":     assembly["simulation"],
    "lista de materiais":  assembly["bom"],
    "bom":                 assembly["bom"],
    "preferencias":        assembly["preferences"],
    "configuracoes":       assembly["preferences"],
    "fixar peca":          assembly["grounded"],
    "ancora":              assembly["grounded"],
    "junta":               joint,

    "ajuda":               joint['help'],
    "informação":          joint['help'],
    "opções":              joint['help']
}