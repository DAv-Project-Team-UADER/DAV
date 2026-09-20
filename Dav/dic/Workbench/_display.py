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

"""Make the result of a voice command visible in the 3D view.

Compartido por Part, PartDesign y Assembly.
"""

from __future__ import annotations


def leaveEditMode() -> None:
    """Close any object edit (a sketch, for instance) so the 3D view is shown.

    Mientras un boceto esta en edicion la vista 3D solo muestra el editor del
    boceto: lo que se cree en ese momento existe en el documento pero no se
    ve hasta salir de la edicion.
    """
    try:
        import FreeCADGui as Gui

        document = Gui.ActiveDocument
        if document is not None and document.getInEdit() is not None:
            document.resetEdit()
    except Exception as error:
        print(f"[DAV] No se pudo salir del modo edición: {error}")


def showResult(feature) -> None:
    """Leave edit mode, make feature visible and fit the view around it.

    Args:
        feature: The object that was just created.
    """
    leaveEditMode()
    try:
        import FreeCADGui as Gui

        view_object = getattr(feature, "ViewObject", None)
        if view_object is not None and hasattr(view_object, "Visibility"):
            view_object.Visibility = True
        Gui.updateGui()
        Gui.SendMsgToActiveView("ViewFit")
    except Exception as error:
        print(f"[DAV] No se pudo actualizar la vista: {error}")


def finishFeature(doc, feature, label: str, *, is3D: bool = True, hide=()) -> bool:
    """Recompute, validate, show and register a feature just created.

    Si el recompute falla, la feature rota se borra para no dejar el modelo
    inconsistente.

    Args:
        doc: Active FreeCAD document.
        feature: The object that was just created.
        label: Name used in the messages (e.g. "cylinder").
        is3D: Whether to register it in the DAV tree as a 3D solid.
        hide: Source objects to hide once the result exists.

    Returns:
        True when the feature is valid and shown.
    """
    doc.recompute()
    shape = getattr(feature, "Shape", None)
    if not feature.isValid() or (shape is not None and shape.isNull()):
        try:
            doc.removeObject(feature.Name)
            doc.recompute()
        except Exception:
            pass
        print(f"[DAV] Error: no se pudo crear {label} con esos datos.")
        return False

    for source in hide:
        try:
            source.Visibility = False
        except Exception:
            pass
    showResult(feature)
    try:
        try:
            from createobjects import CreateObjects
        except ImportError:
            from selection.createobjects import CreateObjects
        CreateObjects(ObjectName=feature.Name, Is3D=is3D).Execute()
    except Exception as error:
        print(f"[DAV] No se pudo registrar {feature.Name}: {error}")
    print(f"[DAV] Creado {label} '{feature.Name}'.")
    return True


def _jumpToContext(path: list, message: str) -> None:
    """Move the voice context to ``path`` and print ``message`` when it worked."""
    try:
        from integration.browser_voice_adapter import get_active_adapter

        adapter = get_active_adapter()
        browser = getattr(adapter, "_browser", None)
        if browser is not None and browser.JumpToPath(path):
            print(message)
    except Exception as error:
        print(f"[DAV] No se pudo cambiar el contexto de voz a {'/'.join(path)}: {error}")


def enterSketcherContext() -> None:
    """Hand the voice over to the Sketcher tools (lines, constraints, ...).

    Mientras se edita el boceto, FreeCAD cambia a las herramientas de croquis;
    el contexto de voz hace lo mismo para que todas queden al alcance.
    """
    _jumpToContext(["workbench", "sketcher"], "[DAV] Herramientas de croquis activadas.")


def enterPartDesignContext() -> None:
    """Hand the voice back to PartDesign once a sketch of a Body is closed.

    Al cerrar el croquis lo que sigue es extruir, girar, agujerear...: el
    contexto de voz vuelve a PartDesign para que esos comandos estén a mano.
    """
    _jumpToContext(["workbench", "partdesign"], "[DAV] Herramientas de PartDesign activadas.")
