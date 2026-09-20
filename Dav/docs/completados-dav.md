# Completados — DAV

Contraparte de [`pendientes-dav.md`](pendientes-dav.md): lo que **ya está
resuelto**, con qué era el problema y cómo se cerró. Sirve para no re-diagnosticar
lo mismo dos veces y para ver el avance real sin leer el historial de git.

Orden: lo más reciente arriba.

---

## «Mover» la vista a un punto (2026-09-20)

`Dav/dic/moveview.py`: pide un punto y centra la cámara en él sin cambiar hacia dónde
mira ni el zoom (se corre la posición de la cámara a lo largo de su eje de visión,
a la distancia de enfoque; usa pivy). Igual que la cota, pide **X, Y** (dibujo plano,
o boceto en edición, con su `Placement`) o **X, Y, Z** (modelo 3D) según
`measure.dimensionMode()`. Está en los 384 `TraduceTo*` de todos los contextos, en
es/en/pt (`MOVE_VIEW_PHRASES`), agregado con `setdefault`: donde «mover» ya tenía otro
significado (Explorer/Edit, Draft/modify, Sketcher) gana el local y valen las variantes
«mover vista», «mover cámara», «centrar en»...

---

## «Medir» / «cota»: 2D o 3D según el documento (2026-09-20)

`CreateDimension` (`Dav/dic/measure.py`, importado por 36 `TraduceTo*`) pedía siempre
seis valores. Ahora decide en cada ejecución y pide **cuatro** (X, Y de cada punto) o
**seis** (X, Y, Z):

1. boceto en edición → 2D, en el plano del boceto (usa su `Placement`);
2. el documento tiene algún sólido → 3D;
3. sin sólidos y banco Draft/Sketcher/TechDraw activo → 2D;
4. cualquier otro caso → 3D.

Sigue siendo el mismo nombre, así que los diccionarios no cambian. Funciona porque
el colector y el validador leen `inspect.signature(función)` en cada ejecución:
`CreateDimension` es un objeto invocable con `__signature__` calculado en el momento.
Además, todos los `TraduceTo*` de `Workbench` (es/en/pt) reciben las frases de
`MEASURE_PHRASES` (en `measure.py`) con `setdefault`: no pisan frases propias del
contexto (p. ej. «cota» dentro de `constraints` sigue siendo la del Sketcher). La
gramática de Vosk solo incluye el contexto actual y la raíz, no los ancestros, por
eso tiene que estar en cada diccionario y no alcanza con la búsqueda hacia arriba.

---

## Preguntar sobre qué se trabaja, modificar por voz y corregir (2026-09-20)

Seguimiento de una auditoría a simple vista. Todo en `Dav/dic/` salvo dos prompts nuevos.

### 1. Comandos que dependían de «selección u objeto activo»

`pad_by_length`, `revolve_by_angle`, `pocket_by_length` y `groove_by_angle` tomaban
`_SelectedOrActive`: tras crear una figura, el «activo» es la figura, no un perfil
(mismo origen que el fallo de «agujero pasante»). Ahora preguntan el dibujo con
`askSketch`. Un dibujo suelto (sin cuerpo) en un corte ya no crea un cuerpo vacío
nuevo: se pregunta sobre qué cuerpo trabajar (`_OwningBody`).

### 2. Modificar en Draft sin mouse (`DraftWork/_modify.py`)

`modify`, `modification`, `array` y `facebinder` lanzaban el comando nativo, que
espera clics. Ahora cada uno pregunta el objeto con el menú de voz y los datos con
ventanas numéricas, y usa la API de Draft: clonar, degradar/mejorar, a boceto, mover,
rotar, escalar, espejo, desfase, redondeo, unir, editar/estirar un punto, pendiente,
dividir, extender/recortar, polilínea a curva, vista 2D, todas las matrices
(circular, ortogonal, polar, por trayectoria, por puntos, con y sin enlaces) y
unión de caras. Lo nativo quedó como `interactive_*`.

### 3. Cuerpo nuevo o existente

Las figuras aditivas preguntan «¿cuerpo nuevo?» (`YesNoInputPrompt`: «no» es una
respuesta, no cancelar). Con «no» se abre el menú de cuerpos válidos y la figura se
suma a uno existente; si no toca el sólido, FreeCAD la rechaza y se descarta con un
aviso. Las sustractivas y los agujeros abren siempre el menú de cuerpos válidos
(`chooseBody`; `isBody` descarta los de operación rota).

### 4. Cobertura

- **Figuras sin parámetros**: elipsoide, cuña, hélice, loft y tubo, aditivos y
  sustractivos. La cuña se pone de pie (su altura nace en Y) y se centra en x, y, z;
  hélice, loft y tubo eligen sus dibujos de una lista.
- **Sketcher por voz** (`Sketcher/_edit.py`, `_elements.py`, `constraints/_voice.py`):
  recortar, dividir, extender, redondeo, bisel, simetría, mover y construcción, y las
  restricciones **geométricas**. Se elige el boceto de una lista y el elemento **por
  número** (orden de dibujo, desde 1; el mensaje del pedido lo lista con su tipo).
  **Las cotas y «medir» no se tocan**: `constraints.py`, la cota lineal de Draft y
  los bloques MEASURE (`measure.py`) quedaron como estaban.
- **Corregir por voz** (`Correction/`, enganchado en `dic/TraduceTo*.py`, se dice desde
  cualquier contexto): «deshacer», «rehacer», «borrar último», «borrar objeto» y
  «borrar rotos». Borrar pide confirmación y no borra lo que otros objetos usan.
- **Idiomas**: ver `pendientes-dav.md` §5. TechDraw ya estaba cargado; los fallos
  reales eran typos y mayúsculas en imports.

Pendiente: rotar, escalar y desfasar elementos del boceto, y las restricciones
`lock`, `horver` y `coincidentunified`, siguen usando el comando nativo.

---

## PartDesign: agujeros y figuras con posición (2026-09-20)

«agujero pasante» fallaba con `No base set, no sketch support either` y
«agujero ciego» con `draw the hole centres in a sketch first`. Además ninguna
figura preguntaba dónde iba.

### La causa real

- `hole_by_size` creaba el `Hole` con `doc.addObject` (fuera del Body) y le
  asignaba el perfil **antes** de meterlo al Body: FreeCAD lo rechaza.
- Tomaba como perfil «el objeto activo», que tras «cubo» era el propio cubo:
  convertía las 12 aristas de la caja en un boceto.
- Usaba `DepthType = 1` creyendo que era «profundidad explícita». En FreeCAD 1.x
  `0 = Dimension` y `1 = ThroughAll`: el valor dictado se ignoraba. Lo mismo
  pasaba en `hole_choose_sketch` ("agujero" con boceto elegido).

### Qué cambió (`Dav/dic/Workbench/PartDesign/`)

- **Agujeros sin boceto previo**: `hole_by_size(diametro, x, y, z)` y
  `blind_hole_by_size(diametro, profundidad, x, y, z)` dibujan solos el boceto
  (círculo en x, y sobre el plano z) dentro del Body del último sólido. `z` es
  la altura de la cara desde la que se perfora; corta hacia -Z y, si así no saca
  material, se invierte. Si tampoco saca material se descarta y se avisa.
- **Figuras centradas en (x, y, z)**: caja, cilindro, esfera, cono, toro y
  prisma, aditivos y sustractivos (cono, toro y prisma sustractivos eran
  comandos nativos sin parámetros). `_placement.py` ata la figura al plano XY
  del Body con `AttachmentOffset`, corrida media medida donde la primitiva nace
  con una esquina o la base en el origen.
- **Con qué cuerpo se trabaja**: agujeros y cortes usan `chooseBody`: solo se
  ofrecen cuerpos con un sólido válido (`isBody` en `_prompts.py` descarta los
  que tienen la última operación rota). Con uno solo se usa directo; con varios
  se pregunta por voz («avanzar» / «okey»). Antes se cortaba siempre sobre el
  último Body: si su remate era un `Hole` roto, el corte fallaba con
  `Cannot subtract primitive feature without base feature`.
- Un corte que no toca el sólido (o no saca material) ya no deja una feature
  inútil en el modelo: se elimina y se avisa.

Pendiente: elipsoide, cuña, hélice, loft y tubo siguen usando el comando nativo.

---

## Gramática de Vosk acotada al contexto (2026-08-10)

Era la **§1** de pendientes: el `KaldiRecognizer` se creaba sin `SetGrammar`, así
que Vosk competía contra las **100.001 palabras** del modelo en cada frase en vez
de las ~12 del contexto activo. De ahí «croquis» → «crockett» y el «traffic» que
nadie dijo.

Integrado del PR #176 de SoPerez1, más los arreglos del #178.
Funcionamiento completo en
[`acortador-gramatica-vosk.md`](acortador-gramatica-vosk.md).

### La causa que no estaba a la vista

La gramática por sí sola no alcanzaba: **tumbaba FreeCAD**. Vosk no acepta que se
le cambie la gramática a un recognizer que ya procesó audio, y falla con una
excepción de C++ que ningún `except` de Python atrapa.

```
SetGrm():recognizer.cc:235
"Can't add speaker model to already running recognizer"
```

Como el loop llama `SetGrammar` después de procesar audio, **cada cambio de nivel
era un intento de crash**. Verificado contra el modelo `pt` en procesos
separados:

| escenario | resultado |
| --- | --- |
| `SetGrammar` antes de audio | ok |
| `SetGrammar` después de audio | ERROR → crash |
| `Reset()` + `SetGrammar` | ok |

`speech/voice_commands.py` ya tenía `USE_GRAMMAR = False` con la nota *"can block
all recognition on some models"*: alguien se había chocado con esto antes. Esa
variable **no la leía nadie**, así que no apagaba nada, y su diagnóstico era
incorrecto —no depende del modelo, pasa siempre—. Se eliminó.

### El micrófono que "no tomaba"

Segundo síntoma, misma raíz. El log mostró los dos modos peleándose el
recognizer:

```
14:28:27  aplicando gramatica: 82 frases    ← preferencias
14:28:27  aplicando gramatica: 54 frases    ← CAD
14:28:27  aplicando gramatica: 82 frases
```

Cada aplicación hace `Reset()`, que descarta el audio a medio reconocer, así que
ninguna frase llegaba a completarse. El loop ahora drena la cola y se queda solo
con la última gramática.

### Qué se hizo

| Cambio | Efecto |
| --- | --- |
| `Browser.GetSpokenPhrases()` | Gramática del nivel activo, derivada del diccionario |
| `Reset()` antes de `SetGrammar` | Cierra el crash |
| Solo la última gramática de la cola | Cierra el micrófono muerto |
| `core/dav_log.py` | Log a archivo: sin esto nada de lo anterior era diagnosticable |
| `enviar`/`cancelar` a `NavCommands/` | Estaban en tres lugares del código, ya desincronizados |

### Verificación

Sesión real por voz dentro de FreeCAD: la gramática sigue la navegación (54 en la
raíz → 93 en Archivo → 199 en Sketcher), sin crashes ni gramáticas pisándose.

### Lo que sigue abierto

- **La gramática restringe el vocabulario, no la sintaxis.** Vosk puede combinar
  palabras válidas en frases sin sentido («extender oblongo»). No ejecutan nada,
  pero con 199 frases activas hay más superficie para el ruido.
- `settings.json` a veces queda en `pt` entre sesiones y todavía no se sabe qué
  lo escribe. El log ya registra qué frase dispara cada cambio de idioma.

---

## Panel DAV acoplado a FreeCAD (2026-08-09)

Migración completa de la GUI: de proceso externo a `QDockWidget` dentro de
FreeCAD. Plan y etapas en [`plan-unificacion-guis.md`](plan-unificacion-guis.md).

### El problema de fondo

La `InterfazDAV` **no abría**. Corría como proceso aparte con su propio
PySide6 6.11.1 y heredaba de FreeCAD las variables que apuntan a su Qt 6.8.3:

```
ImportError: DLL load failed while importing QtWidgets
```

Se intentó parchear tres veces (limpiar `PYTHONHOME`/`PYTHONPATH`/`QT_PLUGIN_PATH`,
filtrar el `PATH`, cambiar el `cwd`) y ninguna alcanzó: cada parche tapaba una vía
de contaminación conocida y quedaban las que dependen del estado en memoria del
proceso padre.

**Se resolvió por construcción, no por parche:** un widget dentro de FreeCAD usa
el Qt de FreeCAD, así que no hay dos Qt que colisionen.

### Qué se hizo

| Etapa | Resultado |
| --- | --- |
| 1 | `MainWindow.py` (1011 líneas) partido en `DavPanel` + `ContextView` + `IconLocator`, sin dependencias de FreeCAD ni de archivos |
| 2 | Panel montado como dock, alimentado por el `Browser` en proceso; puente por archivos eliminado en ambas direcciones |
| 3 | Árbol de objetos desde `App.ActiveDocument` + `DocumentObserver`, sin macro ni polling |
| 4 | Ventana externa retirada por completo, incluido `DiccionarioPrueba/` |
| 5 | Launcher de escritorio borrado: queda **una sola GUI**, cierra §2.b |

### Por qué eran "dos GUIs" y por qué ahora hay una

No eran equivalentes: `InterfazDAV/MainWindow.py` (1011 líneas) era la de
trabajo, y `IntegracionGUI/ui/main_window.py` (138) un *launcher* cuyo botón de
voz hacía `Popen` de la otra. Divergieron por desarrollo paralelo, no por diseño.

La etapa 5 se resolvió al revés de lo planeado: se recomendaba conservar el
launcher como configurador de escritorio, pero su botón principal ya estaba roto
(lanzaba la ventana borrada en la etapa 4) y **no aportaba la descarga de
modelos** —ese flujo vive en `preferences_dialog.py`, accesible desde la barra
DAV y el botón ⚙ del panel—. Sólo *avisaba* si faltaba un modelo, aviso que
`voice_bootstrap` ya da.

### El puente por archivos, eliminado

| Antes | Ahora |
| --- | --- |
| `export_context_state()` → JSON, leído cada 500 ms | `PublishContext()` directo |
| `command_queue.txt` + `QTimer` | `SendCommand()` → `procesar_frase_final` |
| `voice_history.log` por polling | `_publish_line()` en el momento |
| `tree_data.json` + macro + 2 timers | `App.ActiveDocument` + observador |

Sobreviven `voice_history.log` (registro persistente) y `voice_status.json`
(`export_voice_status` es el punto único del estado del motor, y desde ahí se
publica al panel).

### Borrado, ~4900 líneas

`main.py` · `run_interfaz.bat` · `VoiceWorker.py` · `MainWindow.py` ·
`trigger_capture.py` · `capture_tree.FCMacro` · `HelpWindow.py` ·
`DiccionarioPrueba/` · `DavPanelController` + `FileBridgeSource` · los 7 métodos
del lanzador externo en `dav_commands.py` · `_schedule_interfaz_dav_launch`

### Un crash duro que apareció y se cerró

Montar el panel tumbaba FreeCAD entero (`0xC0000005`), sin traza en la consola de
Python. El log de FreeCAD lo mostró: se tocaba un widget Qt **desde el hilo del
micrófono**, lo cual es access violation, no una excepción que un `except` pueda
atrapar.

Corregido moviendo las publicaciones dentro de `run_on_main_thread`, y con
`_on_gui_thread()` que las bloquea si aun así llegaran desde otro hilo.

---

## Defectos de la GUI corregidos (2026-08-09)

| Síntoma | Causa real |
| --- | --- |
| Botones con dos letras en vez de icono | La clave y el archivo diferían en case/separadores (`lineattributes` vs `LineAttributes.svg`); y `pieza`/`circulo`/`stdview` tienen icono con otro nombre → normalización + tabla de alias |
| Iconos de tamaños dispares | `QSvgWidget` embebido dibujaba según el `viewBox` de cada SVG → `setIcon`/`setIconSize` |
| "Micrófono inactivo" con la voz activa | `PublishStatus` existía pero no lo llamaba nadie |
| La ventana quedaba siempre encima, sin minimizar | Un `QDockWidget` flotante es `Qt.Tool` por defecto → flags de ventana real, reaplicados en `topLevelChanged` |
| El panel se estiraba al entrar a contextos grandes | Los botones iban en una sola fila; `Part` tiene 47 entradas (~3000 px) → grilla con scroll horizontal y alto fijo |
| El botón "volver" no hacía nada | `NavCommands/` sólo tenía `TraduceToEs.py`; en otros idiomas se cargaban **cero** comandos de navegación |
| La ayuda salía en el Report View, no en el panel | Los comandos escriben con `print()` (988 llamadas en 123 archivos) → se captura el stdout durante la ejecución |
| `Cannot find icon` en la barra | `Std_DlgCustomize` es un identificador de comando, no un nombre de icono |
| `part` y `circle` aparecían en la raíz | Los `TraduceTo*` agregaban dos destinos que `base.py` no define; `circulo` además es una hoja que dibuja, no una categoría |

---

## Análisis del modelo de voz (2026-08-09)

**Hallazgo contrafáctico:** un modelo Vosk más grande **no** mejora el
reconocimiento de comandos. Detalle completo en `pendientes-dav.md` §10.

- El modelo chico ya carga 100.001 palabras y DAV usa 745 (0,75 %). La mediana
  por contexto es de 12 frases: un factor de ~8.000×.
- 66 de esas 745 (8,9 %) están **fuera del vocabulario** y son imposibles de
  emitir: `chaflán`, `extruir`, `biselar`, `isométrica`, `polilínea`. Es el
  núcleo del vocabulario CAD, y agrandar el modelo no las agrega.
- El overkill está en el modelo de lenguaje (`Gr.fst`), no en el acústico. Una
  gramática restringida reemplaza el primero y conserva el segundo.

> **Falta el benchmark** de tasa de acierto antes de presentarlo como resultado
> experimental. El diseño del experimento está en §10.f.

---

## Limpieza de vocabulario (2026-08-08)

**89 → 66 palabras fuera de vocabulario (11,5 % → 8,9 %).** Al cruzar el árbol
contra el modelo aparecieron 89 palabras que el reconocedor no puede emitir, pero
no todas eran el mismo problema: sólo una categoría era limitación del modelo, el
resto era deuda del diccionario (claves internas que quedaron como frase hablada,
anglicismos sin sinónimo, typos). Detalle en `pendientes-dav.md` §11.

---

## Correcciones de diccionarios y navegación (2026-06 / 2026-08)

- **Subcontextos anidados, nunca aplanados** — `explorer.update({'file': file})`
  y no `explorer.update(file)`. Aplanar colisionaba claves repetidas entre hojas
  y dejaba la carpeta fuera del árbol navegable. Convención en
  `pendientes-dav.md` §4.
- **`NavCommands/`** — las palabras de navegación (subir, contexto) viven en el
  diccionario como cualquier otro comando, no hardcodeadas en `browser.py`.
- **Imports rotos** que tumbaban la carga de Base y Sketcher.
- **Normalización de acentos** unificada en una sola función.
- **`IsSameTarget`** como alias público de `_SameTarget`: quien recorre `Context`
  desde afuera necesita deduplicar igual que el `Browser`.

## Resaltado de la selección en el árbol del panel (2026-08-18)

**Problema.** Al decir `"seleccion"` → `"siguiente"`, el objeto se seleccionaba
en FreeCAD pero el árbol del panel DAV no lo resaltaba. Lo mismo con los objetos
que crea `CreateObjects`: aparecían en el árbol, pero no se veía cuál estaba
activo. Había que mirar el árbol nativo de FreeCAD para saberlo.

**Causa real.** No faltaba nada en el árbol ni en `ObjectSelection`: los dos
funcionaban bien por separado. `ObjectSelection.MonoSelection()` llama a
`Gui.Selection.addSelection(Obj)` y ahí termina su trabajo — **nadie le avisaba
al panel**. El `_TreeDocumentObserver` que ya existía escucha cambios del
*documento* (crear/borrar/recomputar), y seleccionar no cambia el documento,
así que nunca se disparaba. Faltaba el observador del otro canal.

**Solución.**

- `DavPanel.HighlightSelection(Names)` — recorre el mapa `_treeItems` (que
  `SetTree` ahora guarda) y marca los seleccionados, con `scrollToItem` al
  primero. El widget sigue sin importar FreeCAD: recibe una lista de nombres.
- `BrowserPanelSource.PublishSelection()` — lee `Gui.Selection.getSelection()`
  y se lo pasa al panel.
- `_TreeSelectionObserver` — registrado con `Gui.Selection.addObserver()`,
  mismo patrón que `_TreeDocumentObserver`: todos los slots caen en un
  `_Refresh` con `try/except`, porque una excepción acá se propagaría al
  manejo de selección de FreeCAD.

**Detalle no obvio.** `HighlightSelection` envuelve el bucle en
`blockSignals(True/False)`: `setSelected()` emite `itemSelectionChanged`, y
cuando se implemente el sentido inverso (clic en el panel → seleccionar en
FreeCAD) eso se realimentaría en bucle infinito. Bloquear ahora evita el bug
antes de que exista.

Sigue pendiente el sentido panel → FreeCAD y navegar el árbol por voz
("seleccionar el tercero"). Ver `plan_arbol_de_objetos_navegable.md`.

---

## Cómo se agrega a este documento

Al cerrar un pendiente: moverlo acá con **qué era el problema** y **cuál resultó
ser la causa real**, no sólo qué se cambió. Varias veces la causa aparente y la
real fueron distintas (los iconos no faltaban, el nombre no coincidía; el botón
de ayuda sí andaba, su salida iba a otro lado), y ese es justamente el dato que
evita repetir el diagnóstico.
