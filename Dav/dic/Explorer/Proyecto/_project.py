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

"""Open, save and export a project without the native file dialogs.

Los diálogos nativos de FreeCAD (Std_Open, Std_SaveAs, Std_Export) no se
pueden manejar por voz. Acá se reemplazan por: un navegador de carpetas
(``FileSelectionInputPrompt``) para elegir qué abrir, y nombre sugerido o
deletreado más carpeta elegida por voz para guardar y exportar.

Las funciones de ``Explorer/File`` no se tocan: siguen disponibles.
"""

import importlib
import re
from pathlib import Path

import FreeCAD as App
import FreeCADGui as Gui

# Formatos que se ofrecen al abrir: el propio de FreeCAD y los que abre Gui.open.
OPEN_EXTENSIONS = ("FCStd", "step", "stp", "iges", "igs", "brep", "brp", "stl", "obj", "dxf")

# (extensión, etiqueta, palabras que la eligen directo). Las siglas se
# reconocen mal por voz: arriba/abajo y okey siempre funcionan.
EXPORT_FORMATS = (
    ("step", "STEP (.step)", ("step", "estep")),
    ("iges", "IGES (.iges)", ("iges", "aiges")),
    ("stl", "STL (.stl)", ("stl", "estl")),
    ("obj", "OBJ (.obj)", ("obj", "obj")),
    ("dxf", "DXF (.dxf)", ("dxf", "deqf")),
)

_ORIGIN_TYPES = ("App::Origin", "App::Line", "App::Plane", "App::Point")


def _importPrompts() -> None:
    """Make ``InputPrompts`` importable, wherever the dictionary was loaded from."""
    try:
        import InputPrompts  # noqa: F401
    except ImportError:
        from Workbench.Sketcher.new_sketch.new_sketch import _ensure_input_prompts_on_path

        _ensure_input_prompts_on_path()


def _startDir(doc=None) -> Path:
    """Return the folder to start browsing in.

    Prioridad: carpeta del documento, última carpeta usada por FreeCAD,
    Documentos y, por último, la carpeta del usuario.
    """
    if doc is not None and doc.FileName:
        folder = Path(doc.FileName).parent
        if folder.is_dir():
            return folder
    try:
        last = App.ParamGet("User parameter:BaseApp/Preferences/General").GetString(
            "FileOpenSavePath", ""
        )
    except Exception:
        last = ""
    if last and Path(last).is_dir():
        return Path(last)
    documents = Path.home() / "Documents"
    return documents if documents.is_dir() else Path.home()


def _browse(startDir: Path, title: str, message: str, extensions=None, foldersOnly=False):
    """Show the voice file browser and return the chosen path, or None."""
    _importPrompts()
    from InputPrompts.FileSelectionInputPrompt import FileSelectionInputPrompt
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
    from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

    prompt = FileSelectionInputPrompt(
        StartDir=startDir,
        Extensions=extensions,
        FoldersOnly=foldersOnly,
        Title=title,
        Message=message,
    )
    # el vocabulario abierto confunde las palabras de navegación: se acota la gramática
    PlaneGrammarSwitcher.ActivateGrammar(
        prompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage())
    )
    PromptVoiceRouter.SetActivePrompt(prompt)
    try:
        result = prompt.RequestValue()
    finally:
        PromptVoiceRouter.ClearActivePrompt(prompt)
        PlaneGrammarSwitcher.RestoreCadGrammar()
    if result is None or result.Cancelled or not result.Success:
        return None
    return Path(result.Value)


def _safeName(text: str) -> str:
    """Turn spoken or spelled text into a file name without special characters."""
    return re.sub(r"[^\w\-]+", "_", text.strip()).strip("_").lower()


def _askFileName(title: str, defaultName: str):
    """Ask for the file name: the suggested one or one spelled by voice.

    Returns:
        The name without extension, or None when cancelled.
    """
    from Workbench._prompts import askChoice, askText

    choice = askChoice(
        title,
        f"Nombre del archivo: '{defaultName}'",
        [
            ("suggested", f"Usar '{defaultName}'", ("sugerido", "mismo", "suggested", "same")),
            ("spell", "Deletrear otro nombre", ("deletrear", "otro", "nuevo", "spell", "other")),
        ],
    )
    if choice is None:
        return None
    if choice == "suggested":
        return defaultName
    spelled = askText(title, "Deletreá el nombre, 'espacio' entre palabras")
    name = _safeName(spelled) if spelled else ""
    if not name:
        print("[DAV] Error: el nombre quedó vacío.")
        return None
    return name


def _askFolder(title: str, defaultFolder: Path):
    """Ask whether to use the default folder or browse to another one."""
    from Workbench._prompts import askChoice

    choice = askChoice(
        title,
        f"Carpeta de destino: '{defaultFolder}'",
        [
            ("here", "Usar esa carpeta", ("aqui", "esa", "misma", "here", "same")),
            ("other", "Elegir otra carpeta", ("otra", "elegir", "other", "choose")),
        ],
    )
    if choice is None:
        return None
    if choice == "here":
        return defaultFolder
    return _browse(defaultFolder, title, "Elegí la carpeta de destino", foldersOnly=True)


def _confirmOverwrite(title: str, path: Path) -> bool:
    """Ask before replacing an existing file. Cancelling keeps it."""
    from Workbench._prompts import askChoice

    choice = askChoice(
        title,
        f"'{path.name}' ya existe. Decí 'sobrescribir' u 'okey' para reemplazarlo, 'cancelar' para dejarlo.",
        [("yes", "Sobrescribir", ("sobrescribir", "reemplazar", "overwrite"))],
    )
    return choice == "yes"


def _askTarget(doc, title: str, extension: str, defaultName: str):
    """Ask folder and name for a new file.

    Returns:
        The destination path, or None when the user cancelled.
    """
    folder = _askFolder(title, _startDir(doc))
    if folder is None:
        return None
    name = _askFileName(title, defaultName)
    if name is None:
        return None
    path = folder / f"{name}.{extension}"
    if path.exists() and not _confirmOverwrite(title, path):
        return None
    return path


def _exportObjects(doc) -> list:
    """Return what to export: the selection, else every visible top-level shape."""
    selected = list(Gui.Selection.getSelection(doc.Name))
    if selected:
        return selected
    objects = []
    for obj in doc.Objects:
        shape = getattr(obj, "Shape", None)
        if shape is None or shape.isNull() or obj.TypeId in _ORIGIN_TYPES:
            continue
        # lo que está dentro de un Body/Part ya viaja con su contenedor
        if obj.getParentGeoFeatureGroup() is not None:
            continue
        view = getattr(obj, "ViewObject", None)
        if view is not None and not view.Visibility:
            continue
        objects.append(obj)
    return objects


def openProject() -> None:
    """Browse the folders by voice and open the chosen file.

    Example::

        openProject()
    """
    path = _browse(
        _startDir(App.activeDocument()),
        "Abrir proyecto",
        "Elegí el archivo a abrir",
        extensions=OPEN_EXTENSIONS,
    )
    if path is None:
        print("[DAV] Abrir cancelado.")
        return
    try:
        Gui.open(str(path))
    except Exception as error:
        print(f"[DAV] Error: no se pudo abrir '{path}': {error}")
        return
    print(f"[DAV] Abierto '{path}'.")


def saveProject() -> None:
    """Save the active document, asking folder and name by voice when it is new.

    A document that already has a file is saved in place.

    Example::

        saveProject()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo para guardar.")
        return
    if doc.FileName:
        doc.save()
        print(f"[DAV] Guardado '{doc.FileName}'.")
        return
    path = _askTarget(doc, "Guardar proyecto", "FCStd", _safeName(doc.Label) or "proyecto")
    if path is None:
        print("[DAV] Guardar cancelado.")
        return
    try:
        doc.saveAs(str(path))
    except Exception as error:
        print(f"[DAV] Error: no se pudo guardar '{path}': {error}")
        return
    print(f"[DAV] Guardado '{path}'.")


def exportProject() -> None:
    """Export the selection (or all visible shapes) choosing format and file by voice.

    Example::

        exportProject()
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo para exportar.")
        return
    objects = _exportObjects(doc)
    if not objects:
        print("[DAV] Error: no hay nada visible para exportar.")
        return

    from Workbench._prompts import askChoice

    formats = [item for item in EXPORT_FORMATS if App.getExportType(item[0])]
    extension = askChoice("Exportar proyecto", "Elegí el formato", formats)
    if extension is None:
        print("[DAV] Exportar cancelado.")
        return
    path = _askTarget(doc, "Exportar proyecto", extension, _safeName(doc.Label) or "proyecto")
    if path is None:
        print("[DAV] Exportar cancelado.")
        return

    last_error = None
    for moduleName in App.getExportType(extension):
        try:
            importlib.import_module(moduleName).export(objects, str(path))
            print(f"[DAV] Exportado '{path}' ({len(objects)} objeto/s).")
            return
        except Exception as error:
            last_error = error
    print(f"[DAV] Error: no se pudo exportar '{path}': {last_error}")
