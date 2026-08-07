# Pendientes DAV — hallazgos de sesión de auditoría de diccionarios y navegación por voz

## 1. Vosk reconoce con vocabulario abierto, no acotado al contexto

**Dónde:** `Dav/scr/ComponentesDAV/InterfazDAV/VoiceWorker.py:56`

```python
recognizer = vosk.KaldiRecognizer(model, 16000)
```

El `KaldiRecognizer` se crea sin gramática restringida (`SetGrammar`), así que Vosk compite contra todo el vocabulario del modelo español en cada frase, en vez de limitarse a los comandos válidos del contexto actual (`Browser.Context` ya tiene esa lista disponible en todo momento).

**Síntoma observado:** palabras cortas o poco frecuentes se transcriben mal — "croquis" salió como "crockett", apareció "traffic" sin que nadie lo dijera. Con el modelo pequeño (`vosk-model-small-es-0.42`, 39 MB) el efecto es más marcado que con el modelo grande.

**Arreglo sugerido:** pasarle a `KaldiRecognizer` una gramática JSON con las palabras/frases de `Browser.Context` (o `BaseContext` si aún no se descendió), actualizándola cada vez que cambia el contexto de navegación. Debería reducir bastante las transcripciones erráticas.

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
