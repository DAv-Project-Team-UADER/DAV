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

"""Create a TechDraw page from a template and export it to PDF by voice.

Los diálogos nativos de TechDraw_PageTemplate y de la exportación a PDF no se
pueden manejar por voz. Acá se reemplazan reutilizando los mismos pasos que
Explorer/Proyecto: navegador de carpetas para elegir la plantilla (como
"abrir") y carpeta + nombre por voz para el PDF (como "guardar").
"""

from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui

PAGE_TYPE = "TechDraw::DrawPage"


def _project():
    """Return the Explorer/Proyecto helpers (voice browser, folder and name prompts)."""
    from dic.Explorer.Proyecto import _project

    return _project


def _templateDir() -> Path:
    """Return the folder where the template browser starts.

    Usa la carpeta de plantillas de las preferencias de TechDraw y, si no es
    legible, la que trae FreeCAD.
    """
    default = Path(App.getResourceDir()) / "Mod" / "TechDraw" / "Templates"
    try:
        configured = App.ParamGet("User parameter:BaseApp/Preferences/Mod/TechDraw/Files").GetString(
            "TemplateDir", ""
        )
    except Exception:
        configured = ""
    if configured and Path(configured).is_dir():
        return Path(configured)
    return default


def newPageFromTemplate() -> None:
    """Browse the folders by voice, pick an SVG template and create a page with it.

    Example::

        newPageFromTemplate()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo para crear la página.")
        return
    path = _project()._browse(
        _templateDir(),
        "Página desde plantilla",
        "Elegí la plantilla (.svg)",
        extensions=("svg",),
    )
    if path is None:
        print("[DAV] Plantilla cancelada.")
        return
    try:
        doc.openTransaction("Drawing create page")
        page = doc.addObject(PAGE_TYPE, "Page")
        template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
        page.Template = template
        template.Template = str(path)
        doc.commitTransaction()
        doc.recompute()
    except Exception as error:
        doc.abortTransaction()
        print(f"[DAV] Error: no se pudo crear la página con '{path}': {error}")
        return
    print(f"[DAV] Página creada con la plantilla '{path.name}'.")


def _pickPage(doc):
    """Return the page to export: the selected one, the only one, or the one chosen by voice."""
    pages = doc.findObjects(PAGE_TYPE)
    if not pages:
        return None
    for obj in Gui.Selection.getSelection(doc.Name):
        if obj.isDerivedFrom(PAGE_TYPE):
            return obj
    if len(pages) == 1:
        return pages[0]
    from Workbench._prompts import askObject

    return askObject(
        doc,
        "Exportar PDF",
        "Elegí la página",
        lambda obj: obj.isDerivedFrom(PAGE_TYPE),
        "[DAV] Error: no hay páginas para exportar.",
    )


def hasPage() -> bool:
    """Return True when the active document has at least one TechDraw page."""
    doc = App.activeDocument()
    return doc is not None and bool(doc.findObjects(PAGE_TYPE))


def exportPagePdf() -> None:
    """Export a TechDraw page to PDF, choosing folder and name by voice.

    Example::

        exportPagePdf()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo para exportar.")
        return
    page = _pickPage(doc)
    if page is None:
        print("[DAV] Exportar PDF cancelado: no hay página elegida.")
        return
    project = _project()
    path = project._askTarget(doc, "Exportar PDF", "pdf", project._safeName(page.Label) or "pagina")
    if path is None:
        print("[DAV] Exportar PDF cancelado.")
        return
    try:
        import TechDrawGui

        TechDrawGui.exportPageAsPdf(page, str(path))
    except Exception as error:
        print(f"[DAV] Error: no se pudo exportar '{path}': {error}")
        return
    print(f"[DAV] PDF exportado '{path}'.")
