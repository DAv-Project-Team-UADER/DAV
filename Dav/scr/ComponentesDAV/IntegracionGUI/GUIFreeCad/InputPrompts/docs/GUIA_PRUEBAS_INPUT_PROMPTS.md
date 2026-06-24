# Guia de pruebas - InputPrompts

Este documento describe como probar la implementacion de `InputPrompts`, desde pruebas unitarias/manuales hasta una prueba completa con funciones reales de `DiccionariosEnBruto`.

Ruta base del modulo:

```text
luigiIntegracionV1/GUIFreeCad/InputPrompts/
```

Antes de empezar, abrir FreeCAD desde el proyecto DAV:

```powershell
.\iniciar_dav.ps1
```

Luego usar la consola Python de FreeCAD.

## Preparacion comun

En la consola Python de FreeCAD, ejecutar:

```python
import sys
sys.path.insert(0, r"D:\Facultad\PET DAV\Fork\DAV\luigiIntegracionV1\GUIFreeCad")
sys.path.insert(0, r"D:\Facultad\PET DAV\Fork\DAV\validation")
```

Si vas a probar comandos reales del diccionario, tambien conviene definir:

```python
import os
os.environ["DAV_DICTIONARY_ROOT"] = r"D:\Facultad\PET DAV\Fork\DAV\DiccionariosEnBruto"
os.environ["DAV_VALIDATION_ROOT"] = r"D:\Facultad\PET DAV\Fork\DAV\validation"
```

## Prueba 1 - IntegerInputPrompt

Objetivo: verificar que una frase numerica hablada se convierta en `int`.

```python
from InputPrompts.IntegerInputPrompt import IntegerInputPrompt

Prompt = IntegerInputPrompt("Integer", "Deci un entero")
Prompt.Show()
Prompt.ProcessFinalText("uno dos enviar")
print(Prompt.GetResult())
```

Resultado esperado:

```text
PromptResult(Success=True, Value=12, Cancelled=False, Error='')
```

Tambien probar cancelacion:

```python
Prompt = IntegerInputPrompt("Integer", "Deci un entero")
Prompt.Show()
Prompt.ProcessFinalText("cancelar")
print(Prompt.GetResult())
```

Resultado esperado:

```text
PromptResult(Success=False, Value=None, Cancelled=True, Error='')
```

## Prueba 2 - FloatInputPrompt

Objetivo: verificar captura de decimales.

```python
from InputPrompts.FloatInputPrompt import FloatInputPrompt

Prompt = FloatInputPrompt("Float", "Deci un decimal")
Prompt.Show()
Prompt.ProcessFinalText("cinco coma dos enviar")
print(Prompt.GetResult())
```

Resultado esperado:

```text
PromptResult(Success=True, Value=5.2, Cancelled=False, Error='')
```

Probar portugues:

```python
Prompt = FloatInputPrompt("Float", "Diga um decimal")
Prompt.Show()
Prompt.ProcessFinalText("quatro ponto meia aceitar")
print(Prompt.GetResult())
```

Resultado esperado:

```text
PromptResult(Success=True, Value=4.6, Cancelled=False, Error='')
```

## Prueba 3 - StringInputPrompt

Objetivo: verificar captura de texto libre.

```python
from InputPrompts.StringInputPrompt import StringInputPrompt

Prompt = StringInputPrompt("Text", "Deci un texto")
Prompt.Show()
Prompt.ProcessFinalText("linea prueba enviar")
print(Prompt.GetResult())
```

Resultado esperado:

```text
PromptResult(Success=True, Value='linea prueba', Cancelled=False, Error='')
```

## Prueba 4 - ObjectSelectionInputPrompt

Objetivo: verificar seleccion de objetos del documento activo.

Primero crear objetos visibles:

```python
import FreeCAD as App

doc = App.newDocument("DAVPromptTest")
box = doc.addObject("Part::Box", "BoxTest")
cylinder = doc.addObject("Part::Cylinder", "CylinderTest")
sphere = doc.addObject("Part::Sphere", "SphereTest")
doc.recompute()
```

Luego probar el prompt:

```python
from InputPrompts.ObjectSelectionInputPrompt import ObjectSelectionInputPrompt

Prompt = ObjectSelectionInputPrompt("Object", "Selecciona un objeto")
Prompt.Show()

Prompt.ProcessFinalText("siguiente")
print(Prompt.GetResult())

Prompt.ProcessFinalText("enviar")
print(Prompt.GetResult())
```

Resultado esperado despues de `siguiente`:

```text
PromptResult(Success=False, Value=None, Cancelled=False, Error='')
```

Resultado esperado despues de `enviar`:

```text
PromptResult(Success=True, Value='CylinderTest', Cancelled=False, Error='')
```

Notas:

- `doc.recompute()` es importante para que FreeCAD registre y muestre correctamente los objetos.
- Por defecto el prompt devuelve el nombre del objeto.
- Si se necesita devolver el objeto real de FreeCAD:

```python
Prompt = ObjectSelectionInputPrompt("Object", "Selecciona un objeto", ReturnObject=True)
```

## Prueba 5 - ParameterCollector con entradas simuladas

Objetivo: probar parser, prompts simulados y `Validator`, sin usar voz real.

```python
from InputPrompts.ParameterCollector import ParameterCollector

def CreateLine(x1: float, y1: float, x2: float, y2: float, label: str):
    print("Line:", x1, y1, x2, y2, label)

Collector = ParameterCollector(DelayMs=0)
Result = Collector.CollectForFunction(
    CreateLine,
    SimulatedFinalTexts=[
        "uno dos enviar",
        "dos enviar",
        "cinco enviar",
        "dos enviar",
        "linea prueba enviar",
    ],
)

print(Result)
```

Resultado esperado:

```text
PromptResult(Success=True, Value={'x1': 12.0, 'y1': 2.0, 'x2': 5.0, 'y2': 2.0, 'label': 'linea prueba'}, Cancelled=False, Error='')
```

Tambien se puede verificar que `Validator` describe los requisitos:

```python
print(Collector.GetRequirementsText(CreateLine))
```

Resultado esperado:

```text
Dato1: se espera un numero decimal
Dato2: se espera un numero decimal
Dato3: se espera un numero decimal
Dato4: se espera un numero decimal
Dato5: se espera un texto
```

## Prueba 6 - PromptedCommandExecutor con entrada simulada

Objetivo: probar ejecucion final con parametros.

```python
from InputPrompts.PromptedCommandExecutor import PromptedCommandExecutor

state = {}

class Entry:
    InternalKey = "create_line"

    def IsCallable(self):
        return True

def CreateLine(x1: float, y1: float, x2: float, y2: float):
    state["line"] = (x1, y1, x2, y2)

Entry.Target = CreateLine

Executor = PromptedCommandExecutor(DelayMs=0)
Executor.ExecuteEntry(
    Entry(),
    SimulatedFinalTexts=[
        "uno dos enviar",
        "dos enviar",
        "cinco enviar",
        "dos enviar",
    ],
)

print(state)
print(Executor.LastResult)
```

Resultado esperado:

```text
{'line': (12.0, 2.0, 5.0, 2.0)}
PromptResult(Success=True, Value={'x1': 12.0, 'y1': 2.0, 'x2': 5.0, 'y2': 2.0}, Cancelled=False, Error='')
```

## Prueba 7 - Motor de voz existente con prompt activo

Objetivo: verificar que `DavVoiceService` envie la voz al prompt activo, sin crear otro microfono.

Primero iniciar la voz desde FreeCAD:

```text
DAV -> Iniciar voz DAV
```

Luego, en la consola Python:

```python
from InputPrompts.IntegerInputPrompt import IntegerInputPrompt
from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

Prompt = IntegerInputPrompt("Integer", "Deci un entero")
Prompt.Show()
PromptVoiceRouter.SetActivePrompt(Prompt)
```

Ahora hablar:

```text
uno dos enviar
```

Luego consultar:

```python
print(Prompt.GetResult())
PromptVoiceRouter.ClearActivePrompt(Prompt)
```

Resultado esperado:

```text
PromptResult(Success=True, Value=12, Cancelled=False, Error='')
```

Si esto funciona, significa que:

- El microfono usado es el de `DavVoiceService`.
- La frase fue enviada al prompt activo.
- La frase no fue interpretada como comando normal del `Browser`.

## Prueba 8 - Funcion real del diccionario: geometry.line/create_by_points

Esta es la prueba mas importante con un comando real existente en `DiccionariosEnBruto`.

Funcion real:

```text
DiccionariosEnBruto/Workbench/Sketcher/Geometry/line/_parametric.py
```

Firma:

```python
def create_by_points(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str = "Segment",
) -> None:
```

Esta funcion crea una linea `Part::Feature` desde `(x1, y1)` hasta `(x2, y2)`.

### 8.1 Crear documento

```python
import FreeCAD as App

doc = App.newDocument("DAVLineDictionaryTest")
doc.recompute()
```

### 8.2 Cargar funcion real desde el diccionario

```python
import sys
import os

sys.path.insert(0, r"D:\Facultad\PET DAV\Fork\DAV\validation")
os.environ["DAV_DICTIONARY_ROOT"] = r"D:\Facultad\PET DAV\Fork\DAV\DiccionariosEnBruto"

from dictionary_resolver import GetDictionaryFunction

Function = GetDictionaryFunction("geometry.line", "create_by_points")
print(Function)
```

Resultado esperado:

```text
<function create_by_points ...>
```

### 8.3 Probar con ParameterCollector simulado

```python
from InputPrompts.ParameterCollector import ParameterCollector

Collector = ParameterCollector(DelayMs=0)
Result = Collector.CollectForFunction(
    Function,
    SimulatedFinalTexts=[
        "uno dos enviar",
        "dos enviar",
        "cinco enviar",
        "dos enviar",
    ],
)

print(Result)
```

Resultado esperado:

```text
PromptResult(Success=True, Value={'x1': 12.0, 'y1': 2.0, 'x2': 5.0, 'y2': 2.0}, Cancelled=False, Error='')
```

Nota: `label` tiene valor por defecto, por eso no se pide.

### 8.4 Ejecutar la funcion con los datos recolectados

```python
if Result.Success:
    Function(**Result.Value)
```

Resultado esperado en consola:

```text
[geometry.line] Created 'Segment' from (12.0,2.0) to (5.0,2.0)
```

Tambien deberia aparecer un objeto nuevo en el documento, con label `Segment`.

Verificar:

```python
print([obj.Name for obj in App.activeDocument().Objects])
print([obj.Label for obj in App.activeDocument().Objects])
```

### 8.5 Probar con PromptedCommandExecutor

```python
from InputPrompts.PromptedCommandExecutor import PromptedCommandExecutor

class Entry:
    InternalKey = "create_by_points"

    def IsCallable(self):
        return True

Entry.Target = Function

Executor = PromptedCommandExecutor(DelayMs=0)
Executor.ExecuteEntry(
    Entry(),
    SimulatedFinalTexts=[
        "uno dos enviar",
        "dos enviar",
        "cinco enviar",
        "dos enviar",
    ],
)

print(Executor.LastResult)
```

Resultado esperado:

```text
PromptResult(Success=True, Value={'x1': 12.0, 'y1': 2.0, 'x2': 5.0, 'y2': 2.0}, Cancelled=False, Error='')
```

Y deberia crearse otra linea en el documento.

## Prueba 9 - Funcion real con objeto: additive/pad_sketch

Esta prueba valida parametros de tipo `object`.

Funcion real:

```text
DiccionariosEnBruto/Workbench/PartDesign/additive/_parametric.py
```

Firma:

```python
def pad_sketch(sketch: object, length: float = 10.0) -> None:
```

La funcion espera un objeto `sketch`. El parametro `length` es opcional, por eso `ParameterCollector` no lo pide.

### 9.1 Crear un sketch simple

```python
import FreeCAD as App

doc = App.newDocument("DAVPadDictionaryTest")
sketch = doc.addObject("Sketcher::SketchObject", "SketchTest")
doc.recompute()
```

### 9.2 Cargar funcion

```python
from dictionary_resolver import GetDictionaryFunction

Function = GetDictionaryFunction("additive", "pad_sketch")
print(Function)
```

### 9.3 Probar recoleccion simulada

```python
from InputPrompts.ParameterCollector import ParameterCollector

Collector = ParameterCollector(DelayMs=0)
Result = Collector.CollectForFunction(
    Function,
    SimulatedFinalTexts=[
        "SketchTest enviar",
    ],
)

print(Result)
```

Resultado esperado:

```text
PromptResult(Success=True, Value={'sketch': <Sketcher::SketchObject>}, Cancelled=False, Error='')
```

La representacion exacta del objeto puede variar, pero debe resolver `SketchTest` al objeto real del documento.

### 9.4 Ejecutar

```python
if Result.Success:
    Function(**Result.Value)
```

Resultado esperado:

```text
[additive] Pad on 'SketchTest' length=10.0
```

Nota: este comando dispara `Gui.runCommand("PartDesign_Pad", 0)`, por lo que puede depender de que el contexto de FreeCAD sea compatible con PartDesign.

## Prueba 10 - Flujo real por voz con Browser

Esta prueba depende de que el comando este accesible por el `Browser` desde el contexto cargado.

Actualmente, `voice_bootstrap.py` carga `DiccionariosEnBruto` con `Browser`, y los comandos disponibles dependen de `base.py` y los `TraduceTo*.py`.

Para comandos ya conectados al `Browser`, el flujo esperado es:

```text
comando enviar
se abre prompt para parametro 1
usuario dice valor enviar
se abre prompt para parametro 2
usuario dice valor enviar
...
se ejecuta la funcion
```

Si `geometry.line/create_by_points` no aparece todavia navegable desde `Browser`, usar la prueba 8 como prueba real de diccionario hasta que ese comando sea agregado al arbol base/navegable.

## Diagnostico del modelo Vosk

Si al iniciar voz aparece:

```text
[DAV] Sin modelo Vosk para idioma 'es'
```

verificar dentro de FreeCAD:

```python
import os
print(os.environ.get("DAV_GUI_FREECAD_ROOT"))

from core.settings import MODELS_DIR, settings
from core.model_manager import get_active_model_path, verify_small_models

print(MODELS_DIR)
print(settings.language, settings.model_size)
print(verify_small_models())
print(get_active_model_path(settings.language, settings.model_size))
```

Resultado correcto:

```text
...\luigiIntegracionV1\GUIFreeCad
...\luigiIntegracionV1\GUIFreeCad\models
es small
{'en': True, 'es': True, 'pt': True}
...\luigiIntegracionV1\GUIFreeCad\models\vosk-model-small-es-0.42
```

Si apunta a `ComponentesDAV\IntegracionGUI\GUIFreeCad`, FreeCAD esta usando otra copia de la GUI.

## Orden recomendado para validar todo

Ejecutar en este orden:

```text
1. IntegerInputPrompt
2. FloatInputPrompt
3. StringInputPrompt
4. ObjectSelectionInputPrompt
5. ParameterCollector simulado
6. PromptedCommandExecutor simulado
7. PromptVoiceRouter con voz real
8. Funcion real geometry.line/create_by_points
9. Funcion real additive/pad_sketch
10. Browser con voz real cuando el comando este navegable
```

Si una prueba falla, no avanzar a la siguiente hasta corregirla.
