# Pendientes DAV — hallazgos de sesión de auditoría de diccionarios y navegación por voz

## 1. Vosk reconoce con vocabulario abierto, no acotado al contexto

**Dónde:** `Dav/scr/ComponentesDAV/InterfazDAV/VoiceWorker.py:56`

```python
recognizer = vosk.KaldiRecognizer(model, 16000)
```

El `KaldiRecognizer` se crea sin gramática restringida (`SetGrammar`), así que Vosk compite contra todo el vocabulario del modelo español en cada frase, en vez de limitarse a los comandos válidos del contexto actual (`Browser.Context` ya tiene esa lista disponible en todo momento).

**Síntoma observado:** palabras cortas o poco frecuentes se transcriben mal — "croquis" salió como "crockett", apareció "traffic" sin que nadie lo dijera. Con el modelo pequeño (`vosk-model-small-es-0.42`, 39 MB) el efecto es más marcado que con el modelo grande.

**Arreglo sugerido:** pasarle a `KaldiRecognizer` una gramática JSON con las palabras/frases de `Browser.Context` (o `BaseContext` si aún no se descendió), actualizándola cada vez que cambia el contexto de navegación. Debería reducir bastante las transcripciones erráticas.

> Medido sobre el modelo real: `vosk-model-small-es-0.42` carga **100.001
> palabras**, y el árbol `Dav/dic/` usa **745** (0,75 %). La mediana por contexto
> es de **12 frases**. La precisión no se arregla agrandando el modelo — se
> arregla acá, restringiendo la gramática al contexto activo.

## 2. MainWindow.py (la GUI que se usa hoy) no usa el Browser real

**Dónde:** `Dav/scr/ComponentesDAV/InterfazDAV/MainWindow.py` (`_VoiceMap`, `_GroupMeta`, `_LoadGroupMeta`, `_LoadVoiceMap`)

Esta ventana tiene su propio motor de navegación por voz, separado de `navigation/browser.py` (`Browser.ProcessPhrase`, el que se audita y mantiene activamente). Lee de:

```
Dav/scr/ComponentesDAV/InterfazDAV/DiccionarioPrueba/
```

que es un diccionario de prueba chico (solo `explorer` con `file`/`edit`/`print`/`doc`), **no** el árbol completo `Dav/dic/` (Sketcher, Workbench, PartDesign, StdView, NavCommands, etc.).

**Consecuencia práctica:** todo lo arreglado en `Dav/dic/` (imports rotos, duplicados, `base.py` enlazado, `NavCommands` para "subir"/"contexto") no tiene ningún efecto en la GUI real que se está probando. Los logs de este motor tienen formato distinto (`[Voz]`, `[Btn]`, `No entendí: '...' no disponible en <grupo>`) al del `Browser` (`[DAV Browser]`, `[BrowserVoiceAdapter]`).

**Pendiente de decidir:** si `MainWindow.py` debe migrar a usar `Browser` (de `navigation/browser.py`) en vez de su propio `_VoiceMap`/`_GroupMeta`, o si son productos deliberadamente separados (uno de prueba rápida, otro el motor "serio") y hay que documentar cuál es cuál.

### 2.b Investigar POR QUÉ hay dos GUIs en paralelo

No están sólo duplicados los motores de voz: son **dos aplicaciones PySide completas**, cada una con su ventana principal, su worker de voz y su arranque.

| Componente | `InterfazDAV/` | `IntegracionGUI/GUIFreeCad/` |
| --- | --- | --- |
| Ventana | `MainWindow.py` | `ui/main_window.py` |
| Voz | `VoiceWorker.py` | `speech/dav_voice_service.py`, `speech/voice_commands.py` |
| Navegación | `_VoiceMap`/`_GroupMeta` propio | `navigation/browser.py` (`Browser`) |
| Diccionario | `InterfazDAV/DiccionarioPrueba/` | `Dav/dic/` (árbol completo) |
| Arranque | `main.py` | `main.py`, `integration/voice_bootstrap.py`, `integration/windows_startup.py` |
| Extras | `FlashOverlay.py`, `HelpWindow.py`, `Paletas.py`, `Textos.py` | `InputPrompts/` (10 módulos), `ui/preferences_dialog.py`, `core/model_manager.py`, `ui/download_dialog.py` |

Cada una tiene funcionalidad que a la otra le falta: `InterfazDAV` es la única con **historial** y con **minimizar/overlay**; `IntegracionGUI` es la única con el **Browser real**, los **InputPrompts** (pedir parámetros por voz), **preferencias/idioma** y **descarga de modelos Vosk**.

**A investigar / decidir con el equipo:**

- ¿Fue una división deliberada por grupos de trabajo, o dos ramas que divergieron y nunca se integraron?
- ¿Cuál es la que se demuestra/entrega? (hoy se está probando `InterfazDAV`, pero el motor que se mantiene y testea es el de `IntegracionGUI`)
- Si se unifica: llevar historial + minimizar a `IntegracionGUI`, o llevar `Browser` + InputPrompts a `InterfazDAV`. Mantener las dos implica duplicar cada arreglo (como ya pasó con los diccionarios).

> **Respuesta parcial (auditoría 2026-08-08):** no son dos GUIs sino **tres
> motores de voz**, y divergieron por desarrollo paralelo en mayo, no por
> diseño. Ver §9 para el mapa completo y el estado de ejecución de cada uno.

## 3. Palabras ambiguas entre workbenches (parcialmente resuelto)

`"dibujar"` (Sketcher) y `"dibujo"` (Draft) eran casi indistinguibles para el reconocimiento de voz — se sacó `"dibujo"`/`"dibujos"` de Draft en `Dav/dic/Workbench/TraduceToEs.py` (queda `"banco de dibujo"`, `"borrador"`, `"draftwork"`, `"draft"` como alternativas). Sketcher sigue teniendo `"dibujar"` como sinónimo — si se repite el problema, revisar si conviene sacarlo también y dejar solo `"croquis"`/`"banco de croquis"`.

También hay pares similares en el mismo archivo con nombres en inglés (`"sketcher"`, `"draft"`, `"partdesign"`, `"techdraw"`) — el modelo español los reconoce mal por no ser palabras españolas; siempre usar los sinónimos en español como forma principal.

## 4. Convención obligatoria: subcontextos ANIDADOS, nunca aplanados

Al armar el diccionario maestro de una carpeta, cada submenú va **como valor bajo su propia clave**, nunca fusionado con `.update(sub_dict)`:

```python
# CORRECTO (Explorer/Explorer.py, el patrón de referencia)
explorer.update({'file': file})
explorer.update({'edit': edit})

# INCORRECTO — aplana las hojas del hijo dentro del padre
explorer.update(file)
explorer.update(edit)
```

**Por qué importa.** El `Browser` navega por niveles: cada frame del stack es una carpeta, y `DictionaryLoader` lee el `TraduceTo*.py` **de esa carpeta**. Aplanar rompe dos cosas a la vez:

1. **Colisiones silenciosas de claves.** Varias hojas definen la misma clave (`create`, `help`, `center`, `horizontal`). Con `.update()` gana la última y las demás se pierden sin ningún error. En `sketcher.py` la clave `create` colisionaba 13 veces (line, point, polyline, rectangle, circle…) y solo sobrevivía la de bspline — por eso "crear línea" no hacía nada.
2. **Traducciones huérfanas.** El `TraduceToEs.py` de la subcarpeta solo se lee si el `Browser` desciende a esa carpeta como frame. Si el padre aplanó al hijo, la carpeta deja de ser un nodo navegable y su archivo de traducciones no se carga nunca, aunque esté escrito y correcto.

Corregido en esta sesión en: `workbench.py`, `StdView.py`, `sketcher.py`, `partdesign.py`, `DraftWork.py`, `TechDraw.py`, `Part.py`, `Assembly.py`, `LineAttributes.py` y `TechDraw/Dimensions/dimensions.py` (este último tenía además 7 `.update()` que eran código muerto: los descartaba una reasignación `dimensions = {...}` en la línea siguiente).

**Al agregar un workbench o submenú nuevo:** anidar, y verificar que la carpeta quede navegable (que `Browser` pueda descender y leer su `TraduceTo*.py`).

## 5. Diccionarios de traducción todavía vacíos

- `Dav/dic/Workbench/TechDraw/TraduceToEs.py` — stub sin dict `TraduceToEs`. Se entra al workbench por voz pero adentro no hay ningún comando en español.
- `Dav/dic/Workbench/Sketcher/Geometry/TraduceToEn.py` y `TraduceToPt.py` — vacíos. El español (`TraduceToEs.py`) ya está completo con las figuras (línea, círculo, rectángulo, polígono, arco, elipse, bspline…).

Mientras tanto `LenientDict` devuelve un no-op y loguea `Comando 'X' aún no implementado`, así que no rompe el contexto, pero el comando no hace nada.

## 6. Cuidado con los imports en los diccionarios (fallan en silencio)

Varios archivos tenían imports rotos que no se notaban porque `DictionaryLoader` los captura y sigue de largo. Patrones encontrados y corregidos:

- **Rutas inexistentes:** 12 archivos importaban desde `DAV.DiccionariosEnBruto.*`, que no existe en el repo.
- **Nombre de módulo con mayúscula equivocada:** `PartDesign/TraduceTo*.py` hacían `from .PartDesign import partdesign`, pero el archivo es `partdesign.py`.
- **Nombre de variable equivocado:** `Geometry/geometry.py` importaba `tools` de `BSpline_Tools/_tools.py`, que exporta `bspline_tools`.

Este último era el más grave: hacía fallar el import de `base.py` **completo**, dejando al `Browser` sin ningún comando (`[DAV] Contexto: Base — (sin comandos en este contexto)`). Un solo import roto en una hoja profunda puede tumbar todo el árbol, así que conviene verificar que `base.py` importe limpio después de tocar cualquier diccionario.

## 7. Normalización de acentos: usar siempre la misma función

**Dónde:** `Dav/scr/.../GUIFreeCad/navigation/context_entry.py`

`FindBySpoken` y `ContextEntry.NormalizeSpoken` normalizaban solo con `lower().split()`, mientras `Browser.ProcessPhrase` normaliza la frase entrante con `DictionaryLoader.NormalizeSpoken`, que además **quita acentos** (NFKD + descarte de combinantes). Como se comparaba `"diseno de pieza"` (ya sin tilde) contra `"diseño de pieza"` (con eñe), **ningún comando con tilde o eñe matcheaba nunca**: "diseño de pieza", "dibujo técnico", "información", "cuadrícula", "simetría", "chaflán", etc.

Corregido: `context_entry.py` ahora usa la misma normalización con NFKD. **Si se agrega otro punto de matcheo de frases habladas, debe usar esa misma función** — no `lower()` a secas.

## 8. Cobertura de los requisitos del MVP — qué falta

Estado del árbol `Dav/dic/` tras la sesión de auditoría. "Navegable" = el `Browser` entra al contexto por voz; "vocabulario" = tiene frases en español cargadas.

| Requisito (CLAUDE.md) | Navegable | Vocabulario ES | Falta |
| --- | --- | --- | --- |
| Explorer | Sí | Sí | — |
| Viewer (StdView) | Sí | Sí | — |
| Draft | Sí | Sí | — |
| Sketcher | Sí | Sí | — |
| PartDesign | Sí | Sí | — |
| Part | Sí | Sí | — |
| Assembly | Sí | Sí | — |
| TechDraw | Sí | **No** | `TraduceToEs/En/Pt.py` vacíos (ver §5) |

Ninguna carpeta de comandos quedó sin archivo `TraduceToEs.py`. Los únicos vacíos son los de §5 (TechDraw en los 3 idiomas, `Sketcher/Geometry` en en/pt, `Sketcher/arcslot` en los 3).

**Requisitos de la GUI** (los tres del enunciado):

| Requisito | Estado |
| --- | --- |
| Arrancar con FreeCAD | Existe `Dav/scr/ComponentesDAV/Dav/InitGui.py` + `integration/voice_bootstrap.py` y `windows_startup.py` — **verificar que efectivamente levante en un FreeCAD limpio**, no sólo desde consola. |
| Minimizarse | Implementado sólo en `InterfazDAV` (`FlashOverlay.py`, `MainWindow.py`). Falta en `IntegracionGUI`. |
| Dar historial | Implementado sólo en `InterfazDAV` (`MainWindow.py`, `Textos.py`). Falta en `IntegracionGUI`. |

Los dos últimos quedan atados a la decisión de §2.b: si se unifica en `IntegracionGUI` (el que tiene el `Browser` real), hay que portar historial y minimizar.

**Otros pendientes transversales:**

- Idiomas **en** y **pt**: el árbol está armado para tres idiomas, pero sólo el español está completo. Si el MVP se demuestra en español, documentarlo como alcance y no como bug.
- Gramática restringida de Vosk (§1) — impacta la precisión de todo lo anterior.
- Tests: `tests/test_browser.py` (18 casos) usa un loader mock. **No hay tests que corran contra el árbol real `Dav/dic/`**, que es donde aparecieron todos los bugs de esta sesión (imports rotos, aplanado, acentos). Vale la pena agregar un test de integración que recorra las rutas principales.

## 9. Hay TRES motores de voz en el repo, no dos (auditoría 2026-08-08)

Responde la pregunta abierta de §2.b. Además de los dos de esa tabla existe un
tercer sistema completo, `PruebaIntegracion/`, que **no se ejecuta nunca**.

| | A. IntegracionGUI | B. InterfazDAV | C. PruebaIntegracion |
| --- | --- | --- | --- |
| Motor | `Browser.ProcessPhrase` + `DictionaryLoader` | `_VoiceMap` / `_GroupMeta` | `ExploradorVoz` + `Navigator` |
| Diccionario | `Dav/dic/` (árbol oficial) | `InterfazDAV/DiccionarioPrueba/` | `PruebaIntegracion/diccionario/` |
| GUI | `ui/main_window.py` | `MainWindow.py` | `GUI/asistente_voz.py` |
| Estado | **Camino principal** | Vivo, pero como proceso aparte | **Huérfano — código muerto** |

### 9.a `PruebaIntegracion/` está desconectado

Es un DAVCore completo y autónomo: `core/VoiceExplorer.py`, `core/Navigator.py`,
`core/Command.py`, `core/FunctionWrapper.py`, `modelo/VoskModel.py` (la
implementación literal del UML de CLAUDE.md), `hilos/GestorDeHilos.py`, GUI y
tests propios.

Existen dos puentes que lo conectarían —`integration/cad_session.py` y
`integration/cad_voice_adapter.py`— pero **nadie los llama**. Buscar referencias
a `cad_session` / `cad_voice_adapter` fuera de esos archivos no devuelve nada.

La razón se ve en el arranque: `integration/voice_bootstrap.py` arma el motor con
`Browser` + `BrowserVoiceAdapter`, no con `ExploradorVoz` + `CadVoiceAdapter`.
Cuando las implementaciones paralelas convergieron, ganó el `Browser`.

`plan_arbol_de_objetos_navegable.md:89` ya propone borrar
`PruebaIntegracion/hilos/GestorDeHilos.py` como maqueta muerta, pero el problema
alcanza al árbol entero, no a ese archivo solo.

### 9.b `InterfazDAV` no está desconectado: corre como proceso separado

Distinto de C. `Dav/scr/gui/dav_commands.py:371` busca `InterfazDAV/main.py` y lo
**lanza como proceso aparte**. No comparte memoria ni diccionario con A.

La única comunicación entre ambos es por archivo: `freecad_wb.py:239` vigila el
`settings.json` de IntegracionGUI *"para que los cambios desde InterfazDAV
apliquen a FreeCAD"*. Se hablan por configuración, no por código — de ahí que un
fix en `Dav/dic/` no tenga efecto en B (§2).

### 9.c `InputPrompts/` SÍ está en uso (no confundir con C)

Aunque `PruebaIntegracion/` esté muerto, el subsistema de captura de parámetros
por voz está vivo y en el camino principal, enganchado en dos puntos:

- `integration/voice_bootstrap.py:81-88` — el `PromptedCommandExecutor` se pasa
  como `on_execute` del `Browser`: **todo comando que ejecuta el Browser pasa por
  él**.
- `speech/dav_voice_service.py:338-346` — en modo CAD cada frase se ofrece primero
  al `PromptVoiceRouter`; si hay un prompt activo esperando un valor, la frase se
  la queda y no llega al Browser.

Tiene cobertura en `Dav/scr/validation/test_integration.py`.

> ⚠️ `_dispatch_to_active_prompt` envuelve el router en `except Exception: return
> False`. Si InputPrompts falla, la frase sigue de largo al Browser **sin ninguna
> señal** de que algo se rompió. Difícil de diagnosticar; considerar loguear la
> excepción aunque se siga tragando.

### 9.d Qué hacer — NO escribir una GUI nueva

Sería el cuarto sistema paralelo. El problema no es que falte una GUI: es que
sobran dos. A ya tiene Browser, InputPrompts, tests, temas e i18n.

Orden sugerido:

1. **Declarar A como camino oficial.** Ya lo es de hecho, pero no está escrito —
   por eso los tres siguen conviviendo.
2. **Retirar `PruebaIntegracion/`** junto con sus puentes muertos
   (`cad_session.py`, `cad_voice_adapter.py`). Preferible moverlo a
   `Dav/docs/prototipos/` antes que borrarlo: conserva el trabajo como referencia
   de diseño sin aparentar código activo.
3. **Migrar `InterfazDAV` a leer de `Dav/dic/`.** Es el paso de mayor valor:
   elimina el diccionario duplicado y hace que un comando nuevo sirva en ambas
   interfaces. Coordinar con Mica Saul (autora principal de `MainWindow.py`) y
   combinarlo con `plan-migracion-hilos-qthread.md`, que ataca el mismo archivo.
4. **Decidir si B sobrevive.** Si tras migrar hace lo mismo que A, fusionar. Si
   aporta algo propio (interfaz flotante más liviana, historial, minimizar),
   dejarla como vista alternativa **sobre el mismo motor**.

> **Sin verificar:** no se auditó `MainWindow.py` en detalle, así que no se sabe
> cuánto de su comportamiento depende del formato de `DiccionarioPrueba/`. Si esa
> estructura difiere bastante de `Dav/dic/`, el paso 3 es más trabajo del que
> sugiere este plan. Estimar antes de comprometerlo en un sprint.

Esta es una decisión de arquitectura que toca código de varias personas (Luigi
Mete, Mica Saul, Franco Camen) — conviene discutirla en el grupo antes de mover
archivos, no resolverla por commit.

## 11. Limpieza de vocabulario: claves internas y anglicismos (2026-08-08)

Al cruzar el vocabulario del árbol `Dav/dic/` contra el del modelo Vosk
aparecieron 89 palabras que el reconocedor **no puede emitir** —no están en su
vocabulario—, pero **no eran todas el mismo problema**. Separadas por causa, sólo
una categoría era limitación del modelo; el resto era deuda técnica del
diccionario, corregida en esta sesión.

**Resultado: 89 → 66 palabras fuera de vocabulario (11,5 % → 8,9 %).**

### 11.a Claves internas de FreeCAD filtradas como frases habladas

Identificadores copiados tal cual al `TraduceToEs.py`. **Inejecutables por voz**
—nadie dice "guion bajo"— con gramática o sin ella.

| Antes | Ahora | Archivo |
| --- | --- | --- |
| `vista_2d`, `proyeccion_2d` | "vista dos de", "proyección dos de", "vista plana" | `DraftWork/modification` |
| `resaltar_subelemento` | "resaltar subelemento" | `DraftWork/modification` |
| `cable_a_bspline` | "convertir a curva", "cable a curva", "alambre a curva" | `DraftWork/modification` |
| `cancelaredit` | eliminada (ya existía "cancelar edición"); + "cancelar" | `Sketcher` |
| `radiam` | "cota radio diámetro", "radio o diámetro" | `Sketcher/constraints` |
| `ldm` | eliminada; + "lista de piezas" | `Assembly` |

> `radiam` no era un error de tipeo: es la clave real de FreeCAD
> (`Radius/Diameter Dimension`, `constraints.py:46`) filtrada al diccionario
> hablado. Mismo bug, distinto origen.

**Al agregar comandos:** la clave interna va en el `<nombre>.py`; en el
`TraduceTo*.py` van **frases pronunciables**, nunca el identificador.

### 11.b Anglicismos redundantes — eliminados

Cada uno ya tenía sinónimo en español en el mismo archivo, así que sólo agregaban
un competidor fonético mal fonetizado:

`extrude` · `fillet` · `chamfer` · `sweep` (×2) · `cross sections` ·
`paint face` · `toolbars` · `validate` · `draft` · `draftwork` · `partdesign` ·
`part design` · `sketcher` · `techdraw` · `workbench dialog` ·
`workbench window`

> **`bom`** (*Bill of Materials*, `Assembly`) **se conservó**, pero es candidata a
> revisión: es una palabra de una sílaba que en español compite con "con", "son",
> "don", "van". A diferencia de `dxf` o `svg` —que se deletrean y por eso tienen
> redundancia fonética— "bom" se pronuncia como sílaba única, justo el perfil de
> palabra corta que el reconocedor confunde. Se mantiene porque es la
> sigla que el equipo usa; tiene además tres alternativas seguras en el mismo
> contexto ("lista de materiales", "tabla de materiales", "lista de piezas"). Si
> aparecen falsos positivos al probar por voz, es la primera que hay que sacar.

### 11.c Anglicismos sin alternativa — se les dio una

| Antes | Ahora |
| --- | --- |
| `facebinder`, `binder` | "unir caras", "unión de caras", "aglutinante" |
| `workbench`, `workbenches` | "banco de trabajo", "bancos de trabajo", "entorno de trabajo" |

### 11.d Errores de tipeo

- `chanflear` → `chaflanar` + `biselar` (`chanflear` no es palabra del español)
- `"options"` → `"opciones"` en `Part/part_color_per_face`

### 11.e Pendiente sin resolver

- **`colisa`** (`Sketcher/oblong`, `Sketcher/slot`) — puede ser "coliso" mal
  escrito (la ranura alargada, *slot*/*oblong*) o terminología que usa el equipo.
  **No se tocó**: no conviene cambiar vocabulario técnico por conjetura.
  Confirmar con alguien del equipo.
- **`dxf` / `svg`** — se dejaron. Ya tienen "formato de intercambio de dibujo" y
  "gráficos vectoriales escalables" al lado, y las siglas deletreadas son
  plausibles de reconocer.

### 11.f Verificación

`base.py` importa limpio con stubs de FreeCAD y las 5 claves de nivel superior
siguen en pie (`explorer`, `stdview`, `workbench`, `lineattributes`,
`preferences`). 2.344 frases, 1.414 únicas, sin errores de sintaxis.

> **No verificado:** no se corrieron los tests ni se probó dentro de FreeCAD. Los
> cambios son de claves habladas, no de callables, pero conviene una pasada por
> voz sobre los contextos tocados (Sketcher, Part, DraftWork, Assembly, StdView).
