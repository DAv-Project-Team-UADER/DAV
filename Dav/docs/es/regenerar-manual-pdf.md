# Regenerar el manual de usuario (PDF)

`Manual_Usuario.pdf` (español), `User_Manual.pdf` (inglés) y `Manual_do_Usuario.pdf` (portugués)
están en la **raíz del repositorio** y **no se editan a mano**: los arma
[`build_manual.py`](../manual/build_manual.py) leyendo los diccionarios reales de `Dav/dic/`
(grupos, comandos, frases en cada idioma e íconos). Por eso el manual no se desactualiza al
agregar una función: alcanza con volver a generarlo.

## Requisitos

- Python 3 con **PyMuPDF** y **PySide6** (Qt se usa para rasterizar los íconos SVG):

  ```
  pip install pymupdf PySide6
  ```

- No hace falta tener FreeCAD instalado: `arbol.py` simula FreeCAD y Qt al cargar el árbol.

## Generar los PDF

Desde la raíz del repositorio (también funciona desde cualquier carpeta):

```
python Dav/docs/manual/build_manual.py              # los tres idiomas
python Dav/docs/manual/build_manual.py es           # solo uno (es | en | pt)
python Dav/docs/manual/build_manual.py --salida C:/tmp   # otra carpeta de salida
```

Por defecto escribe los tres PDF en la raíz del repositorio, pisando los existentes. Al terminar
avisa qué comandos quedaron **sin descripción** en los `desc_*.py`.

## Qué hay en `Dav/docs/manual/`

| Archivo | Qué contiene |
|---|---|
| `arbol.py` | Carga el árbol de diccionarios: grupos, comandos, frases e íconos SVG (mismo criterio que `IconLocator`) |
| `desc_*.py` | **Qué hace** cada comando, en español, inglés y portugués, y su requisito |
| `textos.py` | Textos fijos (introducción, navegación, ejemplos, agradecimientos) y los requisitos reutilizables |
| `build_manual.py` | Arma el HTML y lo maqueta en PDF (índice, marcadores y cabeceras de tabla) |
| `img/` | Logo y capturas de los ejemplos guiados |

## Agregar una función al manual

1. Agregarla al diccionario como siempre (con su `TraduceTo*.py` y su `<clave>.svg`).
2. En el `desc_*.py` del banco que corresponda, sumar la entrada
   `"ruta/clave": ("español", "inglés", "portugués"[, "código de requisito"])`.
   La ruta es la de las claves del diccionario (`workbench/partdesign/additive/pad`).
3. Volver a correr `build_manual.py` y revisar el aviso de comandos sin descripción.
4. Hacer commit de los tres PDF regenerados junto con el cambio.

Los **grupos** (submenús como «agregar» de PartDesign) salen solos como una fila con su ícono y
las frases para entrar; solo hace falta su descripción. Un grupo sin SVG propio usa el ícono de su
primer comando; un comando sin SVG puede tomar el de su variante en `ICONO_PARIENTE`
(`build_manual.py`). Los códigos de requisito (`doc`, `sel`, `bodysk`…) están en `textos.py`.

## Problemas frecuentes

- **`ModuleNotFoundError: pymupdf` / `PySide6`**: instalar los paquetes de arriba en el mismo
  Python con el que se corre el script.
- **Un comando aparece sin descripción o sin ícono**: falta su entrada en `desc_*.py` o su
  `<clave>.svg` en el diccionario.
- **El PDF no cambia**: confirmar que se escribió en la carpeta esperada (opción `--salida`) y
  que el visor no tiene el archivo abierto (en Windows bloquea la escritura).
