"""Lee el árbol real de diccionarios de DAV (grupos, comandos, frases e íconos).

Los diccionarios importan FreeCAD y Qt al cargarse, así que acá se reemplazan
por módulos simulados: solo interesa la estructura, no ejecutar nada.

Uso:
    from arbol import cargar_arbol
    raiz = cargar_arbol()
    # raiz["children"] -> [{"key", "kind": "group"|"cmd", "phrases": {"es": [...], ...},
    #                       "icon": ruta|None, "children": [...]}]
"""

import importlib
import importlib.abc
import importlib.machinery
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

DAV = Path(__file__).resolve().parents[2]          # .../Dav
DIC = DAV / "dic"
SCR = DAV / "scr"
GUI = SCR / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad"

_STUBS = (
    "FreeCAD", "FreeCADGui", "Part", "Sketcher", "Draft", "TechDraw", "PartDesign", "Mesh",
    "Assembly", "PySide", "PySide2", "PySide6", "shiboken6", "pivy", "draftutils",
    "draftguitools", "DraftVecUtils", "Arch", "BOPTools", "vosk", "sounddevice", "numpy",
    "DraftGui", "SketcherGui", "PartGui", "TechDrawGui", "AssemblyApp", "JointObject",
    "pydantic", "Import", "ImportGui", "Units", "WorkingPlane", "draftobjects", "draftmake",
    "BasicShapes", "Materials", "MaterialEditor", "TechDrawTools", "PartDesignGui",
    "MeshPart", "Path",
)

_LANGS = {"es": ("TraduceToEs",), "en": ("TraduceToEn",), "pt": ("TraduceToPt", "TraduceToPT")}
_ALIAS_CARPETA = {"draft": "DraftWork", "stdview": "StdView", "structure": "StructureToolbar",
                  "array": "circular_array", "tools": "BSpline_Tools"}


class _Simulado(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] in _STUBS:
            return importlib.machinery.ModuleSpec(name, self, is_package=True)
        return None

    def create_module(self, spec):
        modulo = MagicMock(name=spec.name)
        modulo.__path__ = []
        modulo.__spec__ = spec
        modulo.__name__ = spec.name
        return modulo

    def exec_module(self, modulo):
        pass


def _normaliza(nombre: str) -> str:
    return "".join(c for c in nombre.lower() if c.isalnum())


def _indice_iconos() -> dict:
    """Mismo criterio que InterfazDAV/IconLocator: gana la primera raíz que define un nombre."""
    raices = [SCR / "ComponentesDAV" / "InterfazDAV" / "Icons", DIC]
    alias = {"pieza": "part", "circulo": "circle", "stdview": "standardviews", "vistaestandar": "standardviews"}
    indice = {}
    for raiz in raices:
        for carpeta, _, archivos in os.walk(raiz):
            for archivo in sorted(archivos):
                if archivo.lower().endswith(".svg"):
                    indice.setdefault(_normaliza(archivo[:-4]), os.path.join(carpeta, archivo))
    for a, destino in alias.items():
        if a not in indice and destino in indice:
            indice[a] = indice[destino]
    return indice


def _buscar_carpeta(padre, clave):
    if not padre or not os.path.isdir(padre):
        return None
    nombres = [n for n in os.listdir(padre) if os.path.isdir(os.path.join(padre, n))]
    quiero = _ALIAS_CARPETA.get(clave, clave)
    for n in nombres:
        if n.lower() == quiero.lower():
            return os.path.join(padre, n)
    c = _normaliza(clave)
    for n in nombres:
        nn = _normaliza(n)
        if nn in ("part" + c, c + "s") or (len(c) > 4 and (nn.startswith(c) or c.startswith(nn))):
            return os.path.join(padre, n)
    return None


def _traducciones(carpeta, idioma):
    if not carpeta:
        return {}
    rel = os.path.relpath(carpeta, DIC).replace(os.sep, ".")
    existentes = os.listdir(carpeta)
    for stem in _LANGS[idioma]:
        if stem + ".py" in existentes:
            try:
                modulo = importlib.import_module((rel + "." if rel != "." else "") + stem)
            except Exception as error:  # diccionario roto: se informa y se sigue
                print(f"[arbol] {rel}/{stem}: {error.__class__.__name__}: {error}", file=sys.stderr)
                continue
            tabla = getattr(modulo, stem, None)
            if isinstance(tabla, dict):
                return tabla
    return {}


def _recorrer(nodo, carpeta, clave, iconos, traducciones_raiz=None):
    tablas = {l: (traducciones_raiz[l] if traducciones_raiz else _traducciones(carpeta, l)) for l in _LANGS}
    salida = {"key": clave, "kind": "group", "children": [], "folder": os.path.relpath(carpeta, DIC) if carpeta else None}
    vistos = {}
    for k, v in nodo.items():
        if k == "help":
            continue
        vistos.setdefault(id(v), []).append((k, v))

    def frases(v, l):
        return [p for p, t in tablas[l].items() if t is v]

    for items in vistos.values():
        mejor = max(items, key=lambda kv: sum(len(frases(kv[1], l)) for l in _LANGS))
        k, v = mejor
        ph = {l: frases(v, l) for l in _LANGS}
        alias = [a for a, _ in items if a != k]
        if isinstance(v, dict):
            hijo = _recorrer(v, _buscar_carpeta(carpeta, k) if carpeta else None, k, iconos)
        else:
            hijo = {"key": k, "kind": "cmd", "children": []}
        hijo["phrases"], hijo["aliases"] = ph, alias
        hijo["icon"] = iconos.get(_normaliza(k)) or next((iconos.get(_normaliza(a)) for a in alias if iconos.get(_normaliza(a))), None)
        salida["children"].append(hijo)
    return salida


def cargar_arbol() -> dict:
    """Devuelve el árbol completo (Base) como dicts anidados."""
    sys.meta_path.insert(0, _Simulado())
    sys.path[:0] = [str(DAV), str(DIC), str(GUI), str(GUI / "navigation"), str(SCR),
                    str(SCR / "selection"), str(SCR / "ComponentesDAV")]
    import base  # noqa: E402  (necesita los paths y los módulos simulados)

    iconos = _indice_iconos()
    raiz_tr = {l: _traducciones(DIC, l) for l in _LANGS}
    raiz = _recorrer(base.Base, DIC, "base", iconos, traducciones_raiz=raiz_tr)
    raiz["global"] = _globales(raiz_tr, iconos)
    raiz["nav"] = _navegacion()
    raiz["iconos"] = iconos
    return raiz


def _globales(raiz_tr, iconos) -> list:
    """Comandos del diccionario raíz que se dicen desde cualquier contexto."""
    base = sys.modules["base"].Base
    destinos_base = {id(v) for v in base.values()}
    por_destino = {}
    for l in _LANGS:
        for frase, destino in raiz_tr[l].items():
            if id(destino) in destinos_base or isinstance(destino, dict):
                continue
            por_destino.setdefault(id(destino), {"obj": destino, "ph": {x: [] for x in _LANGS}})["ph"][l].append(frase)
    salida = []
    for info in por_destino.values():
        obj = info["obj"]
        salida.append({"key": getattr(obj, "__name__", "?"), "kind": "cmd", "phrases": info["ph"],
                       "module": getattr(obj, "__module__", ""), "icon": None, "children": []})
    return salida


def _navegacion() -> list:
    """Palabras de navegación (subir, contexto, enviar, cancelar), iguales en cualquier nivel."""
    acciones = importlib.import_module("NavCommands.NavActions").NavActions
    salida = []
    for clave in ("up", "show_context", "send", "cancel"):
        ph = {}
        for l in _LANGS:
            tabla = _traducciones(DIC / "NavCommands", l)
            ph[l] = [p for p, t in tabla.items() if t is acciones[clave]]
        salida.append({"key": clave, "kind": "cmd", "phrases": ph, "icon": None, "children": []})
    return salida


if __name__ == "__main__":
    import json
    arbol = cargar_arbol()
    print(json.dumps({"hijos": [c["key"] for c in arbol["children"]], "globales": len(arbol["global"]), "nav": [n["phrases"]["es"][:3] for n in arbol["nav"]]}))
