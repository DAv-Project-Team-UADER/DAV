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

"""Words the Tagger uses to build automatic labels.

Sub-elements of a decomposed shape get labels like "Linea 1" or "Punto 3".
They are still selectable by their full label, but their individual words are
kept out of the search grammar: eight sub-elements would put "linea", "punto"
and the digits 1..4 into it, and those crowd out the name the user actually
wants to say (pendientes-dav.md §14).

Kept here, and not in code, so it follows the Tagger's own vocabulary: if
tagger.py gains a kind, add the word in the three languages here too.
"""


def GeneratedLabelWords() -> set[str]:
    """Return every word the Tagger can use as an automatic label prefix.

    All three languages at once: a document may have been built with the
    interface in another language, and its labels stay as they were written.

    Returns:
        Lowercase words, accent-free variants included.

    Example::

        "linea" in GeneratedLabelWords()   # True
    """
    words: set[str] = set()
    for table in (GeneratedLabelsEs, GeneratedLabelsEn, GeneratedLabelsPT):
        words.update(w.strip().lower() for w in table)
    return words


# Los mismos rotulos que produce Dav/scr/selection/tagger.py (_LABELS).
GeneratedLabelsEs = ("Punto", "Linea", "Superficie", "Arista", "Objeto")
GeneratedLabelsEn = ("Point", "Line", "Surface", "Edge", "Object")
GeneratedLabelsPT = ("Ponto", "Linha", "Superficie", "Aresta", "Objeto")
