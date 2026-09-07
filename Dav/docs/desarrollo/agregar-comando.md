# Agregar un comando por voz

El objetivo es que al decir una **frase hablada** se ejecute una **acción** de
FreeCAD. Eso se logra tocando el **árbol de comandos** (`Dav/dic/`), sin tocar
el motor (`Browser`).

Cada carpeta de `Dav/dic/` es un **nivel de contexto** y tiene:

1. **Un diccionario maestro** (`<nombre>.py`) — claves internas → callables.
2. **Traducciones por idioma** (`TraduceToEs.py`, `TraduceToEn.py`,
   `TraduceToPT.py`) — frases habladas → los mismos callables.

## Paso a paso

### 1. Ubicá la carpeta del contexto

Por ejemplo, los comandos del workbench Sketcher viven en
`Dav/dic/Workbench/Sketcher/`. Si el comando corresponde a un submenú, va en su
carpeta hija (ej. `Sketcher/point/point.py`, `Sketcher/Geometry/geometry.py`).

### 2. Agregá la clave interna al diccionario maestro

Dentro del dict maestro (ej. `sketcher.py`), agregá la clave y su callable:

```python
sketcher = {}
sketcher.update({
    'new': _new_sketch,     # función propia que crea el boceto
    'edit': lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    # ...
})
```

> Si la acción es un comando nativo de FreeCAD que **no** abre un diálogo
> controlable por voz, un `lambda: Gui.runCommand('Comando_De_FreeCAD', 0)`
> alcanza. Si el comando nativo abre un diálogo propio (como el selector de
> plano de `Sketcher_NewSketch`), hay que reemplazarlo por una acción propia de
> DAV con un prompt controlable por voz (ver el ejemplo más abajo).

### 3. Agregá las frases habladas en los `TraduceTo*.py`

En el `TraduceToEs.py` del contexto, mapeá la/s frase/s a la clave:

```python
from .sketcher import sketcher

TraduceToEs = {
    "nuevo": sketcher["new"],
    "nuevo croquis": sketcher["new"],
    "crear croquis": sketcher["new"],
    # ...
}
```

> Sumar sinónimos es **solo** editar estos diccionarios: no hay que tocar el
> motor. El `DictionaryLoader` normaliza acentos al comparar, así que las
> variantes con/sin tilde son opcionales pero inofensivas.

### 4. (Opcional) Actualizá el `ayuda.py` de la carpeta

Muchos contextos tienen un `ayuda.py` que imprime los comandos disponibles.
Agregá la línea del comando nuevo para que la ayuda sea consistente.

### 5. Probalo

Comprobá que la frase navega y ejecuta la acción (ver
[probando.md](probando.md)). Probá en los **tres idiomas** si agregaste frases
en los tres `TraduceTo`.

---

## Ejemplo real: el selector de plano por voz al crear un boceto

Contexto: FreeCAD abre un diálogo nativo (`Sketcher_NewSketch`) que **no es
controlable por voz**. La solución fue una acción propia de DAV que muestra un
prompt navegable por voz.

**Archivos tocados** (referencia):

- `Dav/scr/.../InputPrompts/PlaneSelectionInputPrompt.py` — la ventana de
  selección: recorre `XY` / `XZ` / `YZ` con `arriba`/`abajo` y confirma con
  `okey`/`cancelar` (heredando `BaseInputPrompt`).
- `Dav/dic/Workbench/Sketcher/new_sketch/new_sketch.py` — la acción: muestra el
  prompt, toma el plano elegido y crea el `Sketcher::SketchObject` con el
  mismo placement que el comando nativo.
- `Dav/scr/.../InputPrompts/PlaneGrammarSwitcher.py` — acota la gramática de
  Vosk mientras el prompt está abierto a solo `arriba/abajo/okey/cancelar`,
  para que no confunda "abajo" con "trabajo".
- `Dav/dic/Workbench/Sketcher/sketcher.py` — `'new'` ahora apunta a
  `_new_sketch` en lugar de `Gui.runCommand('Sketcher_NewSketch', 0)`.
- `Dav/dic/Workbench/Sketcher/Geometry/geometry.py` — idem para el subcontexto
  de geometría.
- `Dav/dic/Workbench/Sketcher/TraduceToEs.py` — sinónimos nuevos
  `nuevo boceto` / `crear boceto` / `boceto nuevo`.

**Puntos a copiar de este ejemplo**:

- Si el comando abre un diálogo nativo, **reemplazalo** por un prompt DAV
  (heredá `BaseInputPrompt` y usá `PromptVoiceRouter`).
- Si el prompt necesita que Vosk escuche solo un conjunto chico de palabras,
  usá un "grammar switcher" (patrón `NumericGrammarSwitcher`) y restamelo
  al cerrar.
- Avisá en la GUI (con `print`) el resultado de la acción para que aparezca en
  el historial del panel.

---

## Reglas para no romper nada

- **Subcontextos anidados**: `explorer.update({'file': file})`, nunca
  `explorer.update(file)`. Ver [convenciones](convenciones.md) y
  `pendientes-dav.md` §4.
- Los `TraduceTo*.py` deben importar el dict maestro y enlazar
  **por objeto/clave**, no duplicar callables.
- Mantené el **cabezal obligatorio** en cada archivo nuevo.
- No toques `browser.py` para sumar un comando: el comando va en el diccionario.

---

Siguiente: [Cómo probar y validar](probando.md)