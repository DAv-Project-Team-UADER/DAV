# DAV — Contexto: Cómo se arman los diccionarios

> Proyecto DAV · IV Encuentro · Mayo 2026 · UADER - FCyT

---

## Qué es un diccionario DAV

Cada diccionario es un **archivo `.py` que contiene un `dict` de Python**. La llave es el nombre de invocación en inglés (lo que dice el usuario por voz) y el valor es una función o lambda que ejecuta el comando correspondiente en FreeCAD.

El sistema DAV navega ese árbol de diccionarios para ejecutar comandos por voz.

---

## Distribución de secciones

| Sección | Workbenches | Tickets | Personas |
| --- | --- | --- | --- |
| A — PartDesign | PartDesign Workbench | 36 | 2 |
| B — Draft + TechDraw | Draft Workbench + TechDraw Workbench | 121 (59+62) | 7 |
| C — Part + Assembly | Part Workbench + Assembly Workbench | 70 (46+24) | 4 |
| D — DAVExplorer | Explorer (módulo DAV) | 31 | 2 |
| **TOTAL** | | **258** | **15** |

---

## Pasos para armar un diccionario

### Paso 1 — Preparar el material

1. Abrir la documentación oficial de FreeCAD para los workbenches de tu sección:
   `https://wiki.freecad.org/Main_Page` → sección del workbench correspondiente
2. Reunir todos los tickets de tu sección desde la carpeta:
   `tickets_unificados/Workbench/[nombre]` para workbenches, o `tickets_unificados/Explorer/`, `tickets_unificados/StdView/`, `tickets_unificados/LineAttributes/` según corresponda.
3. Leer cada ticket: anotar el nombre del comando, qué hace y los parámetros que recibe.

---

### Paso 2 — Diseñar la estructura en papel (SIN IA)

Antes de escribir código, hacer en papel un árbol de conjuntos y subconjuntos. **Esta es la parte de mayor valor del trabajo.**

- **Conjunto:** agrupar los comandos por categoría funcional (ej: dibujo, restricciones, vistas, modificaciones).
- **Subconjunto:** si un conjunto tiene variantes (ej: arco por centro vs. arco por 3 puntos), ese conjunto pasa a ser un subconjunto.
- **Elemento suelto:** un comando sin variantes va directamente dentro del conjunto padre.
- **ToolBar:** los elementos marcados como ToolBar van **siempre sueltos**, nunca dentro de un subconjunto.

**Reglas de nomenclatura:**

- Todo en inglés, excepto `ayuda.py`. **Excepción:** el módulo `Explorer/` usa nombres en español (`Archivos`, `Herramientas`, `Intercambio`, `Ventanas`) porque refleja el menú de FreeCAD en español.
- Una sola palabra cuando sea posible: `'circle'`, `'arc'`, `'line'`.
- No repetir el contexto padre en el nombre. Dentro de `arc/` no se dice `'arc_from_center'`, se dice `'center'`.
- Formas cortas: `'points'` en vez de `'multipoint'`, `'elliptic'` en vez de `'elliptical_arc'`.

---

### Paso 3 — Crear los archivos `.py`

Un subconjunto = una carpeta con su nombre. Dentro van el `.py` del subconjunto y las sub-subcarpetas si las hay.

**Árbol de carpetas actual de `DiccionariosEnBruto/`:**

```text
DiccionariosEnBruto/
├── Explorer/                  # Módulo DAV propio (abrir, guardar, exportar, ventanas)
│   ├── File/
│   ├── Edit/
│   └── Windows/
├── LineAttributes/            # Atributos de línea (vacío — pendiente)
├── StdView/                   # Vista estándar de FreeCAD
│   ├── Appearance/
│   ├── Camera/
│   ├── DrawStyles/
│   ├── Overlay/
│   ├── Panels/
│   ├── SavedViews/
│   ├── StandardViews/
│   ├── Stereo/
│   ├── Toolbars/
│   ├── Tree/
│   └── Visibility/
└── Workbench/
    ├── Assembly/              # Assembly Workbench
    ├── DraftWork/             # Draft Workbench
    ├── Part/                  # Part Workbench
    ├── PartDesign/            # PartDesign Workbench (vacío — pendiente)
    ├── Sketcher/              # Sketcher Workbench (vacío — pendiente)
    └── TechDraw/              # TechDraw Workbench
        ├── AddLines/
        ├── AddVertices/
        ├── Annotations/
        ├── Dimensions/
        ├── Features/
        ├── Hatching/
        ├── OtherViews/
        ├── Page/
        ├── Symbols/
        └── Views/
```

**Estructura de ejemplo (un workbench):**

```text
Workbench/
  workbench.py        # diccionario raíz del workbench
  ayuda.py            # explica los elementos sueltos del nivel raíz
  arc/
    arc.py            # subconjunto de arcos
    ayuda.py          # explica: center, points, elliptic, hyperbolic
    circle/
      circle.py
      ayuda.py
```

---

### Paso 4 — Editar los diccionarios en Python

Hay dos niveles con comportamiento distinto:

**Diccionario raíz (`workbench.py`) — usa `.update()` (diseño plano):**

El diccionario raíz aplana todos sus submódulos en un único dict. Esto permite que el usuario diga un solo comando de voz sin navegar niveles. Los submódulos se incorporan con `.update()`, no como llaves anidadas.

```python
# workbench.py
from .arc.arc   import arc
from .line.line import line
from .ayuda     import ayuda

workbench = {}
workbench.update(arc)
workbench.update(line)
workbench.update({'help': ayuda})
```

**Subconjunto (`arc/arc.py`) — usa dict literal con llaves:**

Cada subconjunto es un dict donde las llaves son las palabras de voz y los valores son lambdas. No usa `.update()`.

```python
# arc/arc.py
from .ayuda import ayuda

arc = {
    'center':   lambda: Gui.runCommand('Workbench_ArcByCenter', 0),
    'points':   lambda: Gui.runCommand('Workbench_Arc3Points', 0),
    'elliptic': lambda: Gui.runCommand('Workbench_EllipticArc', 0),
    'help':     ayuda,
}
```

---

### Tres niveles de script para el valor de un dict

El valor de cada llave puede ser uno de tres tipos según lo que requiere el ticket:

**Nivel 1 — Comando simple (preferido):**
Existe un `Gui.runCommand` directo. Usar siempre que el ticket lo indique.

```python
'front': lambda: Gui.runCommand('Std_ViewFront', 0),
```

**Nivel 2 — API Python con parámetros (objetos paramétricos):**
El comando requiere pasar valores por voz (dimensiones, radios, puntos). Se usa la API de FreeCAD directamente.

```python
'new': lambda: FreeCAD.newDocument(),
'save': lambda: FreeCAD.activeDocument().save(),
'quit': lambda: Gui.getMainWindow().close(),
```

**Nivel 3 — API Qt / vista 3D (sin runCommand equivalente):**
Para comandos que operan sobre la vista directamente o requieren Qt.

```python
'zoomin':  lambda: FreeCADGui.ActiveDocument.ActiveView.zoomIn(),
'zoomout': lambda: FreeCADGui.ActiveDocument.ActiveView.zoomOut(),
'workbench': lambda wb='PartDesign': Gui.activateWorkbench(wb),
```

**Regla:** Si el ticket tiene un `Gui.runCommand(...)` válido, usar Nivel 1 aunque el script del ticket use API compleja. La API compleja en el ticket es solo para entender qué hace, no la implementación obligatoria. Excepción: si necesita pasar parámetros variables por voz, usar Nivel 2.

**Tickets que NO tienen `runCommand` equivalente** (deben usar Nivel 3):

- `StdViewZoomIn/Out` → `view.zoomIn()` / `view.zoomOut()`
- `StdSelBoundingBox` → `FreeCAD.ParamGet(...).SetBool(...)`
- `StdWorkbench` → `Gui.activateWorkbench('NombreWorkbench')`
- Stereo (Iv*) → `view.setStereoType('...')` aunque el dict puede usar `runCommand` (ambos funcionan)
- Toolbar (Clipboard/Edit/File/etc.) → solo Qt; el dict usa `runCommand('Std_Toolbar*')` como aproximación válida

**Archivo de ayuda (`ayuda.py`, en español):**

```python
# ayuda.py
def ayuda():
    print('Comandos disponibles en este nivel:')
    print(' line    - Crea una línea entre dos puntos')
    print(' point   - Crea un punto')
    print(' arc     - Subconjunto: tipos de arco (center, points, elliptic)')
```

---

### Paso 5 — Probar

Importar el diccionario más exterior en la consola de Python de FreeCAD y navegar hasta cada elemento terminal. Verificar que:

- El nombre del comando coincide con uno real de FreeCAD (consultar la wiki).
- `Gui.runCommand()` recibe exactamente el nombre de la API, no texto descriptivo.
- Cada carpeta tiene su `ayuda.py`.
- No hay nombres duplicados dentro del mismo diccionario.

---

## Resumen de convenciones

| Regla | Detalle |
| --- | --- |
| **Idioma** | Todo en inglés, excepto `ayuda.py` (que va en español) |
| **Nombres** | Una sola palabra, sin repetir el contexto del padre |
| **Llave de ayuda** | Siempre `'help': ayuda` — en inglés, igual que las demás llaves |
| **ToolBar** | Los elementos de tipo ToolBar van sueltos, no en subconjunto |
| **Subconjunto** | Siempre en su propia carpeta; la carpeta lleva el mismo nombre |
| **`ayuda.py`** | Obligatorio en cada carpeta; contiene `print()` con las descripciones de los tickets |
| **Valor del dict** | Es una lambda que ejecuta `Gui.runCommand('Nombre_Cmd', 0)` |
| **Diccionario raíz** | Usa `dict = {}` + `.update(submodulo)` para cada subconjunto — nunca dict literal `{...}` |
| **Script del ticket** | El campo `script nativo` del ticket indica exactamente el `Gui.runCommand` a usar |
| **Prueba** | Siempre probar desde el diccionario más exterior hacia adentro, uno por uno |
| **Sin IA (diseño)** | La estructura de conjuntos/subconjuntos se decide en papel, sin asistencia de IA |
