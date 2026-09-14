# Guia de implementacion - InputPrompts

Este documento define la ruta de implementacion para agregar ventanas emergentes de entrada de datos por voz en DAV.

La implementacion debe vivir dentro de:

```text
luigiIntegracionV1/GUIFreeCad/InputPrompts/
```

Todo el codigo Python nuevo debe escribirse en ingles, usando PascalCase para nombres publicos cuando corresponda, y cada archivo `.py` debe incluir el header de licencia GPL que ya usan otros archivos del proyecto.

## Objetivo

Agregar una capa de abstraccion para pedir parametros al usuario antes de ejecutar una funcion del diccionario DAV.

El flujo buscado es:

```text
El usuario dice un comando
Browser encuentra la funcion en el diccionario
Validator detecta que datos necesita la funcion
InputPrompts pide esos datos uno por uno mediante ventanas emergentes
Cada dato se captura por voz y se valida
Cuando estan todos los datos, se ejecuta la funcion
```

Ejemplo:

```text
Usuario: linea enviar
DAV pide x1
Usuario: uno dos enter
DAV captura 12
DAV pide y1
Usuario: dos enter
DAV captura 2
DAV pide x2
Usuario: cinco enter
DAV captura 5
DAV pide y2
Usuario: dos enter
DAV captura 2
DAV ejecuta la linea desde (12, 2) hasta (5, 2)
```

## Estructura propuesta

Crear los siguientes archivos:

```text
InputPrompts/
├── __init__.py
├── PromptResult.py
├── SpokenNumberParser.py
├── BaseInputPrompt.py
├── IntegerInputPrompt.py
├── FloatInputPrompt.py
├── StringInputPrompt.py
├── ObjectSelectionInputPrompt.py
├── ParameterCollector.py
└── PromptedCommandExecutor.py
```

Responsabilidades:

- `PromptResult.py`: representa el resultado de una captura.
- `SpokenNumberParser.py`: convierte numeros hablados a `int` o `float`.
- `BaseInputPrompt.py`: ventana base reutilizable.
- `IntegerInputPrompt.py`: ventana para pedir enteros.
- `FloatInputPrompt.py`: ventana para pedir decimales.
- `StringInputPrompt.py`: ventana para pedir texto.
- `ObjectSelectionInputPrompt.py`: ventana para pedir seleccion de objetos.
- `ParameterCollector.py`: coordina la captura de todos los parametros de una funcion.
- `PromptedCommandExecutor.py`: ejecuta funciones del diccionario usando `ParameterCollector`.

## Paso 1 - Crear el resultado comun

Archivo:

```text
InputPrompts/PromptResult.py
```

Debe definir una estructura comun para devolver resultados desde cualquier prompt.

Campos sugeridos:

```text
Success: bool
Value: object | None
Cancelled: bool
Error: str
```

Uso esperado:

```text
Success=True, Value=12, Cancelled=False, Error=""
Success=False, Value=None, Cancelled=True, Error=""
Success=False, Value=None, Cancelled=False, Error="Invalid integer"
```

Prueba recomendada:

```powershell
cd luigiIntegracionV1\GUIFreeCad
python -c "from InputPrompts.PromptResult import PromptResult; print(PromptResult(True, 12, False, ''))"
```

## Paso 2 - Implementar parser de numeros hablados

Archivo:

```text
InputPrompts/SpokenNumberParser.py
```

Debe convertir frases como:

```text
uno dos
```

en:

```text
12
```

Debe soportar al menos:

```text
cero, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve
```

Tambien debe soportar variantes para decimales:

```text
uno dos coma cinco
uno dos punto cinco
```

Resultados esperados:

```text
ParseInteger("uno dos") -> 12
ParseFloat("uno dos coma cinco") -> 12.5
ParseFloat("cinco punto dos") -> 5.2
```

Prueba recomendada fuera de FreeCAD:

```powershell
cd luigiIntegracionV1\GUIFreeCad
python -c "from InputPrompts.SpokenNumberParser import SpokenNumberParser; print(SpokenNumberParser.ParseInteger('uno dos'))"
python -c "from InputPrompts.SpokenNumberParser import SpokenNumberParser; print(SpokenNumberParser.ParseFloat('cinco coma dos'))"
```

## Paso 3 - Crear la ventana base

Archivo:

```text
InputPrompts/BaseInputPrompt.py
```

Debe implementar una ventana PySide6 reutilizable.

Responsabilidades:

- Mostrar titulo.
- Mostrar mensaje principal.
- Mostrar estado de escucha.
- Mostrar texto reconocido si corresponde.
- Permitir confirmar o cancelar.
- Cerrar de forma controlada.

No debe saber si esta pidiendo `int`, `float`, `str` u objeto. Solo debe ser la base visual.

Prueba en FreeCAD:

1. Abrir FreeCAD con DAV:

```powershell
.\iniciar_dav.ps1
```

2. En la consola Python de FreeCAD:

```python
import sys
sys.path.insert(0, r"D:\Facultad\PET DAV\Fork\DAV\luigiIntegracionV1\GUIFreeCad")

from InputPrompts.BaseInputPrompt import BaseInputPrompt
Prompt = BaseInputPrompt("DAV Input", "Deci un valor")
Prompt.Show()
```

Resultado esperado:

```text
La ventana aparece dentro de FreeCAD sin bloquear ni romper la interfaz.
```

## Paso 4 - Crear prompts por tipo

Archivos:

```text
InputPrompts/IntegerInputPrompt.py
InputPrompts/FloatInputPrompt.py
InputPrompts/StringInputPrompt.py
InputPrompts/ObjectSelectionInputPrompt.py
```

Cada prompt debe usar `BaseInputPrompt`.

### IntegerInputPrompt

Debe:

- Mostrar un mensaje para pedir un entero.
- Capturar numeros hablados.
- Confirmar con `enter` o `enviar`.
- Devolver un `int`.

Ejemplo:

```text
Usuario dice: uno dos enter
Resultado: 12
```

### FloatInputPrompt

Debe:

- Mostrar un mensaje para pedir un decimal.
- Soportar `coma` y `punto`.
- Confirmar con `enter` o `enviar`.
- Devolver un `float`.

Ejemplo:

```text
Usuario dice: uno dos coma cinco enter
Resultado: 12.5
```

### StringInputPrompt

Debe:

- Mostrar un mensaje para pedir texto.
- Capturar texto libre.
- Confirmar con `enter` o `enviar`.
- Devolver un `str`.

### ObjectSelectionInputPrompt

Debe:

- Guiar al usuario para seleccionar objetos.
- Integrarse con la clase `ObjectSelection` existente en `selection/object_selection.py`.
- Devolver el objeto seleccionado o el nombre del objeto, segun lo que necesite el flujo de validacion.

Prueba recomendada en FreeCAD:

```python
from InputPrompts.IntegerInputPrompt import IntegerInputPrompt
Prompt = IntegerInputPrompt("Integer", "Deci un numero entero")
Result = Prompt.RequestValue()
print(Result)
```

Al principio se recomienda permitir una prueba simulada sin voz real:

```python
Prompt.ProcessFinalText("uno dos enter")
```

Resultado esperado:

```text
PromptResult(Success=True, Value=12, Cancelled=False, Error="")
```

## Paso 5 - Crear ParameterCollector

Archivo:

```text
InputPrompts/ParameterCollector.py
```

Este modulo coordina todo el pedido de parametros.

Responsabilidades:

- Recibir una funcion del diccionario.
- Consultar al `Validator` que parametros necesita.
- Detectar el tipo de cada parametro.
- Abrir el prompt correspondiente.
- Capturar el valor.
- Validar el valor.
- Guardar los valores recolectados.
- Devolver argumentos listos para ejecutar la funcion.

Flujo interno:

```text
Function
Validator analiza la firma
ParameterCollector detecta parametros
Para cada parametro:
  abre prompt segun tipo
  captura valor por voz
  valida valor
  guarda valor
Devuelve kwargs
```

Prueba con funcion dummy en FreeCAD:

```python
def CreateLine(x1: float, y1: float, x2: float, y2: float):
    print("Line:", x1, y1, x2, y2)

from InputPrompts.ParameterCollector import ParameterCollector
Collector = ParameterCollector()
Result = Collector.CollectForFunction(CreateLine)
print(Result)
```

Resultado esperado:

```text
Se abren cuatro prompts, uno por cada parametro.
Al final se obtiene algo equivalente a:
{"x1": 12.0, "y1": 2.0, "x2": 5.0, "y2": 2.0}
```

## Paso 6 - Integrar con Validator

El `Validator` esta en:

```text
validation/validator.py
```

No mover la logica del validator a `InputPrompts`.

`InputPrompts` debe usar `Validator` como dependencia para:

- Saber que datos necesita la funcion.
- Validar los valores capturados.
- Evitar ejecutar funciones con datos incompletos o invalidos.

Prueba en FreeCAD:

```python
import sys
sys.path.insert(0, r"D:\Facultad\PET DAV\Fork\DAV\validation")

from validator import Validator

def TestCommand(Value: int):
    print(Value)

Validator().GetRequirements("es", TestCommand)
```

Resultado esperado:

```text
Dato1: se espera un entero
```

Luego probar que `ParameterCollector` use esa informacion para abrir `IntegerInputPrompt`.

## Paso 7 - Crear PromptedCommandExecutor

Archivo:

```text
InputPrompts/PromptedCommandExecutor.py
```

Este modulo debe recibir un `ContextEntry` del `Browser` y decidir como ejecutarlo.

Reglas:

- Si el comando no necesita parametros, ejecutarlo directamente.
- Si necesita parametros, llamar a `ParameterCollector`.
- Si el usuario cancela, no ejecutar.
- Si falta algun dato o falla la validacion, mostrar error y no ejecutar.
- Si todo esta correcto, ejecutar la funcion con los argumentos recolectados.

Este modulo evita ensuciar `Browser` con logica de ventanas.

## Paso 8 - Integrar con Browser

Archivo relacionado:

```text
luigiIntegracionV1/GUIFreeCad/navigation/browser.py
```

`Browser` ya acepta un callback:

```text
on_execute
```

La integracion recomendada es pasarle un ejecutor externo:

```text
Browser(..., on_execute=PromptedCommandExecutor.Execute)
```

Asi, cuando `Browser` encuentra una funcion, no la ejecuta directamente, sino que delega la ejecucion al nuevo modulo.

Prueba en FreeCAD:

1. Abrir DAV.
2. Activar voz DAV.
3. Probar un comando sin parametros:

```text
preferencias enviar
```

Resultado esperado:

```text
Debe seguir funcionando igual que antes.
```

4. Probar un comando dummy con parametros.

Resultado esperado:

```text
Browser encuentra el comando.
PromptedCommandExecutor detecta parametros.
ParameterCollector abre prompts.
La funcion se ejecuta despues de capturar todos los datos.
```

## Paso 9 - Integrar con el motor de voz existente

Archivos relacionados:

```text
luigiIntegracionV1/GUIFreeCad/speech/dav_voice_service.py
luigiIntegracionV1/GUIFreeCad/integration/browser_voice_adapter.py
```

Regla importante:

```text
No crear otro RawInputStream ni otro microfono dentro de los prompts.
```

El proyecto ya tiene un servicio de microfono unico: `DavVoiceService`.

Los prompts deben recibir frases finales desde el servicio existente, o el sistema debe entrar en un modo donde las frases reconocidas se enruten al prompt activo.

Orden recomendado:

1. Probar prompts con texto simulado.
2. Probar prompts recibiendo frases finales reales.
3. Probar flujo completo desde comando de voz hasta ejecucion.

## Paso 10 - Delay entre prompts

La tarea menciona un delay de 30 ms entre ventanas.

Implementarlo en `ParameterCollector`, no en cada prompt.

En Qt/FreeCAD usar:

```python
QTimer.singleShot(30, OpenNextPrompt)
```

Evitar:

```python
time.sleep(0.03)
```

Motivo:

```text
time.sleep puede congelar la interfaz grafica de FreeCAD.
QTimer respeta el event loop de Qt.
```

## Paso 11 - Prueba completa en FreeCAD

Caso de prueba sugerido:

```python
def CreateLine(x1: float, y1: float, x2: float, y2: float):
    print("Line created from", (x1, y1), "to", (x2, y2))
```

Flujo esperado:

```text
Usuario: line enviar

Prompt 1:
Deci el valor para x1
Usuario: uno dos enter
Captura: 12

Prompt 2:
Deci el valor para y1
Usuario: dos enter
Captura: 2

Prompt 3:
Deci el valor para x2
Usuario: cinco enter
Captura: 5

Prompt 4:
Deci el valor para y2
Usuario: dos enter
Captura: 2

Resultado:
Line created from (12, 2) to (5, 2)
```

## Orden recomendado de desarrollo

Implementar en este orden:

```text
1. PromptResult.py
2. SpokenNumberParser.py
3. BaseInputPrompt.py
4. IntegerInputPrompt.py
5. FloatInputPrompt.py
6. StringInputPrompt.py
7. ObjectSelectionInputPrompt.py
8. ParameterCollector.py
9. Integracion con Validator
10. PromptedCommandExecutor.py
11. Integracion con Browser usando on_execute
12. Integracion con DavVoiceService
13. Prueba completa en FreeCAD
14. Prueba con comandos reales de DiccionariosEnBruto
```

## Criterios de aceptacion

La tarea puede considerarse completa cuando:

- Existe una ventana para pedir enteros.
- Existe una ventana para pedir floats.
- Existe una ventana para pedir strings.
- Existe una ventana para pedir seleccion de objetos.
- Los prompts usan la escucha existente del proyecto.
- No se crea un segundo microfono.
- `Validator` define que datos se necesitan.
- `ParameterCollector` pide los datos uno por uno.
- Si falta un dato, se informa error y no se ejecuta la funcion.
- Si el usuario cancela, no se ejecuta la funcion.
- Si todos los datos son validos, se ejecuta la funcion del diccionario.
- El flujo funciona dentro de FreeCAD.

## Nota de diseno

`InputPrompts` debe ser una capa de interfaz y recoleccion de datos.

No debe reemplazar:

- `Validator`, porque la validacion ya tiene su propio modulo.
- `Browser`, porque la navegacion ya tiene su propio modulo.
- `DavVoiceService`, porque el microfono unico ya existe.
- `ObjectSelection`, porque la seleccion de objetos ya tiene una clase dedicada.

La idea es conectar esas piezas sin duplicarlas.
