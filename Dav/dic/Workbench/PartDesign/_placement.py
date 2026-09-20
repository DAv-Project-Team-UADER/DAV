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

"""Where a PartDesign primitive goes: its centre, dictated as X, Y, Z.

Las primitivas de FreeCAD nacen con una esquina o la base en el origen (la
caja, el cilindro, el cono, el prisma) o ya centradas (la esfera, el toro).
Para que la voz siempre hable del *centro* de la figura se corre la primitiva
la mitad de su tamaño en cada eje que corresponda.
"""

import FreeCAD as App

from .._prompts import askObject, askYesNo, isBody, isProfile


def chooseBody(doc, title: str):
    """Let the user pick, by voice, the body to work on among the valid ones.

    Abre siempre el menú de cuerpos ("avanzar" para cambiar, "okey" para
    elegir): así el usuario ve sobre qué se trabaja. Solo se ofrecen cuerpos
    con un sólido válido; uno con la última operación rota no puede ser base
    de un corte ("Cannot subtract primitive feature without base feature").

    Args:
        doc: Active FreeCAD document.
        title: Dialog title (the operation being prepared).

    Returns:
        The chosen body, or None when there is none or the user cancelled.
    """
    body = askObject(
        doc,
        title,
        "Elegí el cuerpo con el que trabajar",
        isBody,
        "[DAV] Error: no hay ningún cuerpo sólido válido. Creá un sólido primero "
        "o deshacé la última operación si quedó rota.",
    )
    if body is None:
        print("[DAV] Selección de cuerpo cancelada.")
    return body


def bodyForAdditive(doc, title: str):
    """Return the body a new additive figure goes into.

    Si ya hay cuerpos válidos pregunta "¿cuerpo nuevo?": con sí crea uno, con
    no abre el menú para elegir uno existente y la figura se suma a él. Sin
    cuerpos existentes crea uno nuevo sin preguntar.

    Args:
        doc: Active FreeCAD document.
        title: Dialog title (the operation being prepared).

    Returns:
        The body to build into, or None when the user cancelled.
    """
    if any(isBody(obj) for obj in doc.Objects):
        wantsNew = askYesNo(
            title,
            "¿Crear un cuerpo nuevo? Decí 'sí' para uno nuevo o 'no' para sumarla a uno existente",
        )
        if wantsNew is None:
            print("[DAV] Operación cancelada.")
            return None
        if not wantsNew:
            return chooseBody(doc, title)
    return doc.addObject("PartDesign::Body", "Body")


def placeAt(body, feature, x: float, y: float, z: float, rotation=None) -> None:
    """Move a primitive so that its origin lands on (x, y, z).

    Se ata al plano XY del origen del Body con un desplazamiento, que es lo
    que hace el panel nativo de las primitivas. Si el ataque falla se asigna
    la posición directamente.

    Args:
        body: Body that already holds the feature.
        feature: The PartDesign primitive to move.
        x: X of the primitive's origin, in millimetres.
        y: Y of the primitive's origin, in millimetres.
        z: Z of the primitive's origin, in millimetres.
        rotation: Optional ``App.Rotation`` applied about the origin (the wedge
            is born with its height along Y and is stood up with it).

    Example::

        placeAt(body, box, 0, 0, 5)
    """
    offset = App.Placement(App.Vector(x, y, z), rotation or App.Rotation())
    plane = next(
        (item for item in body.Origin.OriginFeatures if item.Role == "XY_Plane"), None
    )
    if plane is not None:
        try:
            feature.AttachmentSupport = [(plane, "")]
            feature.MapMode = "FlatFace"
            feature.AttachmentOffset = offset
            return
        except Exception as error:
            print(f"[DAV] No se pudo atar al plano XY ({error}); se usa la posición directa.")
    feature.Placement = offset


def askTwoProfiles(doc, title: str, firstMessage: str, secondMessage: str):
    """Ask, by voice, for two different drawings (loft sections, pipe profile and path).

    Args:
        doc: Active FreeCAD document.
        title: Dialog title (the operation being prepared).
        firstMessage: What the first drawing is for.
        secondMessage: What the second drawing is for.

    Returns:
        ``(first, second)``, or None when cancelled or there are not enough drawings.
    """
    empty = "[DAV] Error: no hay ningún dibujo para usar. Dibujá algo primero."
    first = askObject(doc, title, firstMessage, isProfile, empty)
    if first is None:
        return None
    second = askObject(doc, title, secondMessage, isProfile, empty)
    if second is None:
        return None
    if second is first:
        print("[DAV] Error: hay que elegir dos dibujos distintos.")
        return None
    return first, second


def sketchEdges(sketch) -> list:
    """Return the sub-element names of every edge of a sketch (``Edge1``, ``Edge2``...)."""
    return [f"Edge{index}" for index in range(1, len(sketch.Shape.Edges) + 1)]
