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

"""Draft example: a simple title block, two rectangles and a text spelled letter by letter."""

from FreeCAD import Placement, Rotation, Vector

from ._common import activeDoc, fitView
from ._words import numbers

TITLE = {
    "es": "Draft: rótulo simple con texto",
    "en": "Draft: simple title block with text",
    "pt": "Draft: carimbo simples com texto",
}

# el texto es «A1»: una letra y un dígito, para deletrear poco
LABEL = "A1"
_SPELLING = {
    "es": ("a", "uno"),
    "en": ("a", "one"),
    "pt": ("a", "um"),
}
_CONFIRM = {"es": "okey", "en": "okey", "pt": "okey"}


def _rectangle(x1: float, y1: float, x2: float, y2: float):
    def action() -> None:
        import Draft

        doc = activeDoc()
        Draft.make_rectangle(
            x2 - x1, y2 - y1, placement=Placement(Vector(x1, y1, 0), Rotation())
        )
        doc.recompute()
        fitView()

    return action


def _text() -> None:
    import Draft

    doc = activeDoc()
    Draft.make_text([LABEL], placement=Placement(Vector(10, 12, 0), Rotation()))
    doc.recompute()
    fitView()


def _spellLabel(language: str) -> tuple:
    """Words that spell ``LABEL`` and finish the text («okey»)."""
    return (*_SPELLING.get(language, _SPELLING["es"]), _CONFIRM.get(language, "okey"))


def steps() -> list:
    """Return the frames of the title block example."""
    from InputPrompts.ExampleStep import ExampleStep

    return [
        ExampleStep(
            Text={
                "es": "Dibujá el marco del rótulo: un rectángulo de (0, 0) a (80, 30).",
                "en": "Draw the outer frame of the title block: a rectangle from (0, 0) to (80, 30).",
                "pt": "Desenhe a moldura do carimbo: um retângulo de (0, 0) a (80, 30).",
            },
            Path={
                "es": ("banco", "borrador", "crear", "rectangulo"),
                "en": ("workbench", "draft", "create", "rectangle"),
                "pt": ("trabalho", "draft", "criar", "retangulo"),
            },
            Values=lambda language: numbers(language, 0, 0, 80, 30),
            Action=_rectangle(0, 0, 80, 30),
        ),
        ExampleStep(
            Text={
                "es": "Agregá el recuadro interior: otro rectángulo de (4, 4) a (76, 26). Seguís en Crear: alcanza con «rectángulo».",
                "en": "Add the inner box: another rectangle from (4, 4) to (76, 26). You are still in Create: “rectangle” is enough.",
                "pt": "Adicione o quadro interno: outro retângulo de (4, 4) a (76, 26). Você continua em Criar: basta «retangulo».",
            },
            Path={"es": ("rectangulo",), "en": ("rectangle",), "pt": ("retangulo",)},
            Values=lambda language: numbers(language, 4, 4, 76, 26),
            Action=_rectangle(4, 4, 76, 26),
        ),
        ExampleStep(
            Text={
                "es": "Escribí el texto «A1» dentro del recuadro, en (10, 12). Primero «subir» a Borrador. Se deletrea: «a», «uno» y «okey» para terminar; después X e Y.",
                "en": "Write the text “A1” inside the box, at (10, 12). First go “up” to Draft. It is spelled: “a”, “one” and “okey” to finish; then X and Y.",
                "pt": "Escreva o texto «A1» dentro do quadro, em (10, 12). Primeiro «subir» ao Draft. Ele é soletrado: «a», «um» e «okey» para terminar; depois X e Y.",
            },
            Path={
                "es": ("subir", "anotacion", "texto"),
                "en": ("up", "annotation", "text"),
                "pt": ("subir", "anotacao", "texto"),
            },
            Values=lambda language: _spellLabel(language) + numbers(language, 10, 12),
            Action=_text,
        ),
    ]
