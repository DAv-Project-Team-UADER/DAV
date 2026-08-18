# Plan: unificar las dos GUIs (resolver §2 de pendientes-dav.md)

**Estado:** etapas 1 a 4 implementadas; queda la 5.
**Fecha:** 2026-08-09
**Resultado:** resumido en [`completados-dav.md`](completados-dav.md).
**Motivo inmediato:** la InterfazDAV no abre desde FreeCAD por un conflicto de
DLLs de Qt que **sólo existe porque corre como proceso externo**. Parchearlo es
posible; eliminarlo por construcción es mejor.

---

## 1. El mapa real (verificado, no asumido)

La suposición de "hay dos GUIs completas y hay que elegir una" **es incorrecta**.
Lo que hay es:

| | `InterfazDAV/` | `IntegracionGUI/GUIFreeCad/` |
| --- | --- | --- |
| Ventana | `MainWindow.py` — **1011 líneas** | `ui/main_window.py` — **138 líneas** |
| Qué es | la GUI de trabajo real | un **launcher de escritorio** |
| Dónde corre | proceso externo (venv Python 3.14) | proceso externo (venv) |
| Qt | PySide6 propio → **choca con el de FreeCAD** | PySide6 propio |
| Tiene | historial, minimizar, árbol, botones de contexto | preferencias, descarga de modelos |

El dato que cambia todo: **`ui/main_window.py` no usa el `Browser`**. Su botón
"Iniciar Voz" hace `subprocess.Popen` de… `InterfazDAV/main.py`
(`ui/main_window.py:121-138`). Es un lanzador, no una alternativa.

### Dónde vive realmente el Browser

```
FreeCAD (proceso)
└── dav_commands.py / freecad_wb.py
    └── integration/voice_bootstrap.py  ← start_voice_engine()
        └── Browser(...)                ← el motor real, DENTRO de FreeCAD
            └── BrowserVoiceAdapter
                └── escribe context_state.json ─┐
                                                │  puente por archivos
InterfazDAV (proceso externo)                   │
└── MainWindow._PollFreeCADState() ←────────────┘  polling 500 ms
```

El `Browser` **ya corre dentro de FreeCAD**. Ninguna de las dos ventanas lo
tiene: una lo consume por archivos, la otra ni lo toca.

> **Corrección a la recomendación previa:** decir "migrar historial y minimizar
> a IntegracionGUI" estaba mal planteado — `IntegracionGUI` no es la GUI buena a
> la que mudarse, es un launcher de 138 líneas. La migración real es de
> `InterfazDAV` **hacia adentro de FreeCAD**, no hacia la otra carpeta.

---

## 2. Por qué el bug de Qt es estructural

`InterfazDAV` corre en un venv con **PySide6 6.11.1**. FreeCAD 1.1 trae su propio
Qt6 en `bin/` (`Qt6Core.dll`, `Qt6Widgets.dll`, …). Al lanzarse como subproceso
hereda del padre:

- `PYTHONHOME` / `PYTHONPATH` → el venv carga la stdlib de FreeCAD
  (`SRE module mismatch`)
- `QT_PLUGIN_PATH` y el `bin` de FreeCAD en el `PATH` → PySide6 resuelve las Qt6
  de FreeCAD en vez de las suyas (`DLL load failed while importing QtWidgets`)

Se puede sanear el entorno (se intentó: quitar variables, filtrar el `PATH`,
anteponer la carpeta de PySide6, cambiar el `cwd`). Pero cada parche cubre una
vía de contaminación conocida, y quedan las que dependen del estado en memoria
del proceso padre. **Mientras haya dos Qt distintos en juego, el problema puede
volver** con otra versión de FreeCAD, de PySide6 o en otra máquina.

Un widget dentro de FreeCAD usa **el Qt de FreeCAD**. El conflicto no se
parchea: deja de existir.

---

## 3. Objetivo

Convertir `InterfazDAV` en un **panel acoplado dentro de FreeCAD**
(`QDockWidget`), eliminando el proceso externo y el puente por archivos.

```
ANTES                                DESPUÉS

FreeCAD ──► Browser                  FreeCAD ──► Browser
   │           │                        │           │
   │      context_state.json            │      señal Qt directa
   │      command_queue.txt             │           │
   │      voice_history.log             │           ▼
   ▼           │                        └──► DavPanel (QDockWidget)
InterfazDAV ◄──┘                                 historial, árbol,
(proceso externo, Qt propio)                     botones, minimizar
```

### Lo que se elimina

- El conflicto de Qt (por construcción)
- `command_queue.txt`, `context_state.json`, `voice_status.json`,
  `voice_history.log` como canal — y con ellos los pendientes §2.d:
  `pop_command_queue()` perdiendo comandos, la latencia de 500 ms, el estado
  versionado por error
- Los dos `QTimer` de polling
- `_launch_interfaz_dav()`, `_clean_child_env()`, `_probe_pyside6()`,
  `_check_interfaz_started()` en `dav_commands.py`
- `run_interfaz.bat`, `trigger_capture.py`, `capture_tree.FCMacro`

### Lo que se gana

- La GUI accede al `Browser`, al documento y a la selección **en el mismo
  proceso**: sin serializar, sin latencia, sin pérdida de comandos
- El árbol de objetos sale de `App.ActiveDocument` directo, sin macro ni
  `tree_data.json`
- Tema e idioma heredados de FreeCAD

---

## 4. Migración por etapas

Cada etapa deja el repo funcionando. No hay un "big bang".

### Etapa 0 — Parche provisorio (opcional)

Dejar los arreglos de `dav_commands.py` (venv por ruta, saneo de entorno,
diagnóstico de arranque) para que la GUI abra **mientras** dure la migración. Se
borran en la etapa 4.

> Decisión pendiente: si la etapa 1 se hace pronto, este parche puede saltearse.

### Etapa 1 — Extraer el panel

Separar `MainWindow.py` (1011 líneas) en:

- **`DavPanel.py`** — `QDockWidget` con todos los widgets: historial, árbol,
  botones de contexto, overlay. **Sin** `QTimer` de polling, sin lectura de
  archivos, sin `subprocess`.
- **`DavPanelController.py`** — el pegamento: recibe el contexto del `Browser` y
  actualiza el panel.

`MainWindow.py` queda como wrapper delgado para poder seguir corriendo la GUI
suelta durante la transición.

Regla: `DavPanel` **no importa FreeCAD**. Recibe datos, emite señales. Así se
puede testear sin FreeCAD, igual que `Browser`.

### Etapa 2 — Montar el panel en FreeCAD

En `freecad_ui_setup.py` (ya sabe hacer `Gui.getMainWindow()`):

```python
panel = DavPanel()
Gui.getMainWindow().addDockWidget(Qt.RightDockWidgetArea, panel)
```

Conectar al `Browser` por señales, reemplazando el puente:

| Hoy (archivos, 500 ms) | Después (señales, inmediato) |
| --- | --- |
| `export_context_state()` → JSON | `browser.ContextChanged` → `panel.RenderContext()` |
| `command_queue.txt` → `pop_command_queue()` | `panel.CommandRequested` → `browser.ProcessPhrase()` |
| `append_voice_history()` → `.log` | `adapter.PhraseRecognized` → `panel.AddToHistory()` |

El callback `on_descend` que ya existe en `Browser` (hoy sin usar) es el enganche
natural para `ContextChanged`.

En esta etapa conviven las dos rutas: el panel acoplado y la ventana externa. Se
compara comportamiento.

> **Cerrada (2026-08-09).** El puente por archivos ya no existe en ninguna
> dirección:
>
> | Antes | Ahora |
> | --- | --- |
> | `export_context_state()` → JSON | `PublishContext()` directo al panel |
> | `command_queue.txt` + `QTimer` 500 ms | `SendCommand()` → `procesar_frase_final` |
> | `voice_history.log` leído por polling | `_publish_line()` en el momento |
> | `tree_data.json` + macro | `App.ActiveDocument` + observador (etapa 3) |
>
> Se borraron, ya sin consumidor: `export_context_state`, `read_context_state`,
> `write_command_queue`, `pop_command_queue`, `read_voice_history_from`, el
> `QTimer` que sondeaba la cola y el cuerpo de `_export_state`.
>
> `voice_history.log` y `voice_status.json` **siguen escribiéndose**: el primero
> como registro persistente, el segundo porque `export_voice_status` es el punto
> único por donde pasa el estado del motor y desde ahí se publica al panel.
>
> `on_descend` sigue sin usarse: el refresco va por `PublishContext()` al final
> de cada frase, que cubre también los comandos que no cambian de nivel.

### Etapa 3 — Árbol de objetos nativo

**Por qué va aparte de la 2:** son *dos puentes distintos*, con archivos
distintos y código distinto. La etapa 2 reemplaza el canal de voz
(`context_state.json`, `command_queue.txt`, `voice_history.log`); el árbol viaja
por su propio camino:

```
InterfazDAV._AutoCapture()  ──► trigger_capture.py
                                    │
                                    ▼
                            capture_tree.FCMacro  (dentro de FreeCAD)
                                    │
                                    ▼
                            tree_data.json  ──► _RefreshTreeData() (QTimer)
```

Terminada la etapa 2, el árbol **seguiría** leyendo `tree_data.json` por macro:
no se arregla solo. Y al revés, si se junta todo en una etapa y el árbol se
complica, bloquea un fix de voz que ya estaba andando.

Trabajo: `_PopulateTree()` pasa a leer `App.ActiveDocument.Objects` directo
(mismo contrato: `name`, `label`, `type`, `visible`, `parent`). Se borran
`trigger_capture.py`, `capture_tree.FCMacro`, `_AutoCapture()`,
`_RefreshTreeData()`, `_LastTreeMtime` y el `QTimer` de refresco — el documento
avisa por sus propias señales en vez de sondear cada 5 s.

> **Hecho (2026-08-09) para el panel acoplado.** `BrowserPanelSource.PublishTree()`
> lee `App.ActiveDocument` en proceso, y `_TreeDocumentObserver` (registrado con
> `App.addDocumentObserver`) lo dispara ante creación, borrado, cambio,
> recompute y cambio de documento activo. El árbol ahora sigue también lo que se
> dibuja con el mouse, no sólo lo que entra por voz.
>
> **Falta** borrar el camino viejo: `trigger_capture.py` y `capture_tree.FCMacro`
> siguen en el repo porque su único consumidor es `MainWindow.py`, que se retira
> en la etapa 4. Borrarlos ahora rompería la ventana externa mientras todavía es
> la que se usa.

### Etapa 4 — Borrar el andamiaje — HECHO (2026-08-09)

Antes de borrar se cerró la condición de entrada: los botones de **ayuda** y
**preferencias** del panel emitían señales que nadie conectaba. Ahora
`BrowserPanelSource` las atiende — preferencias abre el diálogo de GUIFreeCad, y
la ayuda vuelca `Browser.DescribeContext()` al historial (los comandos válidos
*acá y ahora*, más útil que el texto fijo de la ventana externa).

Borrado:

- `InterfazDAV/`: `main.py`, `run_interfaz.bat`, `VoiceWorker.py`,
  `MainWindow.py` (1011 líneas), `trigger_capture.py`, `capture_tree.FCMacro`,
  `HelpWindow.py` y **`DiccionarioPrueba/`** — cierra §2 del todo
- `DavPanelController.py` + `FileBridgeSource`: eran el puente por archivos que
  esta etapa retira; sin ventana externa quedaron sin consumidor
- `dav_commands.py`: `_launch_interfaz_dav`, `_check_interfaz_started`,
  `_clean_child_env`, `_probe_pyside6`, `_venv_python`, `_bring_interfaz_to_front`,
  `close_interfaz_dav` (~180 líneas). Con ellas se va el conflicto de Qt: ya no
  se lanza ningún proceso externo, así que no hay dos Qt que colisionen.
- `freecad_wb.py`: `_schedule_interfaz_dav_launch()` y su llamada en el arranque
- `IconLocator`: la raíz `DiccionarioPrueba` (quedan 467 iconos indexados)

`Iniciar voz DAV` ahora abre el panel acoplado en vez de lanzar el proceso
externo. `iniciar_dav.bat` no cambia: nunca pasó por `run_interfaz.bat`.

Las entradas de `.gitignore` del circuito de captura se conservan a propósito,
para no versionar los archivos que quedaron en copias de trabajo viejas.

### Etapa 5 — Qué hacer con `ui/main_window.py` — HECHO (2026-08-09): (b)

Se recomendaba **(a)**, conservarlo como configurador de escritorio. Al revisar
el estado real la recomendación no se sostuvo y se fue por **(b)**, borrarlo:

- **Su función principal estaba rota.** El botón "Iniciar Voz" —el elemento
  central, de 150×150 px— hacía `Popen` de `InterfazDAV/main.py`, retirado en la
  etapa 4.
- **No aportaba la descarga de modelos.** Ese flujo vive entero en
  `ui/preferences_dialog.py` (`_download_large` + `DownloadDialog` +
  `download_large_model`), que se abre desde la barra DAV y desde el botón ⚙ del
  panel. `main_window` sólo *avisaba* si faltaba un modelo, aviso que
  `voice_bootstrap` ya da con la línea de `setup_models.py`.
- **Era el último resto del modelo de dos procesos**, lo que mantenía viva la
  pregunta de §2.b.

Borrado: `ui/main_window.py` y `GUIFreeCad/main.py` (~180 líneas de wrapper).
Conservado: `ui/preferences_dialog.py`, `ui/download_dialog.py`,
`core/model_manager.py`, `scripts/setup_models.py`.

> **Lo que se pierde:** bajar modelos con interfaz gráfica sin abrir FreeCAD.
> Queda por línea de comandos (`python scripts/setup_models.py`). Si hiciera
> falta la vía gráfica, es más barato un comando en la barra DAV que abra
> `DownloadDialog` que mantener una app de escritorio entera.

---

## 5. Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Un `QDockWidget` que crashee tumba FreeCAD entero | El panel no hace I/O ni trabajo pesado en el hilo de UI; el micrófono ya corre en su hilo |
| Toca código de varias personas (Tadeo, mica, Camila) | Etapas chicas, PRs separados, `MainWindow.py` sigue vivo hasta la etapa 4 |
| Se pierde el modo "ventana suelta" | El panel se puede desacoplar (`setFloating(True)`): se conserva el comportamiento sin proceso aparte |
| 1011 líneas es bastante para partir | La etapa 1 es sólo mover código, sin cambiar comportamiento; se hace y se prueba antes de tocar FreeCAD |

---

## 6. Orden de trabajo

Las etapas son secuenciales y se hacen de corrido; no hay que esperar a nadie
entre una y otra. Cada una cierra en un PR propio para que sea revisable.

| Etapa | Alcance | Toca FreeCAD | Toca código de otros |
| --- | --- | --- | --- |
| 1 | partir `MainWindow.py` en `DavPanel` + controlador | no | sí (`MainWindow.py`) |
| 2 | montar el panel, señales en vez de archivos | sí | sí (puente de mica) |
| 3 | árbol nativo | sí | sí (`capture_tree`) |
| 4 | borrar andamiaje | sí | sí |
| 5 | destino del launcher | no | no |

La 1 es la más grande pero la más segura: es mover código, sin cambiar
comportamiento, y se prueba corriendo la ventana suelta como hasta ahora.

**Avisar al equipo** antes de la etapa 4: ahí se borran archivos de Tadeo, mica
y Camila (`main.py`, `run_interfaz.bat`, `VoiceWorker.py`, `DiccionarioPrueba/`).
Hasta la 3 todo es aditivo o interno, y `MainWindow.py` sigue funcionando.

### Decisiones abiertas

- **Etapa 0:** ¿se deja el parche de `dav_commands.py` para que la GUI abra
  mientras dura la migración, o se salta directo a la 1? Si la 1 y la 2 salen
  rápido, el parche es trabajo tirado.
- **Etapa 5:** ¿`ui/main_window.py` queda como configurador de escritorio
  (recomendado) o se absorbe en el panel?

> Relacionado: §2, §2.b y §2.e de `pendientes-dav.md` (los pendientes que este
> plan cierra) y §9 (el mapa de los tres motores de voz).
