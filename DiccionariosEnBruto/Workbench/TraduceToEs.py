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

"""Spanish spoken-word mapping for the DAV Workbench dictionary."""

from .workbench import workbench
from .Assembly.Assembly import assembly
from .DraftWork.DraftWork import draft
from .Part.Part import part
from .PartDesign.partdesign import partdesign
from .Sketcher.sketcher import sketcher
from .TechDraw.TechDraw import techdraw

TraduceToEs = {
    # Banco de Ensamblaje
    "ensamblaje":        assembly,
    "ensamblajes":       assembly,
    "ensamble":          assembly,
    "ensambles":         assembly,
    "banco de ensamblaje": assembly,
    "banco de ensamble":   assembly,

    # Banco de Dibujo
    "dibujo":            draft,
    "dibujos":           draft,
    "banco de dibujo":   draft,
    "borrador":          draft,
    "borradores":        draft,
    "draftwork":         draft,
    "draft":             draft,

    # Banco de Piezas
    "pieza":             part,
    "piezas":            part,
    "banco de piezas":   part,
    "parte":             part,
    "partes":            part,
    "banco de partes":   part,

    # Banco de Diseño de Piezas
    "diseño de pieza":   partdesign,
    "diseño de piezas":  partdesign,
    "diseñador de piezas": partdesign,
    "diseño":            partdesign,
    "banco de diseño":   partdesign,
    "partdesign":        partdesign,
    "part design":       partdesign,

    # Banco de Croquis
    "croquis":           sketcher,
    "banco de croquis":  sketcher,
    "dibujar croquis":   sketcher,
    "dibujar":           sketcher,
    "sketcher":          sketcher,

    # Banco de Dibujo Técnico
    "dibujo técnico":    techdraw,
    "dibujos técnicos":  techdraw,
    "banco de dibujo técnico": techdraw,
    "techdraw":          techdraw,
    "dibujo de planos":  techdraw,
    "planos":            techdraw,

    "ayuda":             workbench["help"],
    "información":       workbench["help"],
    "opciones":          workbench["help"],
}