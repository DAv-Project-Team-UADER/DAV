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
 
from .Assembly import assembly
from .joint.joint import joint
from .ayuda import ayuda
 
TraduceToPt = {
    "novo conjunto":       assembly["create"],
    "criar conjunto":      assembly["create"],
    "nova peça":           assembly["newpart"],
    "inserir peça":        assembly["newpart"],
    "inserir link":        assembly["link"],
    "vincular peça":       assembly["link"],
    "resolver":            assembly["solve"],
    "resolver conjunto":   assembly["solve"],
    "fixar":      assembly["solve"],
    "montar conjunto":     assembly["create"],
    "fazer conjunto":         assembly["solve"],
    "verificar conjunto":     assembly["solve"],
    "conjunto":              assembly["create"],
    "arranjo":                assembly["solve"],
    
    "vista explodida":     assembly["view"],
    "explodir vista":      assembly["view"],
    "explodir":   assembly["view"],
    "criar vista":         assembly["view"],
    "simulação":           assembly["simulation"],
    "criar simulação":     assembly["simulation"],
    "lista de materiais":  assembly["bom"],
    "bom":                 assembly["bom"],
    "lista":               assembly["bom"],
    "materiais":           assembly["bom"],
    "preferências":        assembly["preferences"],
    "configurações":       assembly["preferences"],
    "fixar peça":          assembly["grounded"],
    "ancora":              assembly["grounded"],
    "junta":               joint,
    "vincular peças":        joint,
    "vincular partes":       joint,
    "vincular":             joint,
    "juntar":               joint,
    "unir":                joint,
    "conectar":            joint,
    "junto":                joint,

    # Juntas por voz (sem dialogo)
    "junta fixa":            assembly["fixed_joint"],
    "fixar pecas":           assembly["fixed_joint"],

    "junta giratoria":       assembly["revolute_joint"],
    "dobradica":             assembly["revolute_joint"],

    "junta deslizante":      assembly["slider_joint"],
    "deslizar pecas":        assembly["slider_joint"],

    "junta por distancia":   assembly["distance_joint"],
    "separar pecas":         assembly["distance_joint"],

    "junta por angulo":      assembly["angle_joint"],
    "angulo entre pecas":    assembly["angle_joint"],

    "fixar ao chao":         assembly["ground_part"],
    "ancorar peca":          assembly["ground_part"],

    # Juntas restantes por voz
    "junta esferica":        assembly["ball_joint"],
    "rotula":                assembly["ball_joint"],
    "junta cilindrica":      assembly["cylindrical_joint"],
    "junta paralela":        assembly["parallel_joint"],
    "junta perpendicular":   assembly["perpendicular_joint"],

    "junta de engrenagens":  assembly["gears_joint"],
    "junta de correia":      assembly["belt_joint"],
    "junta de parafuso":     assembly["screw_joint"],
    "junta de cremalheira":  assembly["rack_pinion_joint"],

    "ajuda":               joint['help'],
    "informação":          joint['help'],
    "opções":              joint['help']
}