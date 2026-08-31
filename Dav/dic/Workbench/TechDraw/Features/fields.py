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

import codecs
import csv
import datetime
import os.path
from datetime import date

import FreeCAD as App
try:
    import TechDraw
except ImportError as _e:
    TechDraw = None  # type: ignore
    print(f"[DAV] TechDraw no disponible ({_e}); 'fields' queda como no-op.")

_ISO_A4_TEMPLATES = (
    "Mod/TechDraw/Templates/ISO/A4_Landscape_ISO5457_minimal.svg",
    "Mod/TechDraw/Templates/ISO/A4_Landscape_ISO5457_advanced.svg",
    "Mod/TechDraw/Templates/ISO/A4_Landscape_TD.svg",
)

_CSV_COLUMNS = (
    "CreatedByChkLst",
    "ScaleChkLst",
    "LabelChkLst",
    "CommentChkLst",
    "CompanyChkLst",
    "LicenseChkLst",
    "CreatedDateChkLst",
    "LastModifiedDateChkLst",
)


def _loadAliasSets():
    """Load lowercase template-field aliases from FreeCAD's CSV mapping file.

    Returns:
        dict[str, set[str]]: Category name to lowercase field aliases, or empty
        dict if the CSV is missing or invalid.
    """
    aliases = {column: set() for column in _CSV_COLUMNS}
    filePath = App.getResourceDir() + "Mod/TechDraw/CSVdata/FillTemplateFields.csv"
    if not os.path.exists(filePath):
        return aliases

    with codecs.open(filePath, encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        if list(reader.fieldnames or []) != list(_CSV_COLUMNS):
            return aliases
        for row in reader:
            for column in _CSV_COLUMNS:
                value = (row.get(column) or "").strip().lower()
                if value:
                    aliases[column].add(value)
    return aliases


def _findTechDrawPage():
    """Return the best TechDraw page in the active document.

    Prefers a page that already contains at least one view.

    Returns:
        TechDraw::DrawPage | None: Matching page, or None if unavailable.
    """
    doc = App.ActiveDocument
    if doc is None:
        print("No hay documento activo.")
        return None

    pages = doc.findObjects(Type="TechDraw::DrawPage")
    if not pages:
        print("No se encontró ninguna página TechDraw en el documento.")
        return None

    for page in pages:
        if page.Views:
            return page
    return pages[0]


def _firstScaledView(page):
    """Return the first page view that exposes a Scale property."""
    for view in page.Views:
        if hasattr(view, "Scale"):
            return view
    return None


def _isoTemplatePath():
    """Return the first available ISO A4 landscape template with a title block."""
    resourceDir = App.getResourceDir()
    for relativePath in _ISO_A4_TEMPLATES:
        fullPath = resourceDir + relativePath
        if os.path.exists(fullPath):
            return fullPath.replace("\\", "/")
    return None


def _ensureEditableTemplate(page):
    """Ensure the page template exposes editable title-block fields.

    FreeCAD's default A4 template is blank and has no editable texts, so
    ``TechDraw_FillTemplateFields`` cannot populate a rótulo on it.

    Args:
        page: TechDraw DrawPage object.

    Returns:
        bool: True when the page template has editable texts available.
    """
    template = page.Template
    if template is None:
        print("La página no tiene plantilla asociada.")
        return False

    if template.EditableTexts:
        return True

    isoPath = _isoTemplatePath()
    if isoPath is None:
        print(
            "La plantilla actual no tiene campos editables y no se encontró "
            "una plantilla ISO A4 con rótulo."
        )
        return False

    doc = App.activeDocument()
    doc.openTransaction("DAV upgrade TechDraw template")
    template.Template = isoPath
    doc.commitTransaction()
    doc.recompute()

    if not template.EditableTexts:
        print("No se pudieron cargar campos editables desde la plantilla ISO.")
        return False

    print(f"Plantilla actualizada a rótulo ISO: {os.path.basename(isoPath)}")
    return True


def _formatIsoDate(isoValue, sampleValue):
    """Format an ISO-8601 document timestamp for a template field."""
    try:
        dt = datetime.datetime.strptime(isoValue, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        dt = datetime.datetime.combine(date.today(), datetime.time.min)

    if sampleValue == "MM/DD/YYYY":
        return f"{dt.month}/{dt.day}/{dt.year}"
    if sampleValue == "YYYY-MM-DD":
        return f"{dt.year}-{dt.month}-{dt.day}"
    return f"{dt.day}/{dt.month}/{dt.year}"


def _scaleText(view):
    """Build a title-block scale string from a TechDraw view scale."""
    if view is None:
        return "1 : 1"
    if TechDraw is None:
        return f"1 : {getattr(view, 'Scale', 1)}"
    fracScale = TechDraw.nearestFraction(view.Scale)
    return f"{fracScale[0]} : {fracScale[1]}"


def _buildFieldUpdates(page, aliases):
    """Compute template-field values from the active document metadata.

    Args:
        page: TechDraw DrawPage object.
        aliases: Alias sets loaded from FillTemplateFields.csv.

    Returns:
        dict[str, str]: Mapping of template field names to new values.
    """
    doc = App.ActiveDocument
    view = _firstScaledView(page)
    updates = {}

    for fieldName, sampleValue in page.Template.EditableTexts.items():
        key = fieldName.lower()
        if key in aliases["CreatedByChkLst"]:
            updates[fieldName] = doc.CreatedBy or sampleValue
        elif key in aliases["ScaleChkLst"]:
            updates[fieldName] = _scaleText(view)
        elif key in aliases["LabelChkLst"]:
            updates[fieldName] = doc.Label or sampleValue
        elif key in aliases["CommentChkLst"]:
            updates[fieldName] = doc.Comment or sampleValue
        elif key in aliases["CompanyChkLst"]:
            updates[fieldName] = doc.Company or sampleValue
        elif key in aliases["LicenseChkLst"]:
            updates[fieldName] = doc.License or sampleValue
        elif key in aliases["CreatedDateChkLst"]:
            updates[fieldName] = _formatIsoDate(doc.CreationDate, sampleValue)
        elif key in aliases["LastModifiedDateChkLst"]:
            updates[fieldName] = _formatIsoDate(doc.LastModifiedDate, sampleValue)

    return updates


def fillTemplateFields():
    """Fill editable title-block fields on the active TechDraw page.

    Upgrades blank default templates to an ISO A4 title block when needed,
    then writes document metadata (author, title, scale, dates, etc.) into
    the matching template fields.

    Example::
        fillTemplateFields()
    """
    if TechDraw is None:
        print("TechDraw no disponible en este sistema; no se puede rellenar el rótulo.")
        return
    page = _findTechDrawPage()
    if page is None:
        return

    if page.Views == []:
        print("Agregá al menos una vista a la página antes de rellenar el rótulo.")
        return

    if not _ensureEditableTemplate(page):
        return

    aliases = _loadAliasSets()
    updates = _buildFieldUpdates(page, aliases)
    if not updates:
        print(
            "La plantilla no tiene campos reconocidos para autor, escala, título "
            "o fecha."
        )
        return

    doc = App.activeDocument()
    texts = dict(page.Template.EditableTexts)
    for _k, _v in updates.items():
        texts[_k] = _v

    doc.openTransaction("Fill template fields")
    page.Template.EditableTexts = texts
    doc.commitTransaction()
    doc.recompute()

    print("Rótulo actualizado:")
    for fieldName, value in updates.items():
        print(f"  {fieldName}: {value}")
