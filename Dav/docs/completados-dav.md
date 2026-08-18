# Completados — DAV

Contraparte de [`pendientes-dav.md`](pendientes-dav.md): lo que **ya está
resuelto**, con qué era el problema y cómo se cerró. Sirve para no re-diagnosticar
lo mismo dos veces y para ver el avance real sin leer el historial de git.

Orden: lo más reciente arriba.

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

---

## Cómo se agrega a este documento

Al cerrar un pendiente: moverlo acá con **qué era el problema** y **cuál resultó
ser la causa real**, no sólo qué se cambió. Varias veces la causa aparente y la
real fueron distintas (los iconos no faltaban, el nombre no coincidía; el botón
de ayuda sí andaba, su salida iba a otro lado), y ese es justamente el dato que
evita repetir el diagnóstico.
