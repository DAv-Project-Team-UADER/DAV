# Manual de usuario (PDF) — cómo se genera

`Manual_Usuario.pdf`, `User_Manual.pdf` y `Manual_do_Usuario.pdf` (raíz del repositorio) **no se
editan a mano**: los arma `build_manual.py` leyendo los diccionarios reales de `Dav/dic/`.

```
pip install pymupdf
python Dav/docs/manual/build_manual.py          # los tres idiomas
python Dav/docs/manual/build_manual.py es       # solo uno (es | en | pt)
python Dav/docs/manual/build_manual.py --salida C:/tmp
```

| Archivo | Qué contiene |
|---|---|
| `arbol.py` | Carga el árbol de diccionarios (con FreeCAD y Qt simulados): grupos, comandos, frases en cada idioma e íconos SVG (mismo criterio que `IconLocator`) |
| `desc_*.py` | **Qué hace** cada comando, en español, inglés y portugués, y su requisito |
| `textos.py` | Textos fijos (introducción, navegación, ejemplos, agradecimientos) y los requisitos reutilizables |
| `build_manual.py` | Arma el HTML y lo maqueta en PDF (con índice, marcadores y cabeceras de tabla) |
| `img/` | Logo y capturas de los ejemplos guiados |

## Agregar una función al manual

1. Agregarla al diccionario como siempre (con su `TraduceTo*.py` y su `<clave>.svg`).
2. En el `desc_*.py` del banco que corresponda, sumar la entrada
   `"ruta/clave": ("español", "inglés", "portugués"[, "código de requisito"])`.
   La ruta es la de las claves del diccionario (`workbench/partdesign/additive/pad`).
3. Volver a correr `build_manual.py`. Avisa qué comandos quedaron **sin descripción**.

Los **grupos** (submenús como «agregar» de PartDesign) salen solos como una fila con su ícono y
las frases para entrar; solo hace falta su descripción. Un grupo sin SVG propio usa el ícono de su
primer comando; un comando sin SVG puede tomar el de su variante en `ICONO_PARIENTE`
(`build_manual.py`). Los códigos de requisito (`doc`, `sel`, `bodysk`…) están en `textos.py`.
