"""Genera los manuales de usuario de DAV (PDF) en español, inglés y portugués.

Todo lo que se puede leer de los diccionarios sale de ellos (grupos, comandos, frases
en cada idioma, íconos), así que el manual no se desactualiza cuando se agrega una
función: alcanza con volver a generarlo y completar su descripción en ``desc_*.py``.

Uso (desde cualquier carpeta):
    python Dav/docs/manual/build_manual.py            # los tres idiomas
    python Dav/docs/manual/build_manual.py es         # solo español
    python Dav/docs/manual/build_manual.py --salida C:/tmp   # otra carpeta de salida

Requiere PyMuPDF (``pip install pymupdf``). Escribe Manual_Usuario.pdf, User_Manual.pdf y
Manual_do_Usuario.pdf en la raíz del repositorio.
"""

import argparse
import ast
import html
import sys
import tempfile
from pathlib import Path

import pymupdf

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import desc_assembly_draft_part  # noqa: E402
import desc_explorer  # noqa: E402
import desc_partdesign_sketcher  # noqa: E402
import desc_techdraw  # noqa: E402
from arbol import DIC, cargar_arbol  # noqa: E402
from textos import ARCHIVO, IDIOMAS, REQ, SECCIONES, T  # noqa: E402

RAIZ_REPO = AQUI.parents[2]
MODULOS = (desc_explorer, desc_assembly_draft_part, desc_partdesign_sketcher, desc_techdraw)
DESC, REQ_GRUPO = {}, {}
for _m in MODULOS:
    DESC.update(_m.D)
    REQ_GRUPO.update(_m.G)

IDX = {"es": 0, "en": 1, "pt": 2}
AZUL, AZUL_CLARO, GRIS = "#1e3a8a", "#e8eefc", "#64748b"
CSS = f"""
body {{ font-family: sans-serif; font-size: 9.5pt; color: #1f2937; line-height: 1.25; }}
h1 {{ color: {AZUL}; font-size: 17pt; margin-top: 4pt; margin-bottom: 2pt; page-break-before: always; }}
h1.cont {{ page-break-before: avoid; margin-top: 16pt; }}
h2 {{ color: {AZUL}; font-size: 12.5pt; margin-top: 12pt; margin-bottom: 3pt; }}
p {{ margin-top: 3pt; margin-bottom: 3pt; }}
p.sub {{ color: {GRIS}; font-style: italic; margin-top: 0; }}
p.small {{ font-size: 8.5pt; color: {GRIS}; }}
li {{ margin-bottom: 2pt; }}
table.cmd {{ width: 100%; border-collapse: collapse; margin-top: 4pt; }}
table.hdr {{ width: 100%; border-collapse: collapse; margin-top: 4pt; }}
table.hdr td {{ font-size: 8.5pt; padding: 0; height: 16pt; }}
table.cmd {{ margin-top: 0; }}
table.cmd td.z {{ padding: 0; border: none; font-size: 1pt; }}
table.cmd td {{ border-bottom: 0.5pt solid #cbd5e1; padding: 3pt 4pt; font-size: 8.5pt; vertical-align: middle; }}
tr.g td {{ padding-top: 5pt; padding-bottom: 5pt; }}
td.name {{ font-weight: bold; }}
span.k {{ font-weight: normal; color: {GRIS}; font-size: 7pt; }}
span.syn {{ font-weight: normal; color: #475569; }}
table.ex {{ width: 100%; border-collapse: collapse; }}
table.ex td {{ border-bottom: 0.5pt solid #cbd5e1; padding: 3pt 4pt; font-size: 9pt; vertical-align: top; }}
table.ex td.l {{ font-weight: bold; color: {AZUL}; }}
table.toc {{ width: 100%; border-collapse: collapse; }}
table.toc td {{ padding: 2pt 0; font-size: 10pt; }}
table.toc td.n {{ text-align: right; width: 12%; }}
td.t1 {{ font-weight: bold; padding-top: 6pt; }}
td.t2 {{ padding-left: 14pt; }}
.center {{ text-align: center; }}
.titulo {{ font-size: 28pt; color: {AZUL}; font-weight: bold; text-align: center; margin-top: 8pt; }}
.subtitulo {{ font-size: 15pt; color: {GRIS}; text-align: center; margin-bottom: 18pt; }}
"""


def esc(texto: str) -> str:
    return html.escape(texto, quote=False)


# Enlaces de los agradecimientos (los mismos que figuran en los README).
ENLACES = {
    "Universidad Autónoma de Entre Ríos (UADER)": "https://uader.edu.ar/",
    "Universidade Autônoma de Entre Ríos (UADER)": "https://uader.edu.ar/",
    "Autonomous University of Entre Ríos (UADER)": "https://uader.edu.ar/",
    "Naitria Peralta Montoya": "https://www.instagram.com/naitria?stkn=OWkwZnZuOXN6Y2h4",
    "Bruno Contigiani": "https://www.instagram.com/brunocontigiani_?stkn=OG1odzAybWI5OTVw",
}


# ------------------------------------------------------------------ íconos
class Iconos:
    """Convierte los SVG en PNG (una vez) para que el HTML los pueda incrustar."""

    def __init__(self, carpeta: Path):
        self.carpeta = carpeta
        self.hechos = {}

    def archivo(self, svg) -> str | None:
        if not svg:
            return None
        if svg in self.hechos:
            return self.hechos[svg]
        destino = f"i{len(self.hechos)}.png"
        try:
            pagina = pymupdf.open(svg)[0]
            escala = 64 / max(pagina.rect.width, pagina.rect.height)
            pagina.get_pixmap(matrix=pymupdf.Matrix(escala, escala), alpha=True).save(str(self.carpeta / destino))
        except Exception as error:
            print(f"  [icono] {svg}: {error}", file=sys.stderr)
            destino = None
        self.hechos[svg] = destino
        return destino

    def img(self, svg, px: int = 22) -> str:
        nombre = self.archivo(svg)
        return f'<img src="{nombre}" width="{px}" height="{px}">' if nombre else ""


# ------------------------------------------------------------- utilidades
def frases(nodo: dict, idioma: str, tope: int = 4) -> tuple[list, bool]:
    """Frases del nodo en ``idioma``; si no hay, las del español (y se avisa con False)."""
    for lang, propio in ((idioma, True), ("es", False)):
        vistas, salida = set(), []
        for frase in nodo.get("phrases", {}).get(lang, []):
            clave = frase.lower().replace("_", " ")
            if clave not in vistas:
                vistas.add(clave)
                salida.append(frase.replace("_", " "))
        if salida:
            return salida[:tope], propio
    return [], True


def tiene_voz(nodo: dict) -> bool:
    if nodo["kind"] == "cmd":
        return any(nodo.get("phrases", {}).values())
    return any(nodo.get("phrases", {}).values()) or any(tiene_voz(h) for h in nodo["children"])


def requisito(ruta: str, idioma: str) -> str:
    entrada = DESC.get(ruta)
    codigo = entrada[3] if entrada and len(entrada) > 3 else None
    if codigo is None:
        partes = ruta.split("/")
        while partes and codigo is None:
            codigo = REQ_GRUPO.get("/".join(partes))
            partes.pop()
    return REQ[codigo or "none"][IDX[idioma]]


def descripcion(ruta: str, idioma: str, faltan: list) -> str:
    entrada = DESC.get(ruta)
    if entrada is None:
        faltan.append(ruta)
        return "—"
    return entrada[IDX[idioma]]


ARBOL = None
FALTAN, USADAS = [], set()


def icono_de(nodo: dict):
    """Ícono del nodo; un grupo sin SVG propio usa el de su primer comando con ícono."""
    if nodo.get("icon"):
        return nodo["icon"]
    for hijo in nodo.get("children", []):
        encontrado = icono_de(hijo)
        if encontrado:
            return encontrado
    return None


def celda_nombre(nodo: dict, idioma: str, grupo: bool = False, nombre_fijo: str | None = None) -> str:
    lista, propio = frases(nodo, idioma)
    if nombre_fijo:
        principal, resto = nombre_fijo, lista
    elif lista:
        principal, resto = lista[0], lista[1:]
    else:
        principal, resto = nodo["key"], []
    aviso = "" if propio else " <span class='k'>(es)</span>"
    sinonimos = f"<br><span class='syn'>{esc(' , '.join(resto))}</span>" if resto else ""
    clave = f"<br><span class='k'>{esc(nodo['key'])}</span>"
    return f"<b>{esc(principal)}</b>{aviso}{sinonimos}{clave}"


def fila(nodo, ruta, idioma, iconos, profundidad, nombre_fijo=None, frases_de=None):
    t = T[idioma]
    rid = nuevo_id()
    if nodo["kind"] == "group":
        GRUPOS[rid] = profundidad
    USADAS.add(ruta)
    es_grupo = nodo["kind"] == "group"
    descr = descripcion(ruta, idioma, FALTAN)
    req = requisito(ruta, idioma)
    base = frases_de or nodo
    tam = 24 if es_grupo else 20
    icono = icono_de(nodo) or icono_de(nodo_por_ruta(ICONO_PARIENTE[ruta])) if ruta in ICONO_PARIENTE else icono_de(nodo)
    sangria = 4 + 11 * profundidad
    if es_grupo:
        lista, _ = frases(base, idioma, tope=4)
        entra = f"<br><span class='k'>{esc(t['group_hint'])} <b>{esc(' , '.join(lista[:3]))}</b></span>" if lista else ""
        nombre = celda_nombre(base, idioma, nombre_fijo=nombre_fijo).split("<br>")[0] + entra
        clase = "g" if profundidad == 0 else "g g2"
        return (rid, f"<tr id='{rid}' class='{clase}'><td width='9%' style='padding-left:{sangria}pt'>{iconos.img(icono, tam)}</td>"
                f"<td width='31%' class='name'>{nombre}</td><td width='38%'><b>{esc(descr)}</b></td><td width='22%'>{esc(req)}</td></tr>")
    return (rid, f"<tr id='{rid}'><td width='9%' style='padding-left:{sangria}pt'>{iconos.img(icono, tam)}</td>"
            f"<td width='31%' class='name'>{celda_nombre(base, idioma, nombre_fijo=nombre_fijo)}</td>"
            f"<td width='38%'>{esc(descr)}</td><td width='22%'>{esc(req)}</td></tr>")


# Íconos de los comandos globales que reutilizan el de su equivalente en un submenú
ICONO_GLOBAL = {"undo": "undo", "redo": "redo", "deleteLast": "delete", "deleteObject": "delete",
                "deleteBroken": "delete", "CreateDimension": "measure"}
# Comandos sin SVG propio que reutilizan el de su variante (ruta -> ruta del comando cuyo ícono se usa)
_A = "workbench/assembly/"
_P = "workbench/partdesign/"
_S = "workbench/sketcher/geometry/"
ICONO_PARIENTE = {
    "explorer/proyecto/print3d": "explorer/proyecto/export",
    "explorer/print/pdf": "explorer/print/print",
    "explorer/structure/linkactions/importalllinks": "explorer/structure/linkactions/importlink",
    "stdview/appearance/facecolor": "stdview/appearance/facecolors",
    _A + "fixed_joint": _A + "joint/fixed", _A + "revolute_joint": _A + "joint/revolute",
    _A + "slider_joint": _A + "joint/slider", _A + "distance_joint": _A + "joint/distance",
    _A + "angle_joint": _A + "joint/angle", _A + "ball_joint": _A + "joint/ball",
    _A + "cylindrical_joint": _A + "joint/cylindrical", _A + "parallel_joint": _A + "joint/parallel",
    _A + "perpendicular_joint": _A + "joint/perpendicular", _A + "gears_joint": _A + "joint/gears",
    _A + "belt_joint": _A + "joint/belt", _A + "screw_joint": _A + "joint/screw",
    _A + "rack_pinion_joint": _A + "joint/rackpinion", _A + "ground_part": _A + "grounded",
    _P + "additive/pad_sketch": _P + "additive/pad", _P + "additive/pad_by_length": _P + "additive/pad",
    _P + "additive/revolve_by_angle": _P + "additive/revolution", _P + "additive/loft_profiles": _P + "additive/additiveloft",
    _P + "subtractive/pocket_by_length": _P + "subtractive/pocket", _P + "subtractive/hole_by_size": _P + "subtractive/hole",
    _P + "subtractive/blind_hole": _P + "subtractive/hole", _P + "subtractive/groove_by_angle": _P + "subtractive/groove",
    _P + "modify/fillet_by_radius": _P + "modify/fillet", _P + "modify/chamfer_by_size": _P + "modify/chamfer",
    _P + "modify/chamfer_by_size_and_angle": _P + "modify/chamfer", _P + "modify/thickness_by_value": _P + "modify/thickness",
    _P + "transform/linear_pattern_by_spacing": _P + "transform/linearpattern", _P + "transform/scaled_by_factor": _P + "transform/scaled",
    _S + "arc/create_by_center": _S + "arc/center", _S + "arc/create_by_3points": _S + "arc/3point",
    _S + "circle/create_by_center_radius": _S + "circle/create", _S + "circle/create_by_3points": _S + "circle/3point",
    _S + "line/create_by_points": _S + "line/create", "workbench/sketcher/point/create_by_coords": "workbench/sketcher/point/create",
    "workbench/techdraw/views/objectview": "workbench/techdraw/views/view",
    "workbench/techdraw/dimensions/extent/totals": "workbench/techdraw/dimensions/extent/extent",
    "workbench/techdraw/page/pdf": "workbench/techdraw/page/print",
}
MEDIR = None  # nodo global CreateDimension (frases de «medir»), para explorer/tools/measure


def filas(nodo, ruta_padre, idioma, iconos, prof) -> list:
    salida = []
    hijos = nodo["children"]
    if prof == 0:  # primero los comandos directos, después los grupos (submenús)
        propio = lambda h: h["kind"] == "group" and any(h.get("phrases", {}).values())
        hijos = [h for h in hijos if not propio(h)] + [h for h in hijos if propio(h)]
    for hijo in hijos:
        clave = hijo["key"]
        if clave.startswith("interactive") or clave == "help":
            continue
        ruta = f"{ruta_padre}/{clave}" if ruta_padre else clave
        if hijo["kind"] == "group":
            if not tiene_voz(hijo):
                continue
            if not any(hijo.get("phrases", {}).values()):  # sin frase propia: se aplana
                USADAS.add(ruta)
                salida += filas(hijo, ruta, idioma, iconos, prof)
                continue
            salida.append(fila(hijo, ruta, idioma, iconos, prof))
            salida += filas(hijo, ruta, idioma, iconos, prof + 1)
        else:
            fuente = None
            if ruta == "explorer/tools/measure" and not any(hijo["phrases"].values()):
                fuente = MEDIR
            if not any(hijo["phrases"].values()) and fuente is None:
                continue
            salida.append(fila(hijo, ruta, idioma, iconos, prof, frases_de=fuente))
    return salida


_CONTADOR = [0]
GRUPOS = {}  # id de fila de cada grupo -> profundidad, para pintarle el fondo
TABLAS = []  # ids de fila de cada tabla, en orden, para saber dónde cae cada salto de página


def nuevo_id(prefijo: str = "r") -> str:
    _CONTADOR[0] += 1
    return f"{prefijo}{_CONTADOR[0]}"


def tabla(filas_html: list, idioma: str) -> str:
    """Tabla de comandos con la cabecera en una tabla aparte y una primera fila invisible.

    El maquetador repite mal la primera fila de una tabla que cruza páginas (queda una barra
    suelta), así que no se le deja repetir nada: en las páginas que continúan una tabla la
    cabecera se dibuja después, en el margen superior (ver ``pie_y_marcadores``).
    """
    t = T[idioma]
    hid = nuevo_id("h")
    # hueco con el alto de la cabecera; la franja azul con los títulos se dibuja después
    cabecera = f"<table class='hdr'><tr id='{hid}'><td width='100%'>&#160;</td></tr></table>"
    invisible = ("<tr><td class='z' width='9%'></td><td class='z' width='31%'></td>"
                 "<td class='z' width='38%'></td><td class='z' width='22%'></td></tr>")
    TABLAS.append([rid for rid, _ in filas_html if rid])
    return f"{cabecera}<table class='cmd'>{invisible}{''.join(h for _, h in filas_html)}</table>"


def nodo_por_ruta(ruta: str) -> dict:
    nodo = ARBOL
    for parte in ruta.split("/"):
        nodo = next(h for h in nodo["children"] if h["key"] == parte)
    return nodo


def titulos_ejemplos() -> list:
    """(clave, {es,en,pt}) de los ejemplos guiados, leídos de Explorer/Examples/_demos.py."""
    carpeta = DIC / "Explorer" / "Examples"
    arbol = ast.parse((carpeta / "_demos.py").read_text(encoding="utf-8"))
    claves = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "_EXAMPLES":
            claves = [(ast.literal_eval(e.elts[0]), e.elts[1].id.lstrip("_")) for e in n.value.elts]
    salida = []
    for clave, modulo in claves:
        fuente = ast.parse((carpeta / f"_{modulo}.py").read_text(encoding="utf-8"))
        for n in fuente.body:
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "TITLE":
                salida.append((clave, ast.literal_eval(n.value)))
    return salida


# -------------------------------------------------------------- documento
def documento(idioma: str, iconos: Iconos, numeros: dict | None) -> tuple[str, list]:
    """HTML completo y lista de encabezados (nivel, id, texto) para el índice."""
    t = T[idioma]
    toc = []
    cuerpo = []
    _CONTADOR[0] = 0
    TABLAS.clear()
    GRUPOS.clear()

    def h(nivel, id_, texto, clase=""):
        toc.append((nivel, id_, texto))
        etiqueta = f"h{nivel}"
        cuerpo.append(f"<{etiqueta} id='{id_}' class='{clase}'>{esc(texto)}</{etiqueta}>")

    # Portada
    logo = AQUI / "img" / "logo.png"
    cuerpo.append(f"<p class='center'><img src='{logo.name}' width='170'></p>")
    cuerpo.append(f"<div class='titulo'>{esc(t['title'])}</div><div class='subtitulo'>{esc(t['subtitle'])}</div>")
    cuerpo += [f"<p>{p}</p>" for p in t["lead"]]

    # Índice (se completa en la segunda pasada)
    cuerpo.append("@@TOC@@")

    # Introducción y navegación
    h(1, "intro", t["intro_h"])
    for titulo, texto in t["intro"]:
        cuerpo.append(f"<h2>{esc(titulo)}</h2>{texto}")
    h(2, "nav", t["nav_h"])
    cuerpo.append(f"<p>{t['nav_intro']}</p><ol>" + "".join(f"<li>{s}</li>" for s in t["nav_steps"]) + "</ol>")
    cuerpo.append(f"<h2>{esc(t['numbers_h'])}</h2><ul>" + "".join(f"<li>{s}</li>" for s in t["numbers"]) + "</ul>")

    # Comandos globales
    h(1, "global", t["global_h"])
    cuerpo.append(f"<p class='sub'>{esc(t['global_intro'])}</p><h2>{esc(t['nav_table_h'])}</h2>")
    filas_nav = []
    for n in ARBOL["nav"]:
        desc, req = t["nav_rows"][n["key"]]
        rid = nuevo_id()
        filas_nav.append((rid, f"<tr id='{rid}'><td width='9%'></td><td width='31%' class='name'>{celda_nombre(n, idioma, nombre_fijo=t['nav_names'][n['key']])}</td>"
                         f"<td width='38%'>{esc(desc)}</td><td width='22%'>{esc(req)}</td></tr>"))
    cuerpo.append(tabla(filas_nav, idioma))

    cuerpo.append(f"<h2>{esc(t['global_table_h'])}</h2>")
    filas_g = []
    for g in ARBOL["global"]:
        if g["module"].endswith("StandardViews") or g["key"] not in t["global_names"]:
            continue
        USADAS.add(f"global/{g['key']}")
        rid = nuevo_id()
        filas_g.append((rid, f"<tr id='{rid}'><td width='9%'>{iconos.img(ARBOL['iconos'].get(ICONO_GLOBAL.get(g['key'], '')))}</td><td width='31%' class='name'>{celda_nombre(g, idioma, nombre_fijo=t['global_names'][g['key']])}</td>"
                       f"<td width='38%'>{esc(descripcion('global/' + g['key'], idioma, FALTAN))}</td>"
                       f"<td width='22%'>{esc(requisito('global/' + g['key'], idioma))}</td></tr>"))
    for clave in ("preferences", "hide_dav_panel", "show_dav_panel"):
        nodo = next(c for c in ARBOL["children"] if c["key"] == clave)
        USADAS.add(clave)
        rid = nuevo_id()
        filas_g.append((rid, f"<tr id='{rid}'><td width='9%'>{iconos.img(nodo.get('icon'))}</td><td width='31%' class='name'>{celda_nombre(nodo, idioma, nombre_fijo=t['panel_names'][clave])}</td>"
                       f"<td width='38%'>{esc(descripcion(clave, idioma, FALTAN))}</td><td width='22%'>{esc(requisito(clave, idioma))}</td></tr>"))
    cuerpo.append(tabla(filas_g, idioma))
    cuerpo.append(f"<p>{t['global_views']}</p>")

    # Secciones de referencia
    global MEDIR
    MEDIR = next(g for g in ARBOL["global"] if g["key"] == "CreateDimension")
    for n, (ruta, titulos, intro) in enumerate(SECCIONES, start=1):
        nodo = nodo_por_ruta(ruta)
        USADAS.add(ruta)
        h(1, f"sec{n}", f"{n}. {titulos[IDX[idioma]]}")
        cuerpo.append(f"<p class='sub'>{esc(intro[IDX[idioma]])}</p>")
        cuerpo.append(tabla(filas(nodo, ruta, idioma, iconos, 0), idioma))

    # Ejemplos guiados
    h(1, "ejemplos", t["ex_h"])
    cuerpo.append(f"<p class='sub'>{esc(t['ex_sub'])}</p><p>{esc(t['ex_intro'])}</p>")
    cuerpo.append(f"<h2>{esc(t['ex_open_h'])}</h2><ol>" + "".join(f"<li>{s}</li>" for s in t["ex_open"]) + "</ol>")
    cuerpo.append(f"<h2>{esc(t['ex_list_h'])}</h2><table class='ex'><tr><td class='l' style='width:16%'><b>{esc(t['ex_col_ex'])}</b></td><td style='width:84%'><b>{esc(t['ex_col_what'])}</b></td></tr>")
    for clave, titulos in titulos_ejemplos():
        cuerpo.append(f"<tr><td class='l' style='width:16%'>{esc(titulos.get(idioma, titulos['es']))}</td><td style='width:84%'>{esc(t['ex_desc'].get(clave, ''))}</td></tr>")
    cuerpo.append("</table>")
    for pref, imagen in (("casa", "casa.png"), ("bulon", "bulon.png"), ("tij", "tijera.png")):
        h(2, f"ej_{pref}", t[f"ex_{pref}_h"])
        cuerpo.append(f"<p>{esc(t[f'ex_{pref}_p'])}</p><table class='ex'>")
        for a, b in t[f"ex_{pref}"]:
            cuerpo.append(f"<tr><td class='l' style='width:16%'>{esc(a)}</td><td style='width:84%'>{esc(b)}</td></tr>")
        cuerpo.append("</table>")
        if pref == "casa":
            cuerpo.append(f"<p>{esc(t['ex_casa_path'])}</p>")
        if pref == "tij":
            cuerpo.append(f"<p>{t['ex_tij_note']}</p>")
        ancho = 330 if pref == "tij" else 210
        cuerpo.append(f"<p class='center'><img src='{imagen}' width='{ancho}'><br><span class='k'>{esc(t[f'ex_{pref}_cap'])}</span></p>")

    # Ubicación de archivos y agradecimientos
    h(1, "repo", t["repo_h"])
    cuerpo.append("<table class='ex'>" + "".join(f"<tr><td class='l' style='width:16%'>{esc(a)}</td><td style='width:84%'>{b}</td></tr>" for a, b in t["repo"]) + "</table>")
    h(1, "ack", t["ack_h"], clase="cont")
    cuerpo += [f"<p>{esc(p)}</p>" for p in t["ack"]]

    cuerpo_html = "\n".join(cuerpo)
    # índice: nivel 1 y 2
    filas_toc = []
    for nivel, id_, texto in toc:
        pagina = numeros.get(id_, "00") if numeros else "00"
        filas_toc.append(f"<tr><td class='t{nivel}'>{esc(texto)}</td><td class='n t{nivel}'>{pagina}</td></tr>")
    toc_html = f"<h1 class='toc'>{esc(t['toc'])}</h1><table class='toc'>{''.join(filas_toc)}</table>"
    cuerpo_html = cuerpo_html.replace("@@TOC@@", toc_html)
    return f"<html><head><style>{CSS}</style></head><body>{cuerpo_html}</body></html>", toc


def maquetar(contenido: str, carpeta: Path, destino: Path) -> tuple[dict, dict]:
    """Dibuja el HTML en ``destino`` y devuelve ({id: página}, {id: rectángulo}) de lo que tiene id."""
    archivo = pymupdf.Archive(str(carpeta))
    archivo.add(str(AQUI / "img"))
    historia = pymupdf.Story(contenido, archive=archivo)
    escritor = pymupdf.DocumentWriter(str(destino))
    hoja = pymupdf.paper_rect("a4")
    area = hoja + (42, 72, -42, -52)
    paginas, rectas = {}, {}

    def rectangulo(n, lleno):
        return hoja, area, pymupdf.Identity

    def posicion(p):
        if p.open_close & 1 and p.id:
            paginas.setdefault(p.id, p.page_num)
            rectas.setdefault(p.id, tuple(p.rect))

    historia.write(escritor, rectangulo, posicion)
    escritor.close()
    return paginas, rectas


def franja(pagina, t: dict, x0: float, ancho: float, y0: float, y1: float) -> None:
    """Dibuja la cabecera azul de una tabla de comandos (ícono, comando, qué hace, requisitos)."""
    pagina.draw_rect(pymupdf.Rect(x0, y0, x0 + ancho, y1), color=None, fill=(0.118, 0.227, 0.541))
    for fraccion, titulo in ((0.0, t["col_icon"]), (0.09, t["col_cmd"]), (0.40, t["col_what"]), (0.78, t["col_req"])):
        pagina.insert_text((x0 + ancho * fraccion + 4, y1 - 4.5), titulo, fontsize=8, fontname="hebo", color=(1, 1, 1))


def pie_y_marcadores(destino: Path, idioma: str, toc: list, paginas: dict, rectas: dict) -> None:
    """Agrega encabezado, número de página, cabeceras de tabla y marcadores al PDF ya maquetado."""
    t = T[idioma]
    doc = pymupdf.open(str(destino))
    total = len(doc)
    ancho_tabla = doc[0].rect.width - 84
    for id_, (x0, y0, x1, y1) in rectas.items():
        if id_.startswith("h"):  # primera cabecera de cada tabla
            franja(doc[paginas[id_] - 1], t, x0, x1 - x0, y0, y1)
    for rid, profundidad in GRUPOS.items():  # fondo de las filas de grupo, detrás del texto
        if rid in rectas and rid in paginas:
            x0, y0, x1, y1 = rectas[rid]
            pagina = doc[paginas[rid] - 1]
            color = (0.91, 0.933, 0.988) if profundidad == 0 else (0.945, 0.961, 0.984)
            pagina.draw_rect(pymupdf.Rect(x0, y0, x1, y1), color=None, fill=color, overlay=False)
            pagina.draw_line((x0, y0), (x1, y0), color=(0.118, 0.227, 0.541), width=1.0, overlay=False)
    for numero in {paginas[rid] for rid in cortes_de(paginas) if rid in paginas}:  # tablas que continúan
        franja(doc[numero - 1], t, 42, ancho_tabla, 54, 70)
    for n, pagina in enumerate(doc):
        if n == 0:
            continue
        pagina.insert_text((42, 34), t["header"], fontsize=8, fontname="helv", color=(0.39, 0.45, 0.55))
        texto = f"{n + 1} / {total}"
        ancho = pymupdf.get_text_length(texto, fontname="helv", fontsize=8)
        pagina.insert_text((pagina.rect.width - 42 - ancho, pagina.rect.height - 28), texto, fontsize=8, fontname="helv", color=(0.39, 0.45, 0.55))
    for pagina in doc:  # enlaces de los agradecimientos (Story no conserva los <a>)
        for nombre, url in ENLACES.items():
            for r in pagina.search_for(nombre):
                pagina.insert_link({"kind": pymupdf.LINK_URI, "from": r, "uri": url})
                pagina.draw_line((r.x0, r.y1 - 1), (r.x1, r.y1 - 1), color=(0.118, 0.227, 0.541), width=0.5)
    marcadores = [[nivel, texto, paginas[id_]] for nivel, id_, texto in toc if id_ in paginas]
    if marcadores:
        marcadores[0][0] = 1
        doc.set_toc(marcadores)
    doc.set_metadata({"title": f"{t['title']} — {t['subtitle']}", "author": "Proyecto DAV — UADER", "subject": "DAV"})
    doc.save(str(destino) + ".tmp", garbage=3, deflate=True)
    doc.close()
    Path(str(destino) + ".tmp").replace(destino)


def cortes_de(paginas: dict) -> set:
    """Filas que abren una página nueva dentro de su tabla (ahí va una cabecera nueva)."""
    cortes = set()
    for ids in TABLAS:
        for previa, actual in zip(ids, ids[1:]):
            if paginas.get(actual) != paginas.get(previa):
                cortes.add(actual)
    return cortes


def construir(idioma: str, salida: Path) -> Path:
    destino = salida / ARCHIVO[idioma]
    with tempfile.TemporaryDirectory() as tmp:
        carpeta = Path(tmp)
        iconos = Iconos(carpeta)
        # Primera pasada: en qué página cae cada título. Segunda: el índice ya con esos números
        # (ocupa lo mismo que con «00», así que no mueve nada).
        contenido, toc = documento(idioma, iconos, None)
        paginas, _ = maquetar(contenido, carpeta, carpeta / "previo.pdf")
        contenido, toc = documento(idioma, iconos, paginas)
        paginas, rectas = maquetar(contenido, carpeta, destino)
        pie_y_marcadores(destino, idioma, toc, paginas, rectas)
    return destino


def main() -> None:
    global ARBOL
    analizador = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    analizador.add_argument("idiomas", nargs="*", choices=IDIOMAS)
    analizador.add_argument("--salida", default=str(RAIZ_REPO))
    args = analizador.parse_args()
    idiomas = args.idiomas or list(IDIOMAS)
    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    ARBOL = cargar_arbol()
    for idioma in idiomas:
        FALTAN.clear()
        USADAS.clear()
        destino = construir(idioma, salida)
        paginas = len(pymupdf.open(str(destino)))
        print(f"{idioma}: {destino} ({paginas} páginas)")
        if FALTAN:
            print(f"  sin descripción ({len(FALTAN)}):", ", ".join(sorted(set(FALTAN))))
    sobran = sorted(set(DESC) - USADAS)
    if sobran:
        print(f"  descripciones sin comando en el árbol ({len(sobran)}):", ", ".join(sobran[:40]), "…" if len(sobran) > 40 else "")


if __name__ == "__main__":
    main()
