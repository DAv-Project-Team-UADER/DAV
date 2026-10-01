# `PruebaIntegracion` Documentation

## 1. Purpose of the module

`PruebaIntegracion` is an integration implementation for the DAV project focused on voice navigation and on running actions from a hierarchical context structure. Its purpose is to join three parts that appeared separate or incomplete in the repository:

1. Voice capture and filtering.
2. Searching for commands within a tree of contexts.
3. Safe execution of functions with parameter validation.

The folder was conceived as a self-contained workspace to turn into code the idea described in `IDEAS/IDEA DE DAVCORE IMPLEMENTATION/EXPLICACION.txt`, without interfering with the other variants in the repository.

## 2. Relationship with the project

The concrete usefulness of this section for the project is the following:

- It allows tools to be defined per context, rather than as a flat list of commands.
- It makes it possible to translate spoken words into real function or subcontext names.
- It centralizes parameter validation before running an action.
- It separates the voice-recognition logic from the business logic.
- It leaves a clear base to grow from a local demo to a real integration with `VoskModel` and dynamic folders in `dic/`.

In functional terms, `PruebaIntegracion` represents the conceptual core of the future `DAVCore`.

## 3. Developed structure

The main modules developed within `PruebaIntegracion` are:

- `core/ParamSpec.py`
- `core/EnvoltorioFuncion.py`
- `core/NodoContexto.py`
- `core/Navegador.py`
- `core/Comando.py`
- `core/ExploradorVoz.py`
- `core/CargadorConTraducciones.py`
- `main.py`

In addition, the flow uses:

- `modelo/VoskModel.py` for real voice recognition.
- `dic/` as a folder of dynamically loadable modules.
- `idiomas/` as a space prepared for per-language translations.

## 4. Responsibility map

### 4.1 `ParamSpec`

File: [PruebaIntegracion/core/ParamSpec.py](../../prototipos/PruebaIntegracion/core/ParamSpec.py)

Its task is to describe what a function parameter must look like.

#### What it solves

Without this class, each function would have its own manual validation. With `ParamSpec`, validation is declared in a uniform and reusable way.

#### Main attributes

- `nombre`: logical name of the parameter.
- `tipo`: expected type, for example `int`, `float`, `str` or a tuple of types.
- `requerido`: indicates whether the argument is mandatory.
- `longitud_maxima`: limit for text strings.
- `valores_permitidos`: closed set of valid values.

#### Key method

- `validar(valor, nombre_argumento=None)`: checks the received value and raises a clear error if it does not comply.

#### Usefulness in the project

`ParamSpec` is the basis of input validation. It gives the system a declarative way of saying: "this function expects a mandatory float" or "this text cannot exceed a certain length".

### 4.2 `EnvoltorioFuncion`

File: [PruebaIntegracion/core/EnvoltorioFuncion.py](../../prototipos/PruebaIntegracion/core/EnvoltorioFuncion.py)

Wraps a real function to inspect its signature, validate arguments and run it in a controlled way.

#### What it solves

The project needs an intermediate layer between the spoken command and the concrete function. That layer has to know:

- which parameters the function expects,
- in what order,
- whether it needs `context_keys`,
- and how to validate before running.

#### How it works

1. Stores the original function.
2. Reads its signature with `inspect.signature`.
3. Gets the list of `ParamSpec` from the `_param_specs` attribute or from an explicit list.
4. Verifies that each `ParamSpec` really exists in the signature.
5. In `ejecutar()` it does `bind_partial()` on the signature.
6. If the function accepts `context_keys`, it injects them automatically.
7. Validates the arguments with each `ParamSpec`.
8. If everything is correct, it invokes the real function.

#### Key methods

- `obtener_orden_parametros()`: returns the original order of the signature.
- `ejecutar(*args, context_keys=None, **kwargs)`: validates and invokes.

#### Usefulness in the project

This module turns an ordinary function into a safe tool for the voice system. It is the piece that makes it possible to invoke actions without blindly trusting what was heard.

### 4.3 `NodoContexto`

File: [PruebaIntegracion/core/NodoContexto.py](../../prototipos/PruebaIntegracion/core/NodoContexto.py)

Represents a navigation level within the system. It can contain functions, subcontexts and translations.

#### What it solves

The application does not work with a flat menu, but with a hierarchy. `NodoContexto` models that tree.

#### Internal structure

- `elementos`: dictionary from real names to `EnvoltorioFuncion` or `NodoContexto`.
- `traducciones`: dictionary from spoken word to real name.
- `parent`: reference to the parent node.

#### Key methods

- `agregar_funcion(clave, envoltorio)`: registers a function.
- `agregar_subcontexto(clave, nodo)`: registers a subcontext and connects the parent.
- `agregar_traduccion(palabra_hablada, nombre_real)`: adds a local synonym.
- `obtener_nombre_real(palabra_hablada)`: resolves the translation in the current node.
- `obtener_todas_las_llaves()`: walks the local real keys.
- `obtener_hijo(clave)`: returns a subcontext if it exists.

#### Usefulness in the project

`NodoContexto` allows the spoken vocabulary to be separated from the real internal structure. This is useful for supporting several languages, aliases or more natural words for the user.

### 4.4 `Navegador`

File: [PruebaIntegracion/core/Navegador.py](../../prototipos/PruebaIntegracion/core/Navegador.py)

It is the orchestrator of the context tree. It keeps the current context and resolves upward searches.

#### What it solves

When the user speaks from a context, the application must know whether the word corresponds to a local function or to something defined in a parent. `Navegador` concentrates that logic.

#### Key methods

- `establecer_contexto(nodo)`: changes the current context.
- `navegar(ruta)`: descends along a path such as `Dibujo-Geometria-Circulos`.
- `buscar_funcion_ascendente(nombre_real)`: searches from the current context up to the root.
- `llamar(nombre_real, *args, context_keys=None, **kwargs)`: finds the function and runs it.

#### Actual flow

When `llamar()` finds the function, it updates `contexto_actual` to the node where it was found. This allows navigation and execution to work on the same tree without duplicating state.

#### Usefulness in the project

`Navegador` is the central decision point for resolving real names, going up the tree and running actions without losing the user's position.

### 4.5 `Command`

File: [PruebaIntegracion/core/Comando.py](../../prototipos/PruebaIntegracion/core/Comando.py)

It is the voice input adapter. It receives phrases from the voice model and filters only the words that are allowed in the active vocabulary.

#### What it solves

The system's intention is not to transcribe anything, but to recognize only tokens that are useful for the current state.

#### Features

- Has predefined vectors through `VECTORS`.
- Normalizes text by removing accent marks and lowercasing.
- Converts spoken digits such as `uno`, `dos`, `tres` (one, two, three) into numbers.
- Detects special commands such as `cancelar`, `enter` and `enviar` (cancel, enter, send).
- Supports both use by index and by a custom list of tokens.

#### Key method

- `exclusive_listen(vector)`: listens until a valid selection or a cancellation is obtained.

#### Usefulness in the project

`Command` acts as a smart filter between the audio and the system logic. Without this layer, the explorer would have to interpret noisy or irrelevant phrases.

### 4.6 `ExploradorVoz`

File: [PruebaIntegracion/core/ExploradorVoz.py](../../prototipos/PruebaIntegracion/core/ExploradorVoz.py)

It is the main coordinator of the behavior. It handles navigation, function selection and parameter collection.

#### What it solves

It connects everything else in a simple state machine:

- navigation mode,
- parameters mode,
- execution.

#### Internal attributes

- `voice_model`: audio source or test model.
- `navegador`: instance of `Navegador`.
- `command`: instance of `Command`.
- `modo_parametros`: indicates whether a selected function is being read.
- `funcion_pendiente`: wrapped function that still has to be run.
- `parametros_recolectados`: list of captured values.

#### Key methods

- `_obtener_nombre_real_ascendente(palabra)`: resolves translations upward in the hierarchy.
- `_vocabulario_navegacion()`: builds the active vocabulary for navigation.
- `_parse_number(phrase)`: interprets spoken numbers in a simple way.
- `iniciar_parametros(envoltorio)`: switches to parameters mode.
- `procesar_parametros()`: collects values and calls the function.
- `bucle_comando(max_iterations=None)`: main loop.

#### Integration flow

1. Gets the allowed vocabulary according to the current context.
2. Calls `Command.exclusive_listen(...)`.
3. Translates the detected word to a real name.
4. Looks up whether that name corresponds to a function or a subcontext.
5. If it is a function, it enters parameters mode.
6. When capture ends, it runs with `Navegador.llamar()`.

#### Usefulness in the project

It is the module that turns the data infrastructure into real interactive behavior.

### 4.7 `CargadorConTraducciones`

File: [PruebaIntegracion/core/CargadorConTraducciones.py](../../prototipos/PruebaIntegracion/core/CargadorConTraducciones.py)

Dynamic loading of modules from `dic/` and construction of the context tree.

#### What it solves

It avoids having to write the tool tree by hand inside the main code. Instead, the structure can be maintained as loose files inside a folder.

#### Convention used

- Each folder represents a `NodoContexto`.
- Each `TraduceTo*.py` file can expose a `TRADUCCIONES` dictionary.
- Each remaining `.py` file is inspected looking for functions with `_param_specs`.

#### Internal flow

1. Walks the `dic/` folder.
2. Creates a node for each subdirectory.
3. Imports modules with `importlib.util.spec_from_file_location`.
4. If it finds `TRADUCCIONES`, it registers them in the node.
5. If it finds valid functions, it wraps them with `EnvoltorioFuncion`.
6. Returns a dictionary of roots ready to hang from the main node.

#### Usefulness in the project

It makes it possible to scale the system without modifying the core every time a new tool is added.

### 4.8 Real example of `dic/`

So that the loader has functional content, `PruebaIntegracion/dic/` can already use a minimal structure like this:

```text
PruebaIntegracion/dic/
	Demo/
		crear_punto.py
		TraduceToEs.py
```

In that example:

- `crear_punto.py` defines a function `crear_punto(valor, context_keys=None)`.
- The function exposes `_param_specs` with `ParamSpec("valor", float)`.
- `TraduceToEs.py` declares `TRADUCCIONES = {"demo": "Demo", "crear punto": "crear_punto"}`.

That allows the loader to:

1. Create a `NodoContexto` called `Demo`.
2. Register the spoken translation `demo -> Demo`.
3. Register the spoken translation `crear punto -> crear_punto`.
4. Link the real function with `EnvoltorioFuncion`.
5. Allow `ExploradorVoz` to navigate to the context and run the function.

This case serves as a template for adding new real tools without touching the core.

## 5. Integration between modules

The relationship between components is as follows:

- `ExploradorVoz` contains a `Command` and a `Navegador`.
- `Command` uses a `voice_model` to listen.
- `Navegador` manages `NodoContexto`.
- `NodoContexto` contains `EnvoltorioFuncion` and other `NodoContexto`.
- `EnvoltorioFuncion` validates with `ParamSpec`.
- `CargadorConTraducciones` builds the initial tree.

In other words: the loader creates the structure, the navigator walks it, the command filters the voice and the explorer decides what to run.

## 6. Current startup flow

File: [PruebaIntegracion/main.py](../../prototipos/PruebaIntegracion/main.py)

The current `main` replaces the rigid startup with a more flexible flow.

### What it does

- Reads command-line arguments.
- Tries to load the tree from `dic/`.
- If there is no content, it creates a minimal demo with an example function.
- Creates the `Navegador`.
- Instantiates the real voice model or a simulated demo model.
- Launches `ExploradorVoz.bucle_comando()`.

### Demo mode

Demo mode is used to test the flow without a microphone or an installed Vosk model. It is especially useful for validating integration, navigation and basic execution.

## 7. Usage example

### Demo mode

```bash
python -m PruebaIntegracion.main --demo --max-iter 2
```

That mode uses a simulated model that returns a sequence of phrases and lets you confirm that the tree, the translation and the execution work.

### Real mode

```bash
python -m PruebaIntegracion.main --modelo MODELO\vosk-model-small-es-0.42
```

In that case `VoskModel` is used and the input depends on the microphone and on the dependencies being installed.

## 8. Conceptual example code

The central idea of the system is this sequence:

```python
raiz = construir_estructura_desde_diccionario()
navegador = Navegador(raiz)
explorador = ExploradorVoz(modelo_voz, navegador)
explorador.bucle_comando()
```

And inside the explorer:

```python
token = command.exclusive_listen(vocabulario)
nombre_real = _obtener_nombre_real_ascendente(token)
encontrado = navegador.buscar_funcion_ascendente(nombre_real)
```

That small cycle summarizes the whole architecture: listen, translate, search and run.

## 9. Current state and limitations

### Current state

- The main architecture is implemented.
- Startup has a functional demo mode.
- The loader can already walk `dic/` and prepare a tree.
- Upward search and basic execution are tested.

### Current limitations

- `dic/` is still empty, so the system uses a demo fallback if it does not find real modules.
- The numeric interpretation of `ExploradorVoz` is simple and can be extended.
- `Command` and `ExploradorVoz` are prepared to grow, but the final semantics depend on the real modules that are added in `dic/`.

## 10. Conclusion

`PruebaIntegracion` concentrates the practical implementation of the map described in the idea documents. Its value for the project is that it is no longer just a conceptual explanation: there is now an executable base that shows how to translate voice navigation into a tree of contexts, how to validate parameters before running actions and how to extend the system without rewriting the core.
