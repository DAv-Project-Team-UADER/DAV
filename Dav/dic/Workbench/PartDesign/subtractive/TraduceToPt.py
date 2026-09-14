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

"""Portuguese spoken-word mapping for PartDesign subtractive commands."""

from .subtractive import subtractive
from .ayuda import ayuda
from measure import CreateDimension

TraduceToPt = {
    # Pocket
    "bolso": subtractive["pocket"],
    "corte": subtractive["pocket"],

    # Groove
    "ranhura": subtractive["groove"],
    "canal": subtractive["groove"],

    # Hole
    "furo": subtractive["hole"],
    "perfuração": subtractive["hole"],

    # Subtractive Box
    "caixa sustractiva": subtractive["subtractivebox"],
    "corte caixa": subtractive["subtractivebox"],

    # Subtractive Cone
    "cono sustractivo": subtractive["subtractivecone"],
    "corte cono": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindro sustractivo": subtractive["subtractivecylinder"],
    "corte cilindro": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoide sustractivo": subtractive["subtractiveellipsoid"],
    "corte elipsoide": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helice subtrativa": subtractive["subtractivehelix"],
    "corte helice": subtractive["subtractivehelix"],

    # Subtractive Loft
    "loft sustractivo": subtractive["subtractiveloft"],
    "corte loft": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tubo sustractivo": subtractive["subtractivepipe"],
    "corte tubo": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prisma sustractivo": subtractive["subtractiveprism"],
    "corte prisma": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esfera sustractiva": subtractive["subtractivesphere"],
    "corte esfera": subtractive["subtractivesphere"],

    # Subtractive Torus
    "toro sustractivo": subtractive["subtractivetorus"],
    "corte toro": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cuna sustractiva": subtractive["subtractivewedge"],
    "corte cuna": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operação booleana": subtractive["boolean"],

    # Cortes por medida ditada (sem dialogo)
    "vazio por medida":      subtractive["pocket_by_length"],
    "esvaziar por medida":   subtractive["pocket_by_length"],

    "furo por medidas":      subtractive["hole_by_size"],
    "perfurar por medidas":  subtractive["hole_by_size"],

    "ranhura por angulo":    subtractive["groove_by_angle"],

    # Cortes com primitivas por medidas ditadas
    "cortar caixa por medidas":    subtractive["cut_box_by_size"],
    "cortar cilindro por medidas": subtractive["cut_cylinder_by_size"],
    "cortar esfera por raio":      subtractive["cut_sphere_by_radius"],

    # Help
    "ajuda": subtractive['help'],
    "informação": subtractive['help'],
    "opções": subtractive['help'],

    # MEASURE
    "medir": CreateDimension,
    "medida": CreateDimension,
    "medir distancia": CreateDimension,
    "medir distância": CreateDimension,
    "distância": CreateDimension,
    "distancia": CreateDimension,
    "cotar": CreateDimension,
    "dimensionar": CreateDimension,
    "aferir": CreateDimension,
    "mensurar": CreateDimension,
    "calcular distância": CreateDimension,
    "calcular distancia": CreateDimension,
    "comprimento": CreateDimension,
    "separação": CreateDimension,
    "separacao": CreateDimension,
    "afastamento": CreateDimension,
    "extensão": CreateDimension,
    "extensao": CreateDimension,
    "cota": CreateDimension,
    "cotagem": CreateDimension,
    "acotação": CreateDimension,
    "acotacao": CreateDimension,
    "dimensão": CreateDimension,
    "dimensao": CreateDimension,
    "métrica": CreateDimension,
    "metrica": CreateDimension,
    "dimensionamento": CreateDimension,
    "metro": CreateDimension,
    "milímetro": CreateDimension,
    "milimetro": CreateDimension,
    "centímetro": CreateDimension,
    "centimetro": CreateDimension,
    "flexômetro": CreateDimension,
    "flexometro": CreateDimension,
    "metro enrolável": CreateDimension,
    "metro enrolavel": CreateDimension,
    "régua": CreateDimension,
    "regua": CreateDimension,
    "escalímetro": CreateDimension,
    "escalimetro": CreateDimension,
    "calibre": CreateDimension,
    "paquímetro": CreateDimension,
    "paquimetro": CreateDimension,
    "micrômetro": CreateDimension,
    "micrometro": CreateDimension,
    "tolerância": CreateDimension,
    "tolerancia": CreateDimension,
    "desvio": CreateDimension,
    "ajuste": CreateDimension,
    "medição": CreateDimension,
    "medicao": CreateDimension,
    "mensuração": CreateDimension,
    "mensuracao": CreateDimension,
    "aferição": CreateDimension,
    "afericao": CreateDimension,
    "calibração": CreateDimension,
    "calibracao": CreateDimension,
    "verificação": CreateDimension,
    "verificacao": CreateDimension,
    "inspeção": CreateDimension,
    "inspecao": CreateDimension,
    "controle dimensional": CreateDimension,
    "metrologia": CreateDimension,
}