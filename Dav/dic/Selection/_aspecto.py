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
solos, desde cualquier contexto: primero se elige el color o material de la lista y después
siempre se pregunta el objeto (``avanzar`` o ``buscar por deletreo``); la selección actual
nunca se usa.
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
    """Return the object to change, always chosen by list or spelling.

    Nunca se toma lo que esté seleccionado: siempre se pregunta cuál objeto
    (``avanzar`` / ``buscar por deletreo`` / ``okey``).
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return []
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


def _setAppearance(view, rgb, material=None) -> bool:
    """Give a view object one uniform colour (and, optionally, a library material's look).

    FreeCAD 1.x guarda el aspecto en ``ShapeAppearance`` (una lista de ``App.Material``);
    ``ShapeColor`` ya no existe en la vista, así que preguntar por ella no pinta nada.
    Se deja un solo material para que no queden colores por cara tapando el nuevo.

    Args:
        view: The object's ``ViewObject``.
        rgb: Colour as ``(r, g, b)`` in 0-1.
        material: Optional library material whose shininess and transparency are copied.

    Returns:
        True when the view took the new look.
    """
    if "ShapeAppearance" in view.PropertiesList:
        current = list(view.ShapeAppearance)
        look = App.Material()
        if current:  # App.Material no se copia a sí mismo: se pasan los campos
            for name in ("AmbientColor", "SpecularColor", "EmissiveColor", "Shininess", "Transparency"):
                try:
                    setattr(look, name, getattr(current[0], name))
                except (AttributeError, TypeError):
                    pass
        alpha = current[0].DiffuseColor[3] if current and len(current[0].DiffuseColor) > 3 else 1.0
        look.DiffuseColor = tuple(rgb) + (alpha,)
        if material is not None:
            props = getattr(material, "AppearanceProperties", {}) or {}
            for name in ("Shininess", "Transparency"):
                try:
                    setattr(look, name, float(props[name]))
                except (KeyError, ValueError, TypeError, AttributeError):
                    pass
        view.ShapeAppearance = (look,)
        return True
    if "ShapeColor" in view.PropertiesList:  # FreeCAD anterior a 1.0
        view.ShapeColor = rgb
        return True
    return False


def _faceOwner(obj):
    """Find the solid and face an auxiliary surface was copied from.

    DAV crea un objeto ``Superficie N`` por cada cara de una pieza: es una copia de esa cara,
    en el mismo lugar. Se busca en las piezas del documento la cara con la misma área, el
    mismo centro y el mismo tipo de superficie.

    Args:
        obj: A candidate auxiliary surface (an object whose shape is one single face).

    Returns:
        ``(owner, face index)`` or None when ``obj`` is not a copy of a face.
    """
    shape = getattr(obj, "Shape", None)
    if shape is None or shape.isNull() or shape.Solids or len(shape.Faces) != 1:
        return None
    face = shape.Faces[0]
    for candidate in obj.Document.Objects:
        if candidate is obj:
            continue
        owner_shape = getattr(candidate, "Shape", None)
        if owner_shape is None or owner_shape.isNull() or not owner_shape.Solids:
            continue
        try:
            if candidate.getParentGeoFeatureGroup() is not None:
                continue  # lo que vive dentro de un cuerpo viaja con su cuerpo
        except Exception:
            pass
        for index, other in enumerate(owner_shape.Faces):
            if (
                type(other.Surface) is type(face.Surface)
                and abs(other.Area - face.Area) < 1e-6
                and other.CenterOfMass.distanceToPoint(face.CenterOfMass) < 1e-6
            ):
                return candidate, index
    return None


def _paintFace(owner, index: int, rgb) -> int:
    """Colour only face ``index`` of a solid (and of a body's last operation).

    Returns:
        How many views took the colour.
    """
    done = 0
    for item in _withTip(owner):
        view = getattr(item, "ViewObject", None)
        shape = getattr(item, "Shape", None)
        if view is None or shape is None or "ShapeAppearance" not in view.PropertiesList:
            continue
        count = len(shape.Faces)
        if not 0 <= index < count:
            continue
        current = list(view.ShapeAppearance)
        if not current:
            current = [App.Material()]
        looks = []
        for position in range(count):
            source = current[position] if len(current) == count else current[0]
            look = App.Material()
            for name in ("DiffuseColor", "AmbientColor", "SpecularColor", "EmissiveColor", "Shininess", "Transparency"):
                try:
                    setattr(look, name, getattr(source, name))
                except (AttributeError, TypeError):
                    pass
            looks.append(look)
        alpha = looks[index].DiffuseColor[3] if len(looks[index].DiffuseColor) > 3 else 1.0
        looks[index].DiffuseColor = tuple(rgb) + (alpha,)
        try:
            view.ShapeAppearance = tuple(looks)
            done += 1
        except Exception as error:
            print(f"[DAV] No se pudo pintar la cara de '{item.Label}': {error}")
    return done


def _paint(obj, rgb, material=None) -> int:
    """Colour obj (and a body's last operation); return how many views took the colour.

    Si ``obj`` es una superficie auxiliar (copia de una cara), esa cara también se pinta
    en la pieza de la que salió.
    """
    done = 0
    for item in _withTip(obj):
        view = getattr(item, "ViewObject", None)
        if view is None:
            continue
        try:
            done += bool(_setAppearance(view, rgb, material))
        except Exception as error:
            print(f"[DAV] No se pudo pintar '{item.Label}': {error}")
    if material is None:
        try:
            found = _faceOwner(obj)
        except Exception as error:
            print(f"[DAV] No se pudo buscar la cara de '{obj.Label}': {error}")
            found = None
        if found is not None:
            done += _paintFace(found[0], found[1], rgb)
    return done


def _materialColor(material):
    """Return the ``(r, g, b)`` of a library material, or None when it has none."""
    props = getattr(material, "AppearanceProperties", {}) or {}
    text = props.get("DiffuseColor") or ""
    try:
        values = [float(part) for part in str(text).strip("() ").split(",")]
    except ValueError:
        return None
    return tuple(values[:3]) if len(values) >= 3 else None


def paintObject(Key: str | None = None) -> None:
    """Change the colour of the selected objects, picking it by voice.

    Args:
        Key: Colour key of ``_COLORS`` already said ("pintar rojo"); None asks for it.

    Example::

        paintObject()
    """
    title = "Color del objeto"
    # primero se elige el color; después siempre se pregunta el objeto
    key = Key or _prompts().askChoice(title, "Elegí el color (arriba/abajo, okey)", _options(_COLORS))
    if key is None:
        print(f"[DAV] {title} cancelado.")
        return
    objects = _targets(title)
    if not objects:
        return
    name, rgb = next((row[1], row[2]) for row in _COLORS if row[0] == key)
    painted = sum(_paint(obj, rgb) for obj in objects)
    App.activeDocument().recompute()
    if not painted:
        print("[DAV] Error: no se pudo cambiar el color (¿hay ventana 3D?).")
        return
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
    # primero se elige el material; después siempre se pregunta el objeto
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
        # FreeCAD no repinta si ya se había cambiado el color a mano: se fija el aspecto
        color = _materialColor(library[key])
        if color is not None:
            _paint(obj, color, library[key])
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
