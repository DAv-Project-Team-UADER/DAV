# Completados — DAV

Contraparte de [`pendientes-dav.md`](pendientes-dav.md): lo que **ya está
resuelto**, con qué era el problema y cómo se cerró. Sirve para no re-diagnosticar
lo mismo dos veces y para ver el avance real sin leer el historial de git.

Orden: lo más reciente arriba.

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
