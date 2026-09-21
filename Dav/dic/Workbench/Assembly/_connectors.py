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

"""Where two parts of an assembly join: the faces of a part, offered by voice.

Una junta necesita saber por qué lugar de cada pieza se une. FreeCAD lo resuelve con el
mouse (se hace clic en una cara); acá cada pieza ofrece una lista corta de caras que se
recorre con "abajo" y se elige con "okey": los cilindros primero (su eje es lo que se
suele querer alinear) y después las caras planas, de mayor a menor.
"""

from __future__ import annotations

import Part

from .._prompts import askChoice
from ..Sketcher.new_sketch._faces import _AXIS_NAMES

# tope de opciones: recorrerlas por voz se vuelve inmanejable con decenas de caras
_MAX_OPTIONS = 12


def _shapeOf(part):
    """Return the shape of ``part`` in its own coordinates (a link shows its linked body)."""
    target = part.getLinkedObject() if part.isDerivedFrom("App::Link") else part
    return target.Shape


def _numbered(labels: list[str]) -> list[str]:
    """Add a number to the repeated labels, so every option has its own name."""
    seen: dict[str, int] = {}
    named = []
    for label in labels:
        seen[label] = seen.get(label, 0) + 1
        named.append(label if seen[label] == 1 else f"{label} {seen[label]}")
    return named


def listConnectors(part) -> list[tuple[str, str]]:
    """List the faces of ``part`` where a joint can be attached.

    Args:
        part: A body, a part or a link to one.

    Returns:
        ``(faceName, label)`` pairs, cylinders first and then flat faces, each group from
        the largest face to the smallest. Empty when the part has no usable face.

    Example::

        listConnectors(link)  # [("Face1", "Cilindro de radio 3"), ("Face8", "Cara superior"), ...]
    """
    cylinders, planes = [], []
    for index, face in enumerate(_shapeOf(part).Faces, 1):
        surface = face.Surface
        if isinstance(surface, Part.Cylinder):
            cylinders.append((face.Area, f"Face{index}", f"Cilindro de radio {surface.Radius:g}"))
        elif isinstance(surface, Part.Plane):
            u, v = surface.parameter(face.CenterOfMass)
            normal = face.normalAt(u, v)
            key = tuple(int(round(c)) for c in (normal.x, normal.y, normal.z))
            planes.append((face.Area, f"Face{index}", f"Cara {_AXIS_NAMES.get(key, 'inclinada')}"))
    ordered = sorted(cylinders, key=lambda item: -item[0]) + sorted(planes, key=lambda item: -item[0])
    ordered = ordered[:_MAX_OPTIONS]
    labels = _numbered([label for _area, _name, label in ordered])
    return [(name, label) for (_area, name, _old), label in zip(ordered, labels)]


def askConnector(part, title: str):
    """Let the user pick, by voice, the face of ``part`` where the joint is attached.

    Args:
        part: The part being joined.
        title: Dialog title (the operation being prepared).

    Returns:
        The face name (``"Face3"``), or None when cancelled or the part has no usable face.
    """
    options = listConnectors(part)
    if not options:
        print(f"[assembly] Error: '{part.Label}' no tiene caras para unir.")
        return None
    return askChoice(
        title,
        f"¿Por dónde se une '{part.Label}'? 'abajo' para cambiar, 'okey' para elegir",
        [(name, label, ()) for name, label in options],
    )
