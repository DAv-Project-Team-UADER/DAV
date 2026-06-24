# InputPrompts

`InputPrompts` agrega una capa de ventanas emergentes para pedir datos por voz antes de ejecutar comandos DAV que necesitan parametros.

La idea central es:

```text
Browser encuentra una funcion del diccionario
PromptedCommandExecutor decide como ejecutarla
ParameterCollector consulta Validator
InputPrompts pide los datos necesarios uno por uno
DavVoiceService envia la voz al prompt activo
Validator valida los datos recolectados
La funcion se ejecuta con kwargs validados
```

## Objetivo

Antes de esta capa, DAV podia reconocer comandos por voz y ejecutar funciones, pero no tenia un flujo visual general para pedir parametros.

Este modulo resuelve eso para:

- enteros,
- decimales,
- texto,
- objetos de FreeCAD.

Cada dato se pide con una ventana emergente, se confirma por voz y se valida antes de ejecutar la funcion real.

## Archivos

### `PromptResult.py`

Define el objeto comun que devuelven todos los prompts.

Campos:

```text
Success
Value
Cancelled
Error
```

Metodos principales:

```text
PromptResult.Pending()
PromptResult.Ok(Value)
PromptResult.Cancel()
PromptResult.Fail(Error)
```

Se usa para que todos los modulos hablen el mismo idioma al reportar exito, cancelacion o error.

### `SpokenNumberParser.py`

Convierte frases habladas en numeros.

Ejemplos:

```text
uno dos enviar -> 12
cinco coma dos enviar -> 5.2
quatro ponto meia aceitar -> 4.6
```

Soporta vocabulario basico en:

- espanol,
- ingles,
- portugues.

Tambien reconoce palabras de confirmacion y cancelacion, como:

```text
enter, enviar, send, aceitar
cancelar, cancel
```

### `BaseInputPrompt.py`

Ventana base reutilizable hecha con Qt.

Responsabilidades:

- mostrar titulo,
- mostrar mensaje principal,
- mostrar estado,
- mostrar texto reconocido,
- aceptar un valor,
- cancelar,
- devolver `PromptResult`.

Los prompts concretos heredan de esta clase.

### `IntegerInputPrompt.py`

Prompt para capturar enteros.

Usa:

```text
SpokenNumberParser.ParseInteger(...)
```

Ejemplo:

```text
uno dos enviar -> 12
```

No acepta decimales. Si el usuario dice `cinco coma dos enviar`, devuelve error.

### `FloatInputPrompt.py`

Prompt para capturar decimales.

Usa:

```text
SpokenNumberParser.ParseFloat(...)
```

Ejemplo:

```text
cinco coma dos enviar -> 5.2
```

Tambien acepta enteros como floats:

```text
dos enviar -> 2.0
```

### `StringInputPrompt.py`

Prompt para capturar texto libre.

Ejemplo:

```text
linea prueba enviar -> "linea prueba"
```

Elimina la palabra final de confirmacion antes de devolver el texto.

### `ObjectSelectionInputPrompt.py`

Prompt para seleccionar objetos del documento activo de FreeCAD.

Se integra con:

```text
selection/selection.py
```

Permite avanzar entre objetos con frases como:

```text
siguiente
otro
next
seguinte
```

Y confirmar con:

```text
enviar
enter
seleccionar
select
escolher
```

Por defecto devuelve el nombre del objeto:

```text
"CylinderTest"
```

Si se instancia con `ReturnObject=True`, devuelve el objeto real de FreeCAD.

### `PromptVoiceRouter.py`

Conecta los prompts con el motor de voz existente.

No abre otro microfono.

Funciona como un registro global del prompt activo:

```text
PromptVoiceRouter.SetActivePrompt(Prompt)
PromptVoiceRouter.ClearActivePrompt(Prompt)
```

Cuando `DavVoiceService` reconoce texto en modo CAD, primero pregunta si hay un prompt activo.

Si hay prompt activo:

```text
la frase va al prompt
```

Si no hay prompt activo:

```text
la frase sigue al Browser
```

### `ParameterCollector.py`

Coordina la captura de parametros para una funcion.

Responsabilidades:

- recibir una funcion callable,
- consultar requisitos usando `Validator`,
- ignorar parametros opcionales,
- elegir el prompt adecuado segun tipo,
- recolectar valores,
- aplicar delay entre prompts,
- validar todo al final con `Validator`,
- devolver kwargs validados.

Tipos soportados:

```text
int -> IntegerInputPrompt
float -> FloatInputPrompt
str -> StringInputPrompt
object -> ObjectSelectionInputPrompt
```

Tambien permite pruebas simuladas:

```python
Collector.CollectForFunction(
    Function,
    SimulatedFinalTexts=[
        "uno dos enviar",
        "dos enviar",
    ],
)
```

Esto permite probar sin voz real y sin abrir ventanas.

### `PromptedCommandExecutor.py`

Es el adaptador entre `Browser` y `ParameterCollector`.

Se usa como callback de ejecucion:

```python
Executor = PromptedCommandExecutor()
Browser(..., on_execute=Executor)
```

Cuando recibe un `ContextEntry`:

1. verifica que sea callable,
2. usa `ParameterCollector`,
3. si no hay parametros, ejecuta directo,
4. si hay parametros, los pide y valida,
5. ejecuta la funcion con `function(**kwargs)`.

Guarda el resultado mas reciente en:

```text
Executor.LastResult
```

## Integracion con Validator

`InputPrompts` no reemplaza al validator.

Usa:

```text
validation/validator.py
```

`Validator` se encarga de:

- inspeccionar la firma de la funcion,
- detectar tipos esperados,
- convertir valores cuando corresponde,
- resolver objetos por nombre dentro del documento activo,
- rechazar datos invalidos.

`ParameterCollector` usa `Validator` en dos momentos:

```text
1. para saber que parametros pedir
2. para validar los datos recolectados
```

## Integracion con Browser

`Browser` ya tenia un punto de extension:

```python
on_execute
```

La integracion se hace en:

```text
luigiIntegracionV1/GUIFreeCad/integration/voice_bootstrap.py
```

Alli se crea:

```python
executor = PromptedCommandExecutor(Language=settings.language)
browser = Browser(dictionary_root=_dict_root, prefs=preferences, on_execute=executor)
```

Entonces `Browser` mantiene la navegacion, pero delega la ejecucion de funciones al executor.

## Integracion con DavVoiceService

`DavVoiceService` sigue siendo el unico motor de microfono.

Archivo relacionado:

```text
luigiIntegracionV1/GUIFreeCad/speech/dav_voice_service.py
```

Flujo:

```text
DavVoiceService reconoce texto
si hay prompt activo -> PromptVoiceRouter lo envia al prompt
si no hay prompt activo -> BrowserVoiceAdapter procesa el comando CAD
```

Esto evita abrir multiples `RawInputStream` y evita que los prompts compitan por el microfono.

## Flujo completo

Ejemplo con una funcion:

```python
def CreateLine(x1: float, y1: float, x2: float, y2: float):
    ...
```

Flujo:

```text
Usuario dice: linea enviar
Browser encuentra CreateLine
PromptedCommandExecutor recibe el ContextEntry
ParameterCollector consulta Validator
Validator detecta cuatro floats
FloatInputPrompt pide x1
Usuario dice: uno dos enviar
FloatInputPrompt devuelve 12.0
FloatInputPrompt pide y1
Usuario dice: dos enviar
FloatInputPrompt devuelve 2.0
FloatInputPrompt pide x2
Usuario dice: cinco enviar
FloatInputPrompt devuelve 5.0
FloatInputPrompt pide y2
Usuario dice: dos enviar
FloatInputPrompt devuelve 2.0
Validator valida kwargs
CreateLine se ejecuta con x1=12.0, y1=2.0, x2=5.0, y2=2.0
```

## Documentacion adicional

Guia de implementacion:

```text
GUIA_IMPLEMENTACION_INPUT_PROMPTS.md
```

Guia de pruebas:

```text
GUIA_PRUEBAS_INPUT_PROMPTS.md
```

## Notas importantes

- Los `.py` nuevos usan nombres en ingles y PascalCase para clases/metodos publicos.
- Los prompts no deben abrir otro microfono.
- Los prompts no reemplazan a `Validator`.
- `Browser` sigue siendo responsable de navegar comandos.
- `DavVoiceService` sigue siendo responsable de escuchar.
- `InputPrompts` solo se encarga de pedir datos, convertirlos y coordinar su validacion.
