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

"""Spanish spoken-word mapping for TechDraw workbench dictionary."""

from .TechDraw import techdraw

TraduceToEs = {
    # Submenús de TechDraw
    "vistas":                 techdraw["views"],
    "vista":                  techdraw["views"],
    "vistas principales":     techdraw["views"],

    "dimensiones":            techdraw["dimensions"],
    "dimension":              techdraw["dimensions"],
    "dimensión":              techdraw["dimensions"],
    "cotas":                  techdraw["dimensions"],
    "cota":                   techdraw["dimensions"],
    "acotaciones":            techdraw["dimensions"],
    "acotacion":              techdraw["dimensions"],
    "acotación":              techdraw["dimensions"],
    "medidas":                techdraw["dimensions"],

    "lineas":                 techdraw["addlines"],
    "líneas":                 techdraw["addlines"],
    "linea":                  techdraw["addlines"],
    "línea":                  techdraw["addlines"],
    "agregar lineas":         techdraw["addlines"],
    "agregar líneas":         techdraw["addlines"],

    "simbolos":               techdraw["symbols"],
    "símbolos":               techdraw["symbols"],
    "simbolo":                techdraw["symbols"],
    "símbolo":                techdraw["symbols"],

    "capturas":               techdraw["snaps"],
    "enganches":              techdraw["snaps"],
    "snaps":                  techdraw["snaps"],
    "puntos de ajuste":       techdraw["snaps"],

    "topologia":              techdraw["topology"],
    "topología":              techdraw["topology"],
    "elementos topológicos":  techdraw["topology"],

    "pagina":                 techdraw["page"],
    "página":                 techdraw["page"],
    "hoja":                   techdraw["page"],
    "hoja de dibujo":         techdraw["page"],
    "plantilla":              techdraw["page"],

    "anotaciones":            techdraw["annotations"],
    "anotacion":              techdraw["annotations"],
    "anotación":              techdraw["annotations"],
    "notas":                  techdraw["annotations"],
    "texto":                  techdraw["annotations"],

    "sombreado":              techdraw["hatching"],
    "rayado":                 techdraw["hatching"],
    "hatch":                  techdraw["hatching"],
    "tramas":                 techdraw["hatching"],

    "vertices":               techdraw["addvertices"],
    "vértices":               techdraw["addvertices"],
    "vertice":                techdraw["addvertices"],
    "vértice":                techdraw["addvertices"],
    "agregar vértices":       techdraw["addvertices"],

    "otras vistas":           techdraw["otherviews"],
    "vistas auxiliares":      techdraw["otherviews"],
    "proyecciones":           techdraw["otherviews"],

    "caracteristicas":        techdraw["features"],
    "características":        techdraw["features"],
    "elementos":              techdraw["features"],

    "ayuda":                  techdraw["help"],
    "informacion":            techdraw["help"],
    "información":            techdraw["help"],
    "opciones":               techdraw["help"],
}