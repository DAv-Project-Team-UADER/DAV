# Documentación de `PruebaIntegracion`

## 1. Propósito del módulo

`PruebaIntegracion` es una implementación de integración para el proyecto DAV enfocada en la navegación por voz y la ejecución de acciones desde una estructura jerárquica de contexto. Su función es unir tres partes que en el repositorio aparecían separadas o incompletas:

1. Captura y filtrado de voz.
2. Búsqueda de comandos dentro de un árbol de contextos.
3. Ejecución segura de funciones con validación de parámetros.

La carpeta fue pensada como un espacio de trabajo autocontenido para llevar a código la idea descrita en `IDEAS/IDEA DE DAVCORE IMPLEMENTATION/EXPLICACION.txt`, sin interferir con las otras variantes del repositorio.

## 2. Relación con el proyecto

La utilidad concreta de esta sección para el proyecto es la siguiente:

- Permite definir herramientas por contexto, no como una lista plana de comandos.
- Hace posible traducir palabras habladas a nombres reales de funciones o subcontextos.
- Centraliza la validación de parámetros antes de ejecutar una acción.
- Separa la lógica de reconocimiento de voz de la lógica de negocio.
- Deja una base clara para crecer desde una demo local hasta una integración real con `VoskModel` y carpetas dinámicas en `dic/`.

En términos funcionales, `PruebaIntegracion` representa el núcleo conceptual del futuro `DAVCore`.

## 3. Estructura desarrollada

Los módulos principales desarrollados dentro de `PruebaIntegracion` son:

- `core/ParamSpec.py`
- `core/EnvoltorioFuncion.py`
- `core/NodoContexto.py`
- `core/Navegador.py`
- `core/Comando.py`
- `core/ExploradorVoz.py`
- `core/CargadorConTraducciones.py`
- `main.py`

Además, el flujo usa:

- `modelo/VoskModel.py` para el reconocimiento de voz real.
- `dic/` como carpeta de módulos cargables dinámicamente.
- `idiomas/` como espacio preparado para traducciones por idioma.

## 4. Mapa de responsabilidades

### 4.1 `ParamSpec`

Archivo: [PruebaIntegracion/core/ParamSpec.py](core/ParamSpec.py)

Su tarea es describir cómo debe ser un parámetro de una función.

#### Qué resuelve

Sin esta clase, cada función tendría su propia validación manual. Con `ParamSpec`, la validación queda declarada de forma uniforme y reutilizable.

#### Atributos principales

- `nombre`: nombre lógico del parámetro.
- `tipo`: tipo esperado, por ejemplo `int`, `float`, `str` o una tupla de tipos.
- `requerido`: indica si el argumento es obligatorio.
- `longitud_maxima`: límite para cadenas de texto.
- `valores_permitidos`: conjunto cerrado de valores válidos.

#### Método clave

- `validar(valor, nombre_argumento=None)`: verifica el valor recibido y lanza un error claro si no cumple.

#### Utilidad en el proyecto

`ParamSpec` es la base de la validación de entrada. Le da al sistema una forma declarativa de decir: "esta función espera un float obligatorio" o "este texto no puede superar cierta longitud".

### 4.2 `EnvoltorioFuncion`

Archivo: [PruebaIntegracion/core/EnvoltorioFuncion.py](core/FunctionWrapper.py)

Envuelve una función real para inspeccionar su firma, validar argumentos y ejecutarla de forma controlada.

#### Qué resuelve

El proyecto necesita una capa intermedia entre el comando hablado y la función concreta. Esa capa tiene que saber:

- qué parámetros espera la función,
- en qué orden,
- si necesita `context_keys`,
- y cómo validar antes de ejecutar.

#### Cómo funciona

1. Guarda la función original.
2. Lee su firma con `inspect.signature`.
3. Obtiene la lista de `ParamSpec` desde el atributo `_param_specs` o desde una lista explícita.
4. Verifica que cada `ParamSpec` realmente exista en la firma.
5. En `ejecutar()` hace `bind_partial()` sobre la firma.
6. Si la función acepta `context_keys`, los inyecta automáticamente.
7. Valida los argumentos con cada `ParamSpec`.
8. Si todo es correcto, invoca la función real.

#### Método clave

- `obtener_orden_parametros()`: devuelve el orden original de la firma.
- `ejecutar(*args, context_keys=None, **kwargs)`: valida e invoca.

#### Utilidad en el proyecto

Este módulo convierte una función común en una herramienta segura para el sistema de voz. Es la pieza que hace posible invocar acciones sin confiar ciegamente en lo que se escuchó.

### 4.3 `NodoContexto`

Archivo: [PruebaIntegracion/core/NodoContexto.py](core/ContextNode.py)

Representa un nivel de navegación dentro del sistema. Puede contener funciones, subcontextos y traducciones.

#### Qué resuelve

La aplicación no trabaja con un menú plano, sino con una jerarquía. `NodoContexto` modela ese árbol.

#### Estructura interna

- `elementos`: diccionario de nombres reales hacia `EnvoltorioFuncion` o `NodoContexto`.
- `traducciones`: diccionario de palabra hablada hacia nombre real.
- `parent`: referencia al nodo padre.

#### Métodos clave

- `agregar_funcion(clave, envoltorio)`: registra una función.
- `agregar_subcontexto(clave, nodo)`: registra un subcontexto y conecta el padre.
- `agregar_traduccion(palabra_hablada, nombre_real)`: agrega un sinónimo local.
- `obtener_nombre_real(palabra_hablada)`: resuelve la traducción en el nodo actual.
- `obtener_todas_las_llaves()`: recorre las claves reales locales.
- `obtener_hijo(clave)`: devuelve un subcontexto si existe.

#### Utilidad en el proyecto

`NodoContexto` permite separar el vocabulario hablado de la estructura interna real. Esto es útil para soportar varios idiomas, alias o palabras más naturales para el usuario.

### 4.4 `Navegador`

Archivo: [PruebaIntegracion/core/Navegador.py](core/Navigator.py)

Es el orquestador del árbol de contextos. Mantiene el contexto actual y resuelve búsquedas ascendentes.

#### Qué resuelve

Cuando el usuario habla desde un contexto, la aplicación debe saber si la palabra corresponde a una función local o a algo definido en un padre. `Navegador` concentra esa lógica.

#### Método clave

- `establecer_contexto(nodo)`: cambia el contexto actual.
- `navegar(ruta)`: baja por una ruta como `Dibujo-Geometria-Circulos`.
- `buscar_funcion_ascendente(nombre_real)`: busca desde el contexto actual hacia la raíz.
- `llamar(nombre_real, *args, context_keys=None, **kwargs)`: busca la función y la ejecuta.

#### Flujo real

Cuando `llamar()` encuentra la función, actualiza `contexto_actual` al nodo donde se halló. Eso permite que la navegación y la ejecución trabajen sobre el mismo árbol sin duplicar estado.

#### Utilidad en el proyecto

`Navegador` es el punto central de decisión para resolver nombres reales, subir por el árbol y ejecutar acciones sin perder la posición del usuario.

### 4.5 `Command`

Archivo: [PruebaIntegracion/core/Comando.py](core/Command.py)

Es el adaptador de entrada por voz. Recibe frases desde el modelo de voz y filtra solo las palabras que están permitidas en el vocabulario activo.

#### Qué resuelve

La intención del sistema no es transcribir cualquier cosa, sino reconocer solo tokens útiles para el estado actual.

#### Características

- Tiene vectores predefinidos mediante `VECTORS`.
- Normaliza texto quitando tildes y pasando a minúsculas.
- Convierte dígitos hablados como `uno`, `dos`, `tres` en números.
- Detecta comandos especiales como `cancelar`, `enter` y `enviar`.
- Soporta tanto uso por índice como por lista personalizada de tokens.

#### Método clave

- `exclusive_listen(vector)`: escucha hasta obtener una selección válida o una cancelación.

#### Utilidad en el proyecto

`Command` hace de filtro inteligente entre el audio y la lógica del sistema. Sin esta capa, el explorador tendría que interpretar frases ruidosas o irrelevantes.

### 4.6 `ExploradorVoz`

Archivo: [PruebaIntegracion/core/ExploradorVoz.py](core/VoiceExplorer.py)

Es el coordinador principal del comportamiento. Maneja navegación, selección de funciones y recolección de parámetros.

#### Qué resuelve

Conecta todo lo demás en una máquina de estados simple:

- modo navegación,
- modo parámetros,
- ejecución.

#### Atributos internos

- `voice_model`: fuente de audio o modelo de prueba.
- `navegador`: instancia de `Navegador`.
- `command`: instancia de `Command`.
- `modo_parametros`: indica si se está leyendo una función seleccionada.
- `funcion_pendiente`: función envuelta que falta ejecutar.
- `parametros_recolectados`: lista de valores capturados.

#### Métodos clave

- `_obtener_nombre_real_ascendente(palabra)`: resuelve traducciones hacia arriba en la jerarquía.
- `_vocabulario_navegacion()`: arma el vocabulario activo para navegación.
- `_parse_number(phrase)`: interpreta números hablados de forma simple.
- `iniciar_parametros(envoltorio)`: cambia a modo parámetros.
- `procesar_parametros()`: recolecta valores y llama a la función.
- `bucle_comando(max_iterations=None)`: loop principal.

#### Flujo de integración

1. Obtiene el vocabulario permitido según el contexto actual.
2. Llama a `Command.exclusive_listen(...)`.
3. Traduce la palabra detectada a nombre real.
4. Busca si ese nombre corresponde a función o subcontexto.
5. Si es función, entra en modo parámetros.
6. Si termina la captura, ejecuta con `Navegador.llamar()`.

#### Utilidad en el proyecto

Es el módulo que transforma la infraestructura de datos en comportamiento interactivo real.

### 4.7 `CargadorConTraducciones`

Archivo: [PruebaIntegracion/core/CargadorConTraducciones.py](core/LoaderWithTranslations.py)

Carga dinámica de módulos desde `dic/` y construcción del árbol de contextos.

#### Qué resuelve

Evita que el árbol de herramientas tenga que escribirse a mano dentro del código principal. En su lugar, la estructura se puede mantener como archivos sueltos dentro de una carpeta.

#### Convención usada

- Cada carpeta representa un `NodoContexto`.
- Cada archivo `TraduceTo*.py` puede exponer un diccionario `TRADUCCIONES`.
- Cada archivo `.py` restante se inspecciona en busca de funciones con `_param_specs`.

#### Flujo interno

1. Recorre la carpeta `dic/`.
2. Crea un nodo por cada subdirectorio.
3. Importa módulos con `importlib.util.spec_from_file_location`.
4. Si encuentra `TRADUCCIONES`, las registra en el nodo.
5. Si encuentra funciones válidas, las envuelve con `EnvoltorioFuncion`.
6. Devuelve un diccionario de raíces listo para colgar del nodo principal.

#### Utilidad en el proyecto

Hace posible escalar el sistema sin modificar el núcleo cada vez que se agrega una herramienta nueva.

### 4.8 Ejemplo real de `dic/`

Para que el cargador tenga contenido funcional, `PruebaIntegracion/dic/` ya puede usar una estructura mínima como esta:

```text
PruebaIntegracion/dic/
	Demo/
		crear_punto.py
		TraduceToEs.py
```

En ese ejemplo:

- `crear_punto.py` define una función `crear_punto(valor, context_keys=None)`.
- La función expone `_param_specs` con `ParamSpec("valor", float)`.
- `TraduceToEs.py` declara `TRADUCCIONES = {"demo": "Demo", "crear punto": "crear_punto"}`.

Eso permite que el cargador:

1. Cree un `NodoContexto` llamado `Demo`.
2. Registre la traducción hablada `demo -> Demo`.
3. Registre la traducción hablada `crear punto -> crear_punto`.
4. Enlace la función real con `EnvoltorioFuncion`.
5. Permita que `ExploradorVoz` navegue al contexto y ejecute la función.

Este caso sirve como plantilla para agregar nuevas herramientas reales sin tocar el núcleo.

## 5. Integración entre módulos

La relación entre componentes es la siguiente:

- `ExploradorVoz` contiene un `Command` y un `Navegador`.
- `Command` usa un `voice_model` para escuchar.
- `Navegador` administra `NodoContexto`.
- `NodoContexto` contiene `EnvoltorioFuncion` y otros `NodoContexto`.
- `EnvoltorioFuncion` valida con `ParamSpec`.
- `CargadorConTraducciones` construye el árbol inicial.

En otras palabras: el cargador crea la estructura, el navegador la recorre, el comando filtra la voz y el explorador decide qué ejecutar.

## 6. Flujo de arranque actual

Archivo: [PruebaIntegracion/main.py](main.py)

El `main` actual reemplaza el arranque rígido por un flujo más flexible.

### Qué hace

- Lee argumentos por consola.
- Intenta cargar el árbol desde `dic/`.
- Si no hay contenido, crea una demo mínima con una función de ejemplo.
- Crea el `Navegador`.
- Instancia el modelo de voz real o un modelo simulado de demo.
- Lanza `ExploradorVoz.bucle_comando()`.

### Modo demo

El modo demo sirve para probar el flujo sin micrófono ni modelo Vosk instalado. Es especialmente útil para validar integración, navegación y ejecución básica.

## 7. Ejemplo de uso

### Modo demo

```bash
python -m PruebaIntegracion.main --demo --max-iter 2
```

Ese modo usa un modelo simulado que devuelve una secuencia de frases y permite confirmar que el árbol, la traducción y la ejecución funcionan.

### Modo real

```bash
python -m PruebaIntegracion.main --modelo MODELO\vosk-model-small-es-0.42
```

En ese caso se usa `VoskModel` y la entrada depende del micrófono y de la instalación de dependencias.

## 8. Código de ejemplo conceptual

La idea central del sistema es esta secuencia:

```python
raiz = construir_estructura_desde_diccionario()
navegador = Navegador(raiz)
explorador = ExploradorVoz(modelo_voz, navegador)
explorador.bucle_comando()
```

Y dentro del explorador:

```python
token = command.exclusive_listen(vocabulario)
nombre_real = _obtener_nombre_real_ascendente(token)
encontrado = navegador.buscar_funcion_ascendente(nombre_real)
```

Ese pequeño ciclo resume la arquitectura completa: escuchar, traducir, buscar y ejecutar.

## 9. Estado actual y limitaciones

### Estado actual

- La arquitectura principal está implementada.
- El arranque tiene modo demo funcional.
- El cargador ya puede recorrer `dic/` y preparar un árbol.
- La búsqueda ascendente y la ejecución básica están probadas.

### Limitaciones actuales

- `dic/` todavía está vacío, por lo que el sistema usa un fallback de demo si no encuentra módulos reales.
- La interpretación numérica de `ExploradorVoz` es simple y puede ampliarse.
- `Command` y `ExploradorVoz` están preparados para crecer, pero la semántica final depende de los módulos reales que se agreguen en `dic/`.

## 10. Conclusión

`PruebaIntegracion` concentra la implementación práctica del mapa descrito en los documentos de idea. Su valor para el proyecto es que ya no se trata solo de una explicación conceptual: ahora existe una base ejecutable que muestra cómo traducir la navegación por voz en un árbol de contextos, cómo validar parámetros antes de ejecutar acciones y cómo extender el sistema sin reescribir el núcleo.
