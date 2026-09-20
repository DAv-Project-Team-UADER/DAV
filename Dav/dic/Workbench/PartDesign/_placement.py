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

from .._prompts import askObject, isBody


def chooseBody(doc, title: str):
    """Return the body to work on: the only valid one, or the one picked by voice.

    Solo se ofrecen cuerpos con un sólido válido; uno con la última operación
    rota no puede ser base de un corte ("Cannot subtract primitive feature
    without base feature").

    Args:
        doc: Active FreeCAD document.
        title: Dialog title (the operation being prepared).

    Returns:
        The chosen body, or None when there is none or the user cancelled.
    """
    bodies = [obj for obj in doc.Objects if isBody(obj)]
    if not bodies:
        print(
            "[DAV] Error: no hay ningún cuerpo sólido válido. Creá un sólido primero "
            "o deshacé la última operación si quedó rota."
        )
        return None
    if len(bodies) == 1:
        return bodies[0]
    body = askObject(
        doc,
        title,
        "Elegí el cuerpo con el que trabajar",
        isBody,
        "[DAV] Error: no hay ningún cuerpo sólido válido.",
    )
    if body is None:
        print("[DAV] Selección de cuerpo cancelada.")
    return body


def placeAt(body, feature, x: float, y: float, z: float) -> None:
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

    Example::

        placeAt(body, box, 0, 0, 5)
    """
    offset = App.Placement(App.Vector(x, y, z), App.Rotation())
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
