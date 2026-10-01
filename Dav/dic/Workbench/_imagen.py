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

"""Import an image (PNG, JPG, BMP) into the document by voice, for Draft and Sketcher.

Los comandos nativos que cargan imágenes (Std_ViewLoadImage, TechDraw_Image, BIM_ImagePlane)
abren el selector de archivos de Windows, que no se maneja por voz. Acá la imagen se elige
con el navegador de carpetas por voz y se coloca como un plano de imagen (``Image::ImagePlane``):

* Draft: en el plano XY, XZ o YZ, para calcar o usar de referencia.
* Croquis: sobre el plano del croquis, apenas detrás, para dibujar encima.

Se pregunta solo el ancho en mm (el alto sale de la proporción de la imagen) y si va
centrada en el origen; si no, el centro X e Y.
"""

import os
import struct

import FreeCAD as App

IMAGE_EXTENSIONS = ("png", "jpg", "jpeg", "bmp")

# En un croquis la imagen se pone un poco detrás de su plano para que no tape las líneas, en mm.
_SKETCH_DEPTH = 0.05


def _prompts():
    try:
        from Workbench import _prompts as prompts
    except ImportError:
        from dic.Workbench import _prompts as prompts
    return prompts


def _project():
    """Return the Explorer/Proyecto helpers (voice file browser)."""
    try:
        from Explorer.Proyecto import _project
    except ImportError:
        from dic.Explorer.Proyecto import _project
    return _project


def _pixelSize(path: str):
    """Return ``(width, height)`` in pixels of an image, or None when it cannot be read."""
    try:
        from PySide import QtGui

        image = QtGui.QImage(path)
        if not image.isNull():
            return image.width(), image.height()
    except Exception:
        pass
    try:  # PNG sin interfaz: el tamaño está en la cabecera
        with open(path, "rb") as handle:
            header = handle.read(24)
        if header[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", header[16:24])
    except Exception:
        pass
    return None


def _planeRotation(plane: str) -> App.Rotation:
    """Rotation that lays the image (its own XY plane) on the XY, XZ or YZ plane."""
    if plane == "XZ":
        return App.Rotation(App.Vector(1, 0, 0), 90)
    if plane == "YZ":
        return App.Rotation(App.Vector(1, 1, 1), 120)  # x->Y, y->Z, z->X
    return App.Rotation()


def _askImage(title: str):
    """Ask file, width and centre; returns ``(path, width, height, x, y)`` or None."""
    doc = App.activeDocument()
    project = _project()
    path = project._browse(
        project._startDir(doc),
        title,
        "Elegí la imagen (.png, .jpg, .bmp)",
        extensions=IMAGE_EXTENSIONS,
    )
    if path is None:
        print(f"[DAV] {title} cancelado.")
        return None
    prompts = _prompts()
    size = _pixelSize(str(path))
    width = prompts.askNumber(title, "Decí el ancho de la imagen en mm")
    if width is None:
        return None
    if width <= 0:
        print(f"[DAV] Error: el ancho tiene que ser mayor que cero (dijiste {width:g}).")
        return None
    if size is not None:
        height = width * size[1] / size[0]
    else:
        height = prompts.askNumber(title, "No pude leer la proporción: decí el alto de la imagen en mm")
        if height is None or height <= 0:
            return None
    centred = prompts.askYesNo(title, "¿Centrada en el origen?")
    if centred is None:
        return None
    x = y = 0.0
    if not centred:
        x = prompts.askNumber(title, "Decí la posición X del centro, en mm")
        if x is None:
            return None
        y = prompts.askNumber(title, "Decí la posición Y del centro, en mm")
        if y is None:
            return None
    return str(path), width, height, x, y


def _createPlane(doc, path: str, width: float, height: float, placement: App.Placement):
    try:
        doc.openTransaction("Import image")
        image = doc.addObject("Image::ImagePlane", "ImagePlane")
        image.Label = os.path.splitext(os.path.basename(path))[0]
        image.ImageFile = path
        image.XSize, image.YSize = width, height
        image.Placement = placement
        doc.commitTransaction()
        doc.recompute()
    except Exception as error:
        doc.abortTransaction()
        print(f"[DAV] Error: no se pudo importar la imagen '{path}': {error}")
        return None
    try:
        import FreeCADGui as Gui

        Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass
    return image


def importImageDraft() -> None:
    """Import an image as a plane in the XY, XZ or YZ plane, choosing everything by voice.

    Example::

        importImageDraft()
    """
    title = "Importar imagen"
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return
    plane = _prompts().askPlane()
    if plane is None:
        print(f"[DAV] {title} cancelado.")
        return
    answer = _askImage(title)
    if answer is None:
        return
    path, width, height, x, y = answer
    rotation = _planeRotation(plane)
    image = _createPlane(doc, path, width, height, App.Placement(rotation.multVec(App.Vector(x, y, 0)), rotation))
    if image is not None:
        print(f"[DAV] Imagen '{image.Label}' ({width:g} x {height:g} mm) en el plano {plane}.")


def _sketchInEdit():
    try:
        import FreeCADGui as Gui

        obj = getattr(Gui.ActiveDocument.getInEdit(), "Object", None)
        if obj is not None and obj.TypeId == "Sketcher::SketchObject":
            return obj
    except Exception:
        pass
    return None


def importImageSketch() -> None:
    """Import an image on the plane of a sketch, to draw over it, choosing everything by voice.

    Usa el croquis que se está editando; si no hay ninguno, se elige de la lista
    (``avanzar`` o ``buscar por deletreo``).

    Example::

        importImageSketch()
    """
    title = "Imagen en croquis"
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return
    sketch = _sketchInEdit()
    if sketch is None:
        sketch = _prompts().askObject(
            doc,
            title,
            "Elegí el croquis",
            lambda obj: obj.isDerivedFrom("Sketcher::SketchObject"),
            "[DAV] Error: no hay ningún croquis. Creá uno primero.",
        )
    if sketch is None:
        print(f"[DAV] {title} cancelado.")
        return
    answer = _askImage(title)
    if answer is None:
        return
    path, width, height, x, y = answer
    base = sketch.Placement.multVec(App.Vector(x, y, -_SKETCH_DEPTH))
    image = _createPlane(doc, path, width, height, App.Placement(base, sketch.Placement.Rotation))
    if image is not None:
        print(f"[DAV] Imagen '{image.Label}' ({width:g} x {height:g} mm) detrás del croquis '{sketch.Label}'.")
