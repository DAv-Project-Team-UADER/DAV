# Cómo probar y validar

Cómo comprobar que un cambio anda **antes** de mandarlo a revisión. Distintas
capas según lo que tocaste.

---

## 1. Prueba puramente técnica (rápida, sin FreeCAD)

Para código Python propio (prompts, pants, módulos), al menos:

### Sintaxis

```bash
# Windows (PowerShell)
python -c "import ast; ast.parse(open(r'<archivo>', encoding='utf-8').read()); print('OK')"
```

### Import / smoke test con el venv de desarrollo

El venv de desarrollo (`IntegracionGUI/GUIFreeCad/.venv`) tiene PySide6. Se
puede importar un módulo que no requiera FreeCAD en tiempo de import (si
importa `FreeCAD` arriba, usá import diferido dentro de las funciones — patrón
que usan los prompts).

### Lógica de prompts (sin abrir FreeCAD)

Los prompts heredan `BaseInputPrompt` y su lógica se puede probar llamando
`ProcessFinalText("...")` directamente con un `QApplication` offscreen:

```python
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt
from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication([])

p = PlaneSelectionInputPrompt()
print(p.ProcessFinalText("abajo").Success)   # navega
print(p.ProcessFinalText("okey").Value)       # confirma → valor del plano
```

Requiere que `GUIFreeCad` esté en `sys.path` (o configurar la ruta).

### Acciones de FreeCAD sin abrir la interfaz (`freecadcmd`)

Para comprobar que una **acción** (crear un boceto, un sólido, una hoja de TechDraw)
funciona de verdad no alcanza con parsear el archivo: hay que correrla en FreeCAD.
`freecadcmd` es FreeCAD **sin ventana**, con su Python y sus módulos (`Part`, `Sketcher`,
`Draft`, `TechDraw`), y se puede lanzar desde la terminal. Sirve tanto para las acciones
de los diccionarios como para los prompts que usan Qt (con el modo `offscreen`).

| Sistema | Ejecutable |
| --- | --- |
| Windows | `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe` |
| Linux | `freecadcmd` (o el de la carpeta de instalación) |

**Plantilla de un script de prueba** (guardala fuera del repo, por ejemplo en la carpeta
temporal de la sesión):

```python
import os, sys, traceback
os.environ["QT_QPA_PLATFORM"] = "offscreen"          # Qt sin pantalla

DAV = r"C:\ruta\al\repo\Dav"
sys.path[:0] = [
    DAV + r"\dic",                                   # para importar Explorer.Examples...
    DAV + r"\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad",   # para importar InputPrompts
]

out = open("resultado.txt", "w")                     # ver la nota sobre la salida
def log(*args):
    out.write(" ".join(str(a) for a in args) + "\n")
    out.flush()

try:
    import FreeCAD as App
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    App.newDocument("Prueba")
    from Explorer.Examples import _partdesign as ejemplo   # el módulo a probar
    for paso in ejemplo.steps():
        paso.Action()                                # corre cada acción en orden

    doc = App.ActiveDocument
    invalidos = [o.Name for o in doc.Objects if not o.isValid()]
    log("objetos:", len(doc.Objects), "invalidos:", invalidos)
except Exception:
    log(traceback.format_exc())
```

```powershell
& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" prueba.py
Get-Content resultado.txt
```

Qué mirar y qué tener en cuenta:

- **Comprobá `isValid()` de cada objeto** después de recalcular. Una operación que falla
  no lanza excepción: deja el objeto en estado inválido (por ejemplo un agujero que no
  se pudo crear).
- **Escribí los resultados en un archivo.** La salida estándar de `freecadcmd` depende de
  cómo se lo lance y muchas veces no vuelve a la terminal; un archivo es siempre confiable.
- **Sin interfaz no hay vista 3D.** `Gui.ActiveDocument`, `ViewFit` y los paneles no existen;
  el código de las acciones debe tolerarlo (ver `fitView()` en `Explorer/Examples/_common.py`).
  Lo que dependa de la vista se prueba dentro de FreeCAD con la interfaz.
- **El aviso `2 entries found for module 'dav'`** significa que hay dos copias del módulo
  instaladas y FreeCAD usa una sola. Al probar dentro de FreeCAD verificá que sea la copia
  que estás editando.
- **Probá los tres idiomas** de un prompt cambiando su idioma antes de dictar:
  `prompt._Language = "en"`.
- **Simulá la voz** llamando a `prompt.ProcessFinalText("frase")`: devuelve el
  `PromptResult`, así podés comprobar `Success`, `Value` y `Cancelled` sin micrófono.
- **Para un comando con parámetros**, `PromptedCommandExecutor.ExecuteEntry(entrada, ["cinco okey"])`
  recolecta con frases simuladas, una por parámetro.

---

## 2. Prueba de diccionarios / navegación

- **Cargar el dict maestro** no debe romper: si una carpeta tiene un dict roto,
  el `DictionaryLoader` lo omite y sigue (no tumba el motor).
- Verificá que las **frases nuevas aparecen** como opciones del contexto: en el
  panel, tras navegar al contexto, la ayuda/describir contexto listará los
  comandos disponibles (implícito en `Browser.DescribeContext`).
- Probá cada frase en los tres idiomas si agregaste traducciones.
- **Corré la verificación de los ejemplos guiados** si tocás los ejemplos o las palabras del
  árbol que usan. Reproduce, en es, en y pt, cada frase de cada cuadro por un `Browser` real,
  ejecuta las acciones y avisa qué frase no se resuelve o a qué comando llega. Necesita
  FreeCAD, así que se lanza con `freecadcmd`:

  ```powershell
  $tests = "Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad\tests"
  & "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" "$tests\verify_examples_paths.py"
  Get-Content "$tests\verify_examples_paths.txt"
  ```

  Que una frase «se resuelva» no alcanza: mirá también a qué comando llega cada cuadro (`->`
  en el informe). Así se encontró, por ejemplo, que «cortar» dicho desde *Sumar* llegaba a
  «cotar» por coincidencia aproximada, y que desde *Círculo* «crear» salta a Workbench.
- **Corré la prueba de la jerarquía real** después de tocar cualquier diccionario. Necesita
  la carpeta `Dav` en el `PYTHONPATH` (los `TraduceTo*` importan `dic.StdView...`); sin
  eso fallan dos pruebas por `No module named 'dic'`, aunque el árbol esté bien:

  ```powershell
  cd Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad
  $env:PYTHONPATH = "<ruta al repo>\Dav"
  python -m unittest tests.test_real_dictionaries
  ```

  Comprueba que `base.py` importa limpio, que ningún submenú está aplanado y que las
  traducciones no quedaron vacías. Alta prioridad: un solo import roto en una hoja
  profunda deja al `Browser` sin comandos y el `DictionaryLoader` no lo avisa.

---

## 3. Prueba integrada en FreeCAD (la que vale)

Corré el motor de voz dentro de FreeCAD (ver [setup](setup.md)) y probá el
flujo real por voz. Las guías existentes detallan qué esperar:

| Guía | Cubre |
|---|---|
| [guia-pruebas-partdesign-voz.md](../guia-pruebas-partdesign-voz.md) | PartDesign por voz con medidas dictadas (sólidos, extrusión, cortes, acabados) |
| [guia-pruebas-3d-voz.md](../guia-pruebas-3d-voz.md) | Flujo completo desde dibujo 2D y Assembly |
| [guia-prueba-numeros-alumnos.md](../guia-prueba-numeros-alumnos.md) | Dictado de números (cómo decir medidas) |
| [manual-selection-voz.md](../manual-selection-voz.md) | Selección de objetos por voz |
| [manual-explorer-voz.md](../manual-explorer-voz.md) | Explorer por voz (archivos) |
| [informe_pruebas_draftwork.md](../informe_pruebas_draftwork.md) | Reporte de pruebas del workbench Draft |

### Consejos de prueba

- **`donde estoy`** para ubicarte; **`subir`** para subir de nivel.
- Confirmar pop-ups: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`.
  Abortar: `cancelar`.
- Si un comando "no se escucha", pensá en la **gramática acotada**: algunos
  prompts (numéricos, selector de plano) limitan qué palabras acepta Vosk a
  propósito (ver [acortador-gramatica-vosk.md](../acortador-gramatica-vosk.md)).

---

## 4. Correr los tests del proyecto

Hay infraestructura de tests/validación en `Dav/scr/validation/`:

- `test_validator.py` — pruebas del `Validator`.
- `test_integration.py` — pruebas de integración (incluye
  `PromptedCommandExecutor`).
- `run_tests.py` — correr los tests de la carpeta.
- `prueba_validator.py` — helper de prueba/validación.

```bash
python Dav/scr/validation/run_tests.py
```

> El `Validator` se integra a la ejecución de comandos vía
> `PromptedCommandExecutor` (validación previa de parámetros). Si tu comando
> toma parámetros, añadí cobertura en estas pruebas cuando corresponda.

---

## Checklist rápido antes de mandar el PR

- [ ] Sintaxis OK (AST parse) en archivos modificados/nuevos.
- [ ] No se aplanan subcontextos (`.update(sub_dict)`).
- [ ] Archivos nuevos con cabezal obligatorio.
- [ ] Docstrings en inglés para clases/métodos públicos.
- [ ] Frases probadas en los idiomas que toquen.
- [ ] Flujo real por voz probado en FreeCAD (si se puede).
- [ ] Actualizada la guía/doc si cambiaste una convención o un comportamiento.