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

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import loft_profiles, pad_sketch


def _create_additive_primitive(type_id: str, default_name: str, is_3d: bool = True) -> None:
    doc = App.activeDocument()
    if doc is None:
        doc = App.newDocument()
    body = doc.addObject("PartDesign::Body", "Body")
    obj = doc.addObject(type_id, default_name)
    body.addObject(obj)
    doc.recompute()
    try:
        from createobjects import CreateObjects
    except ImportError:
        try:
            from selection.createobjects import CreateObjects
        except ImportError:
            from Dav.scr.selection.createobjects import CreateObjects
    CreateObjects(ObjectName=obj.Name, Is3D=is_3d).Execute()


def _execute_gui_command_with_objects(command_name: str, is_3d: bool = True) -> None:
    try:
        Gui.activateWorkbench("PartDesignWorkbench")
    except Exception:
        pass
    Gui.runCommand(command_name, 0)
    active_doc = App.ActiveDocument
    if not active_doc or not getattr(active_doc, 'ActiveObject', None):
        return
    obj_name = active_doc.ActiveObject.Name
    try:
        from createobjects import CreateObjects
    except ImportError:
        from selection.createobjects import CreateObjects
    CreateObjects(ObjectName=obj_name, Is3D=is_3d).Execute()


def additive_box() -> None:
    _create_additive_primitive("PartDesign::AdditiveBox", "Box", is_3d=True)


def additive_cone() -> None:
    _create_additive_primitive("PartDesign::AdditiveCone", "Cone", is_3d=True)


def additive_cylinder() -> None:
    _create_additive_primitive("PartDesign::AdditiveCylinder", "Cylinder", is_3d=True)


def additive_ellipsoid() -> None:
    _create_additive_primitive("PartDesign::AdditiveEllipsoid", "Ellipsoid", is_3d=True)


def additive_prism() -> None:
    _create_additive_primitive("PartDesign::AdditivePrism", "Prism", is_3d=True)


def additive_sphere() -> None:
    _create_additive_primitive("PartDesign::AdditiveSphere", "Sphere", is_3d=True)


def additive_torus() -> None:
    _create_additive_primitive("PartDesign::AdditiveTorus", "Torus", is_3d=True)


def additive_wedge() -> None:
    _create_additive_primitive("PartDesign::AdditiveWedge", "Wedge", is_3d=True)


def pad() -> None:
    _execute_gui_command_with_objects('PartDesign_Pad', is_3d=True)


def revolution() -> None:
    _execute_gui_command_with_objects('PartDesign_Revolution', is_3d=True)


additive = {
    'pad':               pad,
    'revolution':        revolution,
    'additivehelix':     lambda: Gui.runCommand('PartDesign_AdditiveHelix', 0),
    'additiveloft':      lambda: Gui.runCommand('PartDesign_AdditiveLoft', 0),
    'additivepipe':      lambda: Gui.runCommand('PartDesign_AdditivePipe', 0),
    'additivebox':       additive_box,
    'additivecone':      additive_cone,
    'additivecylinder':  additive_cylinder,
    'additiveellipsoid': additive_ellipsoid,
    'additiveprism':     additive_prism,
    'additivesphere':    additive_sphere,
    'additivetorus':     additive_torus,
    'additivewedge':     additive_wedge,
    'pad_sketch':        pad_sketch,
    'loft_profiles':     loft_profiles,
    'help':              ayuda,
}
