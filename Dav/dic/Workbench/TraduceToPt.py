# Copyright (C) 2026 El Equipo del Projeto DAV
# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# Sob a direção de Guillermo Gerard e Gallo Fabricio David
#
# Este programa é software livre: você pode redistribuir e/ou modificar
# sob os termos da Licença Pública Geral GNU conforme publicado
# pela Fundação para o Software Livre, na versão 3 da Licença.
#
# Este programa é distribuído na esperança de ser útil,
# mas SEM QUALQUER GARANTIA; mesmo sem a garantia implícita de
# COMERCIALIZAÇÃO ou ADEQUAÇÃO PARA UM PROPÓSITO ESPECÍFICO. Consulte
# a Licença Pública Geral GNU para mais detalhes.
#
# Você deveria ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa. Se não, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

"""Mapeamento de palavras em Português para o dicionário DAV Workbench."""
from .workbench import workbench
from .Assembly.Assembly import assembly
from .DraftWork.DraftWork import draft
from .Part.Part import part
from .PartDesign.partdesign import partdesign
from .Sketcher.sketcher import sketcher
from .TechDraw.TechDraw import techdraw

TraduceToPt = {
    # Bancada de Montagem
    "montagem":          assembly,
    "montagens":         assembly,
    "conjunto":          assembly,
    "conjuntos":         assembly,
    "bancada de montagem": assembly,
    "bancada de conjunto": assembly,
    "banco de montagem":   assembly,
    "articular":          assembly,
    "juntar":             assembly,
    "juntar peças":        assembly,

    # Bancada de Desenho
    "desenho":           draft,
    "desenhos":          draft,
    "bancada de desenho": draft,
    
    "rascunho":          draft,
    "rascunhos":         draft,
    "draftwork":         draft,
    "draft":             draft,
    "desenhar":          draft,
    

    # Bancada de Peça
    "peça":              part,
    "peças":             part,
    "bancada de peça":   part,
    "bancada de peças":  part,
    "parte":             part,
    "partes":            part,
    "pedaço":            part,
    "pedaços":           part,
    

    # Bancada de Design de Peças
    "desenho de peça":    partdesign,
    "desenho de peças":   partdesign,
    "designer de peças": partdesign,
    "desenhista":        partdesign,
    "design":            partdesign,
    "bancada de design": partdesign,
    "partdesign":        partdesign,
    "part design":       partdesign,
    "projeto de peça":     partdesign,
    "projeto de peças":    partdesign,
    

    # Bancada de Esboço
   
    "banco de esboço":   sketcher,
    "desenhar esboço":   sketcher,
    "sketcher":          sketcher,
    "croqui":            sketcher,
    "croquis":           sketcher,
    "esboço":            sketcher,
    "esboços":           sketcher,
    # Bancada de Desenho Técnico
    "desenho técnico":   techdraw,
    "desenhos técnicos": techdraw,
    "bancada de desenho técnico": techdraw,
    "techdraw":          techdraw,
    "desenho de planos": techdraw,
    "planos":            techdraw,
    "esboço técnico":    techdraw,
    "rótulo":             techdraw,
    "rótulos":            techdraw,
    "técnico":             techdraw,

    "ajuda":             workbench["help"],
    "informação":        workbench["help"],
    "opções":            workbench["help"],
}