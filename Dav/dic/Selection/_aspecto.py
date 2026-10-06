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

"""Change the colour or the material of the selected objects by voice.

Los comandos nativos de FreeCAD (Std_SetMaterial, el color de superficie) abren
diálogos que no se manejan por voz. Acá el color y el material se eligen de una
lista corta que se dice o se recorre con arriba/abajo. «color» y «material» se dicen
solos, desde cualquier contexto: primero se elige de la lista y después se aplica a lo que
esté seleccionado; si no hay nada, se elige el objeto de la lista (``avanzar``) o
deletreando su nombre (``buscar por deletreo``).
"""

from __future__ import annotations

import FreeCAD as App

try:
    import FreeCADGui as Gui
except ImportError:  # sin interfaz no hay selección ni color de vista
    Gui = None

# (clave, nombre, color RGB 0-1, palabras por idioma). «Arriba» y «abajo» quedan libres:
# en el cuadro mueven la selección.
_COLORS = (
    ("red", "Rojo", (0.80, 0.10, 0.10), {"es": ("rojo",), "en": ("red",), "pt": ("vermelho",)}),
    ("orange", "Naranja", (0.95, 0.50, 0.10), {"es": ("naranja",), "en": ("orange",), "pt": ("laranja",)}),
    ("yellow", "Amarillo", (0.95, 0.85, 0.15), {"es": ("amarillo",), "en": ("yellow",), "pt": ("amarelo",)}),
    ("green", "Verde", (0.15, 0.65, 0.20), {"es": ("verde",), "en": ("green",), "pt": ("verde",)}),
    ("cyan", "Celeste", (0.35, 0.75, 0.95), {"es": ("celeste",), "en": ("light blue", "cyan"), "pt": ("azul claro",)}),
    ("blue", "Azul", (0.15, 0.30, 0.80), {"es": ("azul",), "en": ("blue",), "pt": ("azul",)}),
    ("violet", "Violeta", (0.50, 0.25, 0.70), {"es": ("violeta",), "en": ("purple", "violet"), "pt": ("violeta", "roxo")}),
    ("pink", "Rosa", (0.95, 0.55, 0.70), {"es": ("rosa",), "en": ("pink",), "pt": ("rosa",)}),
    ("brown", "Marrón", (0.45, 0.28, 0.14), {"es": ("marron",), "en": ("brown",), "pt": ("marrom",)}),
    ("black", "Negro", (0.05, 0.05, 0.05), {"es": ("negro",), "en": ("black",), "pt": ("preto",)}),
    ("white", "Blanco", (0.95, 0.95, 0.95), {"es": ("blanco",), "en": ("white",), "pt": ("branco",)}),
    ("gray", "Gris", (0.55, 0.55, 0.55), {"es": ("gris",), "en": ("gray", "grey"), "pt": ("cinza",)}),
)

# (nombre en la biblioteca de FreeCAD, etiqueta, palabras por idioma). Se ofrecen solo los
# que la instalación tenga.
_MATERIALS = (
    ("Aluminum-Generic", "Aluminio", {"es": ("aluminio",), "en": ("aluminum",), "pt": ("aluminio",)}),
    ("Steel-Generic", "Acero", {"es": ("acero",), "en": ("steel",), "pt": ("aco",)}),
    ("Steel-X5CrNi18-10", "Acero inoxidable", {"es": ("inoxidable", "acero inoxidable"), "en": ("stainless", "stainless steel"), "pt": ("inox", "aco inox")}),
    ("Iron-Generic", "Hierro", {"es": ("hierro",), "en": ("iron",), "pt": ("ferro",)}),
    ("Copper-Generic", "Cobre", {"es": ("cobre",), "en": ("copper",), "pt": ("cobre",)}),
    ("Brass", "Latón", {"es": ("laton",), "en": ("brass",), "pt": ("latao",)}),
    ("Bronze", "Bronce", {"es": ("bronce",), "en": ("bronze",), "pt": ("bronze",)}),
    ("titanium", "Titanio", {"es": ("titanio",), "en": ("titanium",), "pt": ("titanio",)}),
    ("Gold", "Oro", {"es": ("oro",), "en": ("gold",), "pt": ("ouro",)}),
    ("Silver", "Plata", {"es": ("plata",), "en": ("silver",), "pt": ("prata",)}),
    ("PLA-Generic", "PLA (impresión 3D)", {"es": ("pla",), "en": ("pla",), "pt": ("pla",)}),
    ("ABS-Generic", "ABS", {"es": ("abs",), "en": ("abs",), "pt": ("abs",)}),
    ("Plastic", "Plástico", {"es": ("plastico",), "en": ("plastic",), "pt": ("plastico",)}),
    ("Acrylic-Glass-Generic", "Acrílico", {"es": ("acrilico",), "en": ("acrylic",), "pt": ("acrilico",)}),
    ("Glass-Generic", "Vidrio", {"es": ("vidrio",), "en": ("glass",), "pt": ("vidro",)}),
    ("Wood-Generic", "Madera", {"es": ("madera",), "en": ("wood",), "pt": ("madeira",)}),
)


def _prompts():
    try:
        from Workbench import _prompts as prompts
    except ImportError:
        from dic.Workbench import _prompts as prompts
    return prompts


def _options(table, available=None):
    """Turn ``(key, label, ..., {language: words})`` rows into ChoiceInputPrompt options."""
    prompts = _prompts()
    prompts._ensure_input_prompts_on_path()
    from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

    language = PlaneGrammarSwitcher.CurrentLanguage()
    return [
        (row[0], row[1], row[-1].get(language, row[-1]["es"]))
        for row in table
        if available is None or row[0] in available
    ]


def _targets(title: str) -> list:
    """Return the objects to change: the selected ones, else one chosen by list or spelling."""
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return []
    selected = []
    if Gui is not None:
        selected = [obj for obj in Gui.Selection.getSelection(doc.Name) if hasattr(obj, "Shape")]
    if selected:
        return selected
    prompts = _prompts()
    obj = prompts.askObject(
        doc,
        title,
        "Elegí el objeto",
        prompts.isShape,
        "[DAV] Error: no hay ningún objeto para cambiar. Creá algo primero.",
    )
    return [obj] if obj is not None else []


def _withTip(obj) -> list:
    """The object and, for a body, its last operation: that is what gets drawn."""
    items = [obj]
    tip = getattr(obj, "Tip", None) if obj.isDerivedFrom("PartDesign::Body") else None
    if tip is not None:
        items.append(tip)
    return items


def _paint(obj, rgb) -> None:
    for item in _withTip(obj):
        view = getattr(item, "ViewObject", None)
        if view is None or not hasattr(view, "ShapeColor"):
            continue
        view.ShapeColor = rgb
        try:
            view.DiffuseColor = [rgb + (0.0,)]  # sin colores por cara que tapen el del objeto
        except Exception:
            pass


def paintObject(Key: str | None = None) -> None:
    """Change the colour of the selected objects, picking it by voice.

    Args:
        Key: Colour key of ``_COLORS`` already said ("pintar rojo"); None asks for it.

    Example::

        paintObject()
    """
    title = "Color del objeto"
    # primero se elige el color; el objeto se pregunta después, solo si no hay selección
    key = Key or _prompts().askChoice(title, "Elegí el color (arriba/abajo, okey)", _options(_COLORS))
    if key is None:
        print(f"[DAV] {title} cancelado.")
        return
    objects = _targets(title)
    if not objects:
        return
    name, rgb = next((row[1], row[2]) for row in _COLORS if row[0] == key)
    for obj in objects:
        _paint(obj, rgb)
    App.activeDocument().recompute()
    print(f"[DAV] {name}: {', '.join(obj.Label for obj in objects)}.")


def _libraryMaterials() -> dict:
    """Name -> material of the FreeCAD library; empty when the Materials module is missing."""
    try:
        import Materials

        return {material.Name: material for material in Materials.MaterialManager().Materials.values()}
    except Exception:
        return {}


def setMaterial(Key: str | None = None) -> None:
    """Change the material of the selected objects, picking it by voice.

    Args:
        Key: Library name of the material already said ("poner material acero"); None asks.

    El material de la biblioteca de FreeCAD trae también su aspecto: el objeto cambia de color
    y queda con la densidad del material.

    Example::

        setMaterial()
    """
    title = "Material del objeto"
    library = _libraryMaterials()
    options = _options(_MATERIALS, available=library)
    if not options:
        print("[DAV] Error: esta instalación de FreeCAD no tiene biblioteca de materiales.")
        return
    if Key is not None and Key not in library:
        print(f"[DAV] Error: este FreeCAD no tiene el material '{Key}'.")
        return
    # primero se elige el material; el objeto se pregunta después, solo si no hay selección
    key = Key or _prompts().askChoice(title, "Elegí el material (arriba/abajo, okey)", options)
    if key is None:
        print(f"[DAV] {title} cancelado.")
        return
    objects = _targets(title)
    if not objects:
        return
    label = next(row[1] for row in _MATERIALS if row[0] == key)
    changed = []
    for obj in objects:
        for item in _withTip(obj):
            if "ShapeMaterial" in item.PropertiesList:
                item.ShapeMaterial = library[key]
                changed.append(item)
    if not changed:
        print("[DAV] Error: los objetos elegidos no admiten material.")
        return
    App.activeDocument().recompute()
    print(f"[DAV] Material {label}: {', '.join(obj.Label for obj in objects)}.")


# Verbos de las frases de una sola vez, por idioma: «pintar rojo», «poner material acero».
_PAINT_VERBS = {
    "es": ("pintar", "colorear", "pintar de", "poner color"),
    "en": ("paint", "color", "set color"),
    "pt": ("pintar", "colorir", "pintar de", "definir cor"),
}
_MATERIAL_VERBS = {
    "es": ("poner material", "usar material", "material"),
    "en": ("set material", "use material", "material"),
    "pt": ("definir material", "usar material", "material"),
}


def oneShotPhrases(Language: str) -> dict:
    """Return the phrases that name the colour or material in the same sentence.

    Evitan el segundo cuadro (y el cambio de gramática) cuando el reconocedor ya oyó
    todo: «pintar rojo» pinta, «poner material acero» asigna el material.

    Args:
        Language: "es", "en" or "pt".

    Returns:
        ``{spoken phrase: function without arguments}``, ready for ``TraduceToXx.update``.

    Example::

        TraduceToEs.update(oneShotPhrases("es"))
    """
    language = Language if Language in _PAINT_VERBS else "es"
    phrases = {}
    for row in _COLORS:
        for word in row[-1].get(language, row[-1]["es"]):
            for verb in _PAINT_VERBS[language]:
                phrases[f"{verb} {word}"] = lambda key=row[0]: paintObject(key)
    for row in _MATERIALS:
        for word in row[-1].get(language, row[-1]["es"]):
            for verb in _MATERIAL_VERBS[language]:
                phrases[f"{verb} {word}"] = lambda key=row[0]: setMaterial(key)
    return phrases
