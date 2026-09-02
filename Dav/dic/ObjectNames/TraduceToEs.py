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

"""Spanish vocabulary for naming objects by voice.

frase hablada -> etiqueta que se escribe en el árbol.

Para agregar un nombre, agregar una línea acá: no hace falta tocar código.
Que sea una palabra corriente del español — Vosk no reconoce inventos ni
siglas (ver pendientes-dav.md §13.e).
"""

TraduceToEs = {
    # Formas
    "cubo":        "Cubo",
    "cuadrado":    "Cuadrado",
    "rectangulo":  "Rectangulo",
    "rectángulo":  "Rectangulo",
    "circulo":     "Circulo",
    "círculo":     "Circulo",
    "triangulo":   "Triangulo",
    "triángulo":   "Triangulo",
    "cilindro":    "Cilindro",
    "esfera":      "Esfera",
    "cono":        "Cono",
    "prisma":      "Prisma",
    "anillo":      "Anillo",
    "aro":         "Aro",

    # Piezas mecánicas
    "base":        "Base",
    "tapa":        "Tapa",
    "placa":       "Placa",
    "chapa":       "Chapa",
    "columna":     "Columna",
    "viga":        "Viga",
    "eje":         "Eje",
    "tubo":        "Tubo",
    "caño":        "Caño",
    "barra":       "Barra",
    "perno":       "Perno",
    "tornillo":    "Tornillo",
    "tuerca":      "Tuerca",
    "arandela":    "Arandela",
    "brida":       "Brida",
    "soporte":     "Soporte",
    "brazo":       "Brazo",
    "engranaje":   "Engranaje",
    "rueda":       "Rueda",
    "resorte":     "Resorte",

    # Muebles y objetos comunes
    "mesa":        "Mesa",
    "silla":       "Silla",
    "patas":       "Patas",
    "pata":        "Pata",
    "estante":     "Estante",
    "puerta":      "Puerta",
    "cajon":       "Cajon",
    "cajón":       "Cajon",
    "marco":       "Marco",
    "pared":       "Pared",
    "techo":       "Techo",
    "piso":        "Piso",

    # Genéricos
    "pieza":       "Pieza",
    "cuerpo":      "Cuerpo",
    "bloque":      "Bloque",
    "objeto":      "Objeto",
    "figura":      "Figura",
    "molde":       "Molde",
    "tapa superior": "Tapa superior",
    "tapa inferior": "Tapa inferior",
    "parte alta":  "Parte alta",
    "parte baja":  "Parte baja",
}
