# Pendientes DAV — hallazgos de sesión de auditoría de diccionarios y navegación por voz

> Lo ya resuelto está en [`completados-dav.md`](completados-dav.md), con la causa
> real de cada caso. Este documento es sólo lo que sigue abierto.

## 3. Palabras ambiguas entre workbenches (parcialmente resuelto)

> La gramática acotada (ver [`acortador-gramatica-vosk.md`](acortador-gramatica-vosk.md))
> baja bastante el riesgo: dentro de un contexto compiten ~12 frases, no 100.001.
> Pero **no elimina la ambigüedad**: si dos frases parecidas están en el mismo
> nivel, Vosk las sigue pudiendo confundir. Esta sección sigue vigente.

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
| Minimizarse | Hecho: lo da el `QDockWidget` que contiene al `DavPanel`. |
| Dar historial | Hecho: `DavPanel._BuildHistoryColumn()` + `AddToHistory`, alimentado por `browser_voice_adapter`. Falta **probarlo por voz dentro de FreeCAD**. |

Los dos últimos quedaron cubiertos al unificar la GUI en el panel acoplado (ver [`completados-dav.md`](completados-dav.md), «Panel DAV acoplado a FreeCAD»).

**Otros pendientes transversales:**

- Idiomas **en** y **pt**: el árbol está armado para tres idiomas, pero sólo el español está completo. Si el MVP se demuestra en español, documentarlo como alcance y no como bug.
- Gramática restringida de Vosk — resuelta, ver [`acortador-gramatica-vosk.md`](acortador-gramatica-vosk.md).
- Tests: `tests/test_browser.py` (21 casos) usa un loader mock. **No hay tests que corran contra el árbol real `Dav/dic/`**, que es donde aparecieron todos los bugs de esta sesión (imports rotos, aplanado, acentos). Vale la pena agregar un test de integración que recorra las rutas principales.

## 10. Hallazgo contrafáctico: un modelo de voz más grande NO mejora el reconocimiento de comandos

**Premisa inicial del proyecto:** se asumió que, si el reconocimiento fallaba, la
solución era subir a un modelo Vosk más grande — `vosk-model-es-0.42` (1.4 GB) en
lugar de `vosk-model-small-es-0.42` (39 MB).

**Resultado:** la premisa no aplica a DAV. Para un conjunto cerrado de comandos,
agrandar el modelo **empeora** el problema en vez de resolverlo. La precisión no
se arregla cambiando de modelo: se arregla restringiendo la gramática (ver [`acortador-gramatica-vosk.md`](acortador-gramatica-vosk.md)).

### 10.a Por qué la premisa era razonable

"Modelo más grande = mejor reconocimiento" es cierto en el dominio para el que
normalmente se mide el ASR: **dictado libre**. La métrica de referencia es el WER
(*word error rate*) sobre habla espontánea, y ahí más vocabulario y un modelo de
lenguaje más rico efectivamente bajan el error.

El README del modelo que usamos trae sus propios números medidos:

```
%WER 42.63  decode_test_call    (habla telefónica)
%WER 16.02  decode_test_cv      (Common Voice — gente leyendo frases)
%WER 11.21  decode_test_mls     (Multilingual LibriSpeech — audiolibros)
%WER 16.72  decode_test_mtedx   (charlas TEDx)
```

Entre 11 % y 43 % de error por palabra. Ese es el eje sobre el que se planteó la
hipótesis original, y sobre ese eje el modelo grande **sí** gana. El problema es
que ese no es nuestro eje.

Nótese además sobre qué está entrenado: audiolibros, charlas y voluntarios
leyendo oraciones. **El modelo no sabe nada de ingeniería ni de CAD.**

### 10.b Anatomía del modelo: acústico vs. lenguaje

Vosk (Kaldi por debajo) descompone el reconocimiento en piezas separables. La
distinción es la que sostiene todo este hallazgo:

```
audio → [MODELO ACÚSTICO] → fonemas → [LÉXICO] → palabras candidatas
                                                        ↓
                                              [MODELO DE LENGUAJE]
                                                        ↓
                                            secuencia más probable
```

| | Modelo acústico | Modelo de lenguaje |
| --- | --- | --- |
| Archivo | `am/final.mdl` (16,1 MB) | `graph/Gr.fst` (21,8 MB) |
| Qué hace | sonido → fonemas | fonemas → palabras plausibles |
| Entrenado sobre | audio + transcripciones | **texto** (audiolibros, TEDx) |
| Depende del dominio | poco | **muchísimo** |
| ¿Sirve para comandos? | **sí, entero** | **no — estorba** |
| ¿Sustituible? | no | **sí, por una gramática** |

- El **acústico** toma la onda, la corta en ventanas de ~25 ms, extrae MFCC y una
  red TDNN responde qué fonema suena. No sabe qué es una palabra: sabe cómo suena
  el español. Es lo caro de entrenar, es genérico, y **hace falta entero**.
- El **léxico** (dentro de `HCLr.fst`) mapea palabra → fonemas. Define qué
  palabras *pueden* existir.
- El de **lenguaje** es un n-grama sobre texto: desempata cuando el acústico duda
  ("60 % /kasa/, 40 % /kaθa/" → gana "casa" porque es más frecuente).

**El overkill está en el modelo de lenguaje, no en el acústico.** Su estadística
viene de texto corriente, donde un imperativo aislado como "chaflán" es rarísimo:
el prior trabaja en contra nuestra. Pasar una gramática a `KaldiRecognizer`
**reemplaza el `Gr.fst`** y conserva el acústico — se descarta la pieza que no
aplica y se conserva la difícil.

### 10.c Las cifras, medidas sobre el modelo y el árbol reales

Vocabulario extraído de la tabla de símbolos embebida en `graph/Gr.fst`
(`flags=3`, symbol table `exp/chain_d/tdnn/lgraph/words.txt`):

| | |
| --- | --- |
| Símbolos totales | 100.006 |
| Especiales (`<eps>`, `[unk]`, `#0`, `<s>`, `</s>`) | 5 |
| **Palabras reales** | **100.001** |
| Estados en el grafo de lenguaje | 335.886 |
| Tamaño en disco del modelo | 60,3 MB |

Vocabulario que DAV realmente usa (122 archivos `TraduceToEs.py`, tras la
limpieza de §11):

| | |
| --- | --- |
| Frases totales | 2.344 |
| Frases únicas normalizadas | 1.414 |
| **Palabras distintas** | **745** |

**745 / 100.001 ≈ 0,75 %.** El reconocedor carga ~134 veces más vocabulario del
que el proyecto usa. Las primeras entradas del vocabulario lo ilustran mejor que
cualquier argumento: `aa`, `aaa`, `aaah`, `aang`, `abacial`, `abadejo` — todas
candidatas activas cada vez que alguien dice un comando.

Pero el número decisivo es otro, porque **la gramática se carga por contexto**:

| Contexto | Frases |
| --- | --- |
| Máximo (`Workbench/Sketcher`) | 108 |
| `Workbench/Part` | 99 |
| `Assembly/joint` | 97 |
| `StdView/StandardViews` | 86 |
| **Mediana de los 122 contextos** | **12** |
| Mínimo | 6 |

En el contexto típico DAV necesita **12 frases**, contra 100.000 palabras: un
factor de ~8.000×.

### 10.d El otro hallazgo: el modelo también se queda corto

Medición inversa — cuántas palabras de DAV **no existen** en el vocabulario del
modelo. Son imposibles de reconocer: no es que se reconozcan mal, es que Vosk
nunca puede emitirlas.

**66 de 745 palabras (8,9 %) están fuera de vocabulario.** Entre ellas:

`chaflán` · `chaflanar` · `biselar` · `extruir` · `espejar` · `intersecar` ·
`isométrica` · `axonométrico` · `dimétrica` · `trimétrica` · `anaglifo` ·
`heptágono` · `octágono` · `hiperbólico` · `diametral` · `desmoldeo` ·
`multitransformación` · `texturización` · `polilínea` · `multilínea` ·
`bspline` · `nurbs` · `bézier` · `spline` · `wireframe` · `sustractiva` ·
`booleana` · `perpendicularidad` · `preseleccionar` · `subforma`

Es exactamente el núcleo del vocabulario CAD. Cuando el usuario dice "chaflán",
el decoder está **obligado** a devolver otra cosa. Esto explica los síntomas de
la gramática abierta mejor que la hipótesis del ruido: "croquis" tampoco está en el vocabulario, y
por eso salió "crockett" — el vecino fonético más probable del español general.

> El modelo es simultáneamente **demasiado grande y demasiado chico**: sobra en lo
> que no usamos y falta en lo que sí.

Y el modelo grande tampoco resuelve esto de forma confiable: pasar de 100k a
~300k palabras del español general agrega más `abadejo`, no `chaflán`. El corte
sigue siendo por frecuencia en audiolibros y charlas, donde "chaflán" es raro por
más corpus que se agregue. Alguna entraría, pero por casualidad estadística, no
por diseño.

La gramática restringida **sí** lo resuelve: al pasar una lista de frases, Vosk
las fonetiza y las mete en el grafo de decodificación. Las palabras fuera de
vocabulario dejan de ser imposibles y pasan a ser las únicas candidatas.

> ⚠️ **Salvedad a verificar:** hay que comprobar caso por caso que el G2P del
> modelo fonetice razonablemente los anglicismos que sobrevivan (`bspline`,
> `nurbs`, `wireframe`). El fonetizador español puede darles una pronunciación
> que no coincida con cómo los dice la gente. Es una razón medida más para la
> regla de §3: usar siempre el sinónimo en español como forma principal.

### 10.e La formulación correcta

La variable que importa no es el tamaño del modelo, sino la **relación entre el
vocabulario del reconocedor y el vocabulario de la tarea**. Cuanto más cerca de 1
esté esa relación, mejor:

- El modelo grande la **empeora** (más vocabulario, misma tarea).
- La gramática restringida por contexto la lleva **casi a 1**.

Dicho de otro modo: la hipótesis original optimizaba la *capacidad* del
reconocedor, cuando lo que había que optimizar era su *especificidad*.

### 10.f Consecuencia de diseño

Se mantiene `vosk-model-small-es-0.42` y se ataca la precisión por el lado de la
gramática:

| | Modelo grande, sin gramática | Modelo chico + gramática por contexto |
| --- | --- | --- |
| Precisión en comandos | peor | mucho mejor |
| Palabras compitiendo | ~300.000 | ~12 (mediana por contexto) |
| Vocabulario CAD fuera de alcance | sí | **no** (se inyecta en la gramática) |
| Latencia por frase | alta | baja |
| RAM | ~1,4 GB | ~50 MB |
| "No entendí" explícito | no (devuelve lo más parecido) | sí (`[unk]`) |

El `[unk]` es un beneficio aparte: hoy el reconocedor **siempre** devuelve algo,
aunque el usuario haya dicho una frase que no es un comando. Con gramática
cerrada, "no entendí" pasa a ser un estado explícito que la GUI puede mostrar en
vez de ejecutar una acción equivocada.

Encaja directamente con el árbol `Dav/dic/`: **el contexto activo del `Browser` ya
sabe qué comandos son válidos**. Al entrar a `explorer` la gramática son las hojas
de `explorer` + `NavCommands`; al bajar a `file` se regenera con las de `file`.

```python
import json
from vosk import KaldiRecognizer

# frases válidas del contexto actual + comandos de navegación + [unk]
frases = Browser.Context.SpokenPhrases() + NavCommands.SpokenPhrases() + ["[unk]"]
recognizer = KaldiRecognizer(model, 16000, json.dumps(frases, ensure_ascii=False))
```

> **Sin medir todavía:** este análisis explica los síntomas de la gramática
> abierta y de §3, y se apoya
> en cifras reales de vocabulario, pero **no se corrió un benchmark de tasa de
> acierto**. Antes de presentarlo como resultado experimental en un informe
> conviene medirlo: ~30 comandos, 5 repeticiones, 2 o 3 hablantes, contando
> aciertos en cuatro condiciones (chico/grande × con/sin gramática). Es barato y
> convierte el argumento en dato.

### 10.g Corolario sobre sinónimos repetidos

Restringir el vocabulario le da peso a otra regla que ya existe: **una frase
hablada no puede mapear a dos callables distintos dentro del mismo contexto**. Con
gramática cerrada el reconocedor va a acertar la frase, pero el `Browser` no va a
saber cuál ejecutar.

Es el mismo problema de aplanar subcontextos de §4 (`create`, `help`, `center`
colisionando). Con subcontextos correctamente anidados casi desaparece, porque
cada frase sólo necesita ser única **dentro de su nivel** — razón adicional para
no aplanar nunca.

## 11. Limpieza de vocabulario: claves internas y anglicismos (2026-08-08)

Al medir §10.d aparecieron 89 palabras que el reconocedor **no puede emitir** —no
están en su vocabulario—, pero **no eran todas el mismo problema**. Separadas por
causa, sólo una categoría era limitación del modelo; el resto era deuda técnica
del diccionario, corregida en esta sesión.

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
> palabra corta que el reconocedor confunde (§10.d). Se mantiene porque es la
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

## 12. Integrar las clases de `Dav/scr/selection/` al programa (2026-08-09)

**Dónde:** `Dav/scr/selection/` — `createobjects.py` (`CreateObjects`),
`tagger.py` (`Tagger`, `LanguageCode`), `object_selection.py` (`ObjectSelection`).

Sirven para el requisito de GUI **"dar historial (navegar objetos creados)"** y
para el `plan_arbol_de_objetos_navegable.md`: `CreateObjects` descompone una
forma en sus sub-elementos (caras/aristas en 3D, líneas/puntos en 2D) y los
publica como objetos reales del documento; `Tagger` les pone nombre localizado
(`Punto1`, `Linea2`, `Superficie3`) leyendo `Preferences.SetLanguage`;
`ObjectSelection` los recorre resaltándolos de a uno en la vista 3D y el árbol.

### 12.a La integración está empezada, no ausente

Hay que decirlo porque cambia el trabajo: **40 archivos de `Dav/dic/` ya
importan `CreateObjects`** (51 llamadas), y `InitGui.py:58` ya llama a
`_ensure_selection_path()`. No es "conectar algo desconectado" —es **terminar y
arreglar una integración a medio hacer**. Lo que sí está desconectado es
`ObjectSelection`: no lo referencia nadie fuera de su propio archivo.

### 12.b Tres bugs que hacen que hoy no funcione

**1. `Execute()` no recibe el objeto — 10 archivos.** La firma real es
`CreateObjects(ObjectName, Is3D)` + `Execute()` sin argumentos: el objetivo se
resuelve en el `__init__` vía `GetObjectByName()`. Pero `DraftWork` llama:

```python
# Dav/dic/Workbench/DraftWork/circle/circle.py:14 — INCORRECTO
CreateObjects(Is3D=False).Execute(obj)
```

Falla dos veces: `ObjectName` es obligatorio (`TypeError` en el constructor) y
`Execute()` no acepta parámetros. Afecta a `annotation`, `arc`, `circle`,
`creation`, `curve`, `dimension`, `ellipse`, `facebinder`, `modification` y
`modify`. La forma correcta —la que usa `Part/`— es:

```python
CreateObjects(ObjectName=App.ActiveDocument.ActiveObject.Name, Is3D=False).Execute()
```

**2. `.execute()` en minúscula.** `Drafting/drafting.py:22` llama
`CreateObjects(obj.Name, Is3D=False).execute()`. El método es `Execute()`
(PascalCase, según la convención del proyecto): `AttributeError`. Es justo el
callable de la clave hablada `"createobjects"`, o sea el comando más directo
para probar esto por voz.

**3. Los dos `import` fallan si `InitGui.py` no corrió.** El patrón repetido en
los 40 archivos es:

```python
try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
```

`_ensure_selection_path()` inserta la carpeta `selection/` **misma** en
`sys.path`, no su padre — así que sólo puede funcionar la rama plana
(`from createobjects import ...`). La rama de respaldo `selection.createobjects`
necesitaría `Dav/scr/` en el path, y **`DictionaryLoader` sólo agrega `Dav/dic/`
y `ComponentesDAV/`**; nunca `Dav/scr/`. Verificado con stubs de FreeCAD: con
`Dav/scr` en el path importa `selection.createobjects`; sin él fallan las dos
ramas.

Consecuencia: si el árbol se carga sin pasar por `InitGui.py` (tests, consola
Python a mano, cualquier entrada que no sea el arranque del workbench), los 40
módulos revientan al importar. Y como `DictionaryLoader` **captura los errores
de import y sigue de largo** (§6), eso no se ve: los contextos aparecen vacíos
sin ningún mensaje. Es exactamente el modo de falla silenciosa de §6, con la
diferencia de que acá alcanza a diez carpetas de DraftWork y Part a la vez.

### 12.c Lo que falta decidir antes de tocar código

- **Dónde va el bootstrap del path.** Hoy depende de `InitGui.py`, que es el
  arranque del workbench, no la carga del diccionario. Lo consistente con §6 es
  que `DictionaryLoader` agregue `Dav/scr/` a `sys.path` junto con los otros
  roots, y que los diccionarios usen **una sola** forma de import
  (`from selection.createobjects import CreateObjects`), sin `try/except`. Así
  el árbol se puede importar sin FreeCAD y los tests dejan de depender del orden
  de arranque.
- **Si `CreateObjects` debe correr en cada creación.** Hoy cada comando de
  DraftWork/Part lo invoca después de dibujar, o sea que **toda** figura se
  descompone en sub-objetos automáticamente. Un rectángulo pasan a ser 4 líneas
  + 4 puntos en el árbol. Puede ser lo buscado (es lo que habilita "seleccionar
  la línea de arriba" por voz) o puede llenar el documento de ruido. Conviene
  confirmarlo con el equipo antes de arreglar las 51 llamadas: si no es lo
  buscado, la corrección no es cambiar la firma sino sacar la llamada.
- **`ObjectSelection` no tiene comandos de voz.** Es la pieza que faltaría para
  el requisito de historial navegable, y su API está pensada para consola
  (`Instancia.SelectOther = True` como *setter* con efecto). Para voz hay que
  envolverla —`siguiente objeto` / `anterior` / `seleccionar <nombre>`— y darle
  una carpeta en `Dav/dic/` con su `TraduceTo*.py`, anidada según §4. El setter
  con efecto colateral es cómodo en consola pero raro como API; conviene un
  `SelectNext()` explícito y dejar la property como alias.

### 12.d Cómo probarlo

`selection/console_helpers.py` ya trae `RunCreateObjects(...)` y
`dav_commands.RunAlexSelectionPrueba()` para la consola de FreeCAD, sin
configurar rutas. Es el camino más corto para ver qué hace la clase antes de
decidir lo de §12.c. Ojo con el docstring de `console_helpers.py`: dice que
*"el módulo DAV agrega selection/ a sys.path al iniciar"*, lo cual es cierto
sólo por `InitGui.py` — es la misma suposición que rompe fuera de FreeCAD.

> **Sin verificar:** no se probó dentro de FreeCAD. Los tres bugs de §12.b son
> de lectura de código y del test de imports con stubs; el comportamiento real
> de `CreateObjects` sobre geometría (si los sub-objetos quedan bien, si
> `recompute()` alcanza) no se ejerció.

---

## 13. Nombre dictado al crear un objeto + selección por ese nombre (2026-09-02)

Cierra dos de los tres puntos que §12.c dejaba abiertos: `ObjectSelection` ya
tiene comandos de voz, y el `seleccionar <nombre>` que ahí se pedía existe.

**Qué se pidió:** que al crear un objeto (un cuadrado, por ejemplo) el sistema
pida un nombre por voz, y que ese nombre sirva después para elegirlo en el
árbol de objetos.

### 13.a Aclaración de nombres

No existe ninguna clase `Trigger` en el repo — el único `Trigger()` es el del
`FlashOverlay` de `DavPanel` (efecto visual, sin relación). La clase es
**`Tagger`**. Y `CreateObjects`, pese al nombre, **no crea: descompone** un
objeto existente en sus sub-elementos.

### 13.b Un solo punto de intercepción, no 73

Las 73 llamadas de `Dav/dic/` a `CreateObjects` comparten la forma
`CreateObjects(<objeto recién creado>, Is3D=...).Execute()`. Por eso el pedido
del nombre se puso **dentro de `CreateObjects.Execute()`**, detrás del flag
`AskName=True`, en vez de editar los 73 sitios. Quien no quiera el prompt pasa
`AskName=False`.

### 13.c `obj.Name` es de sólo lectura

El nombre dictado **no puede** ir a `obj.Name`: FreeCAD lo fija al crear el
objeto y no admite reasignación. Va a `obj.Label`, que sí acepta espacios y
acentos y es lo que se ve en el árbol. Consecuencia directa: la búsqueda por
voz tiene que resolver **Label → objeto**, no Name; de ahí
`ObjectSelection.SelectByLabel()`, con comparación laxa (sin acentos, sin
mayúsculas, sin espacios) y match exacto con prioridad sobre el parcial.

Los duplicados se resuelven con sufijo (`mesa`, `mesa 2`), no pisando el label.

### 13.d Construir un QDialog sin QApplication aborta el proceso

Encontrado al probar: instanciar el `StringInputPrompt` fuera de FreeCAD **se
lleva el intérprete entero**, con salida vacía y exit code 9. No es una
excepción de Python — un `try/except Exception` alrededor **no la atrapa**, es
el mismo modo de falla que `SetGrammar` de Vosk (§10, `acortador-gramatica-vosk.md`).

Por eso `nameprompt._HasRunningGuiApp()` comprueba `QApplication.instance()`
**antes** de construir el diálogo, en vez de confiar en el `try/except`. Dentro
de FreeCAD siempre hay `QApplication`, así que el camino real no cambia; lo que
cambia es que la consola pelada y los tests degradan al nombre automático en
lugar de morir.

### 13.e El límite real: Vosk sólo oye lo que está en su gramática

Es la restricción que condiciona todo el circuito, y conviene decirla clara:

- **Al dictar el nombre nuevo**, Vosk sólo puede transcribir palabras de su
  vocabulario. "mesa" o "columna" funcionan; un nombre inventado o una sigla
  ("pieza A7") va a salir mal o como `[unk]`. El nombre dictado tiene que ser
  una palabra corriente del idioma.
- **Al buscar por nombre**, el label tiene que estar en la gramática activa o
  no se reconoce nunca — y `SetGrammar` **falla en silencio**, sin avisar.

Para lo segundo se agregó `ObjectNameGrammarSwitcher`, que arma la gramática
con los labels del documento (y además cada palabra suelta, porque la gramática
acota vocabulario, no sintaxis: "mesa chica" necesita "mesa" y "chica"). Se
engancha con el mismo mecanismo polimórfico del numérico
(`RequiresObjectNameGrammar()` en el prompt, como `RequiresNumericGrammar()`),
así que `PromptVoiceRouter` no necesita conocer tipos concretos.

### 13.f Archivos

| Archivo | Cambio |
|---|---|
| `scr/selection/tagger.py` | kind `object`; `ApplyCustomName`, `SanitizeSpokenName`, `NormalizeForMatch`, `_UniqueLabel` |
| `scr/selection/nameprompt.py` | **nuevo** — `AskObjectName`, `AskExistingObjectName`, guarda de `QApplication` |
| `scr/selection/createobjects.py` | flag `AskName`, método `RequestName()` |
| `scr/selection/object_selection.py` | `SelectByLabel()` + `_NormalizeForMatch()` |
| `InputPrompts/ObjectNameGrammarSwitcher.py` | **nuevo** — gramática con los labels |
| `InputPrompts/ObjectNameInputPrompt.py` | **nuevo** — prompt que declara esa gramática |
| `InputPrompts/PromptVoiceRouter.py` | engancha la gramática de nombres |
| `dic/Selection/selection.py` + `TraduceToEs.py` | hoja `byname` ("buscar", "por nombre"…) |

### 13.g Qué se verificó y qué no

**Verificado** (fuera de FreeCAD, con dobles): el `Tagger` nombra, desambigua
duplicados y cae al automático; `SelectByLabel` acierta con mayúsculas,
acentos y espacios, y falla limpio sin match; `CreateObjects.Execute()` sin GUI
aplica el nombre automático y sigue descomponiendo; la gramática se arma con
labels + palabras sueltas; el router discrimina el prompt de nombres del
numérico. Los 5 tests de `validator` siguen pasando.

> **Sin verificar:** nada de esto se probó **dentro de FreeCAD** con micrófono.
> Falta confirmar (a) que el pop-up aparezca y no bloquee la creación, (b) que
> Vosk reconozca de verdad un label agregado a la gramática en caliente, y (c)
> que el `Reset()`+`SetGrammar` del switcher no tumbe el proceso como en §10.
> El punto (c) es el de mayor riesgo: `set_grammar` sólo encola y el loop de
> audio hace el `Reset()`, que es el orden seguro, pero no se ejerció en vivo.
>
> Los 9 errores de `validation/run_tests.py` (`No module named 'InputPrompts'`)
> son **preexistentes** — se reproducen igual revirtiendo estos cambios.

### 13.h Falta de §12.c

Sigue abierto el tercer punto: decidir si `CreateObjects` debe correr en **cada**
creación. Hoy un rectángulo se vuelve 4 líneas + 4 puntos en el árbol.

El prompt de nombre **no** multiplica ese ruido: `RequestName()` se llama una
sola vez por `Execute()`, sobre el objeto padre y antes de descomponerlo; los
sub-elementos los sigue nombrando el `Tagger` solo (`Linea 1`, `Punto 2`). Un
pop-up por creación, no uno por sub-objeto. Pero si el equipo decide que la
descomposición automática es ruido, sacar la llamada se lleva puesto también el
pedido de nombre — habría que reubicarlo en las primitivas.

---

## 14. Vosk pierde la primera palabra de una frase larga (2026-09-02)

**Síntoma real**, del log de una sesión en `Base > workbench > sketcher >
geometry > rectangle`, con el contexto correcto y el comando disponible:

```
[DAV] Voz: ventana por esquinas   → Ignorado: Command not found in upward search
[DAV] Voz: banco por esquinas     → Ignorado: Command not found in upward search
[DAV] Voz: atrás por esquinas     → Ignorado: Command not found in upward search
[DAV] Voz: por esquinas           → Ignorado: Command not found in upward search
```

El usuario decía **"rectangulo por esquinas"**, que existe y está bien
registrada en `Geometry/rectangle/TraduceToEs.py`.

### 14.a El patrón

**"por esquinas" se reconoce siempre; la primera palabra nunca.** Y las tres
sustituciones —"ventana", "banco", "atrás"— son palabras de la **gramática
global**, activas en cualquier contexto: "ventana" viene de Explorer, "banco"
del prefijo de "banco de trabajo", "atrás" de NavCommands.

Es el límite de §10 / `acortador-gramatica-vosk.md` visto en la práctica: **la
gramática acota el vocabulario, no la sintaxis.** Vosk arma "banco por
esquinas" combinando palabras válidas de contextos distintos, aunque esa frase
no exista en ningún diccionario. Después `ProcessPhrase` busca la frase
completa, no la encuentra en ningún nivel, y responde "not found in upward
search" — que suena a problema de navegación pero es de reconocimiento.

Agravante local: en el nivel `Geometry` conviven **"recta"** (→ line) y
**"rectangulo"** (→ rectangle), acústicamente cercanas y una prefijo de la otra.

### 14.b El arreglo: sinónimos que no repitan la palabra conflictiva

Se agregaron a `Geometry/rectangle/TraduceToEs.py` ocho frases que **no
contienen "rectangulo"**, apoyándose en que el log demuestra que "por esquinas"
sí se reconoce bien:

```
por esquinas · por puntos · por coordenadas · esquinas
coordenadas · medidas · por medidas · dictar medidas
```

Dentro de la carpeta `rectangle` no hay ambigüedad posible: la figura ya está
decidida por el contexto. Verificado que ninguna de las ocho colisiona con
`Dav/dic/TraduceToEs.py` ni con `NavCommands/`, así que no compiten con la
gramática global; y que no hay claves duplicadas en el archivo (§4: la última
gana, en silencio).

**No se tocó el motor** — es sólo diccionario, como pide la convención.

### 14.c La regla general que deja

Cuando una frase de varias palabras no se reconoce **y el contexto es el
correcto**, antes de sospechar del árbol de navegación conviene mirar el log:
si parte de la frase llega siempre bien y otra parte varía, es competencia
acústica contra la gramática global, no un problema de diccionario.

El remedio es el mismo: **darle a ese comando un sinónimo corto que no comparta
palabras con la gramática global**, aprovechando que el contexto ya desambigua.
Conviene tenerlo en cuenta al escribir `TraduceTo*.py` nuevos: una frase larga
que empieza con una palabra frecuente en otros contextos es frágil.

> **Pendiente:** replicar los sinónimos en `TraduceToEn.py` y `TraduceToPt.py`
> de esa carpeta, que siguen teniendo sólo las frases largas. Y revisar si otras
> hojas con frases de 3+ palabras sufren lo mismo — no se auditó el árbol
> entero.

---

## 15. El pop-up de nombrado no cambiaba la gramática (2026-09-02)

**Bug de diseño de §13**, encontrado probando dentro de FreeCAD.

**Síntoma:** al crear un objeto y dictar su nombre, "cubo" y "cuadrado" no se
reconocían nunca. El buscador (`seleccion` → `buscar`) sí funcionaba.

### 15.a La causa

`StringInputPrompt` **no declara ninguna gramática**. Mientras el pop-up de
nombrado estaba abierto, la gramática activa seguía siendo la del contexto de
navegación — las ~12 frases de la carpeta donde estaba parado el usuario
(`crear`, `centro`, `por esquinas`, `ayuda`…). "cubo" no estaba entre ellas,
así que Vosk no podía transcribirlo: es §10 otra vez.

La asimetría con el buscador es reveladora: para *buscar* sí se había hecho el
switcher (`ObjectNameGrammarSwitcher`, §13.e), porque los labels existen en el
documento y hay de dónde sacarlos. Para *nombrar* se asumió que el prompt
capturaba texto libre — y **texto libre no existe en Vosk**: sólo puede elegir
entre las frases de su gramática.

### 15.b La solución: vocabulario cerrado en el diccionario

Nombrar un objeto nuevo no puede apoyarse en el documento (el nombre todavía no
existe), así que necesita una lista propia. Se creó **`Dav/dic/ObjectNames/`**
con la estructura de cualquier diccionario DAV:

| Archivo | Qué tiene |
|---|---|
| `ObjectNames.py` | `GetObjectNamePhrases(lang)` y `ResolveObjectName(spoken, lang)` |
| `TraduceToEs.py` | 56 nombres: formas, piezas mecánicas, muebles, genéricos |
| `TraduceToEn.py` / `TraduceToPT.py` | los mismos en inglés y portugués |

**Agregar un nombre es agregar una línea al `TraduceTo*.py`** — misma convención
que el resto del árbol, sin tocar Python.

El mapeo es `frase hablada → etiqueta escrita`, así que la palabra dictada puede
diferir de lo que se escribe en el árbol ("cubo" → `Cubo`).

### 15.c Tres gramáticas, un solo mecanismo

Quedaron tres switchers, todos enganchados por el mismo hook polimórfico en
`PromptVoiceRouter` (`Requires*Grammar()` en el prompt, sin que el router
conozca tipos concretos):

| Prompt | Gramática | De dónde sale |
|---|---|---|
| `IntegerInputPrompt` / `Float…` | números | `Dav/dic/Numbers/` |
| `NewObjectNameInputPrompt` | nombres dictables | `Dav/dic/ObjectNames/` |
| `ObjectNameInputPrompt` | labels del documento | objetos activos |

Verificado que cada prompt pide **exactamente una** y no se pisan.

### 15.d Bug aparte: la extrusión se llamaba "mesa 2"

Al extruir un objeto llamado "mesa", el resultado quedaba como **"mesa 2"** en
vez de tomar el nombre dictado.

**Causa:** FreeCAD copia el Label del objeto base al derivado — la extrusión de
"mesa" **nace llamándose "mesa"**. `_UniqueLabel` veía ese label ya ocupado (por
el propio objeto que estaba por renombrar) y le agregaba el sufijo. Cuando Vosk
además no entendía el nombre dictado, el fallback se aplicaba sobre un objeto ya
llamado "mesa" y salía "mesa 2".

**Arreglo:** `_UniqueLabel(label, obj)` excluye al propio objeto del chequeo de
duplicados. Los duplicados reales (otro objeto con ese label) siguen
desambiguando con sufijo.

> **Sin verificar dentro de FreeCAD:** que Vosk reconozca de verdad las 56
> palabras del vocabulario en caliente, y que el tercer cambio de gramática no
> tumbe el proceso (§10). Lo verificado es sin FreeCAD: que el vocabulario carga
> en los tres idiomas, que el router discrimina las tres gramáticas, y que el
> label heredado ya no genera "mesa 2".

---

## 16. Gramática contaminada: idiomas mezclados y ruido de sub-elementos (2026-09-02)

Dos hallazgos de la misma sesión de prueba en FreeCAD, ambos sobre **qué entra
en la gramática** de los pop-ups.

### 16.a Palabras de otros idiomas robándole el audio al español

**Síntoma:** en el pop-up de nombre sólo funcionaban "aceptar" y "enviar";
"confirmar", "entrar" y "ok" no. Además se veían **palabras en inglés** en la
interfaz de reconocimiento.

**Causa:** `SpokenNumberParser.ConfirmationWords` junta los **tres idiomas a la
vez** — y eso está bien para *aceptar* la palabra escrita (uno puede decir "ok"
con la interfaz en español). El error fue que los switchers volcaban ese
conjunto entero **en la gramática de Vosk**:

```
accept · send · enter · confirm · discard · never mind · aceitar · cancelamento
```

Con el modelo español esas palabras **no se pueden reconocer nunca** (no están
en el modelo acústico), pero **compiten igual por el audio** y le ganaban a las
válidas. De ahí que sólo sobrevivieran dos.

**Arreglo:** `InputPrompts/GrammarLanguageFilter.py` — clasifica cada palabra
por idioma leyendo `NavCommands/TraduceTo*.py`, y los switchers filtran por el
idioma activo. Un sinónimo agregado al diccionario se clasifica solo.

Verificado: la gramática pasó de 10 palabras de confirmación mezcladas a las 8
españolas, con **cero** en inglés.

> Distinción que conviene no perder: **aceptar una palabra** (los tres idiomas,
> en `SpokenNumberParser`) y **poder oírla** (un solo idioma, en la gramática)
> son cosas distintas. Mezclarlas fue el bug.

### 16.b Los sub-elementos ahogaban el nombre del usuario

**Síntoma:** con un objeto llamado "Rectangulo" en el árbol, el buscador no lo
reconocía.

**Causa:** no era la gramática —"rectangulo" sí entraba— sino la competencia.
`CollectLabelPhrases` agregaba cada label **y cada una de sus palabras
sueltas**. Un rectángulo descompuesto deja 8 sub-elementos, así que la gramática
recibía `linea`, `punto`, `1`, `2`, `3`, `4`… : once competidores, todos ruido
de la descomposición automática, contra el único nombre que el usuario puso.

**Arreglo:** las palabras sueltas se agregan **sólo para etiquetas que puso el
usuario**. Las autogeneradas por el `Tagger` (`<tipo> <número>`) entran nada más
con su label completo, así "linea 1" se sigue pudiendo seleccionar.

Qué cuenta como autogenerado sale de **`Dav/dic/Tagger/TaggerKinds.py`**, no de
código: si `tagger.py` gana un tipo, se agrega la palabra ahí en los tres
idiomas.

Verificado sobre un árbol real (1 rectángulo + 8 sub-elementos): la gramática
bajó de 26 a 20 frases y "rectangulo" quedó como **única palabra suelta**, sin
nada parecido compitiendo.

### 16.c La regla que dejan los dos

**Todo lo que entra a una gramática le compite el audio a lo demás.** Vale la
pena preguntarse, por cada frase que se agrega, si el usuario la va a decir de
verdad en ese momento: una palabra que nunca va a decir no es neutral, empeora
el reconocimiento del resto. Es la misma lección de §14, ahora del lado del
código que arma la gramática y no del diccionario.

> **Sin verificar dentro de FreeCAD:** los dos arreglos se probaron con dobles.
> Falta confirmar en vivo que "confirmar"/"entrar" respondan y que "rectangulo"
> se reconozca al buscar.

---

## 17. El prompt de texto exigía nombre y confirmación en la misma frase (2026-09-02)

**Síntoma, reportado con precisión desde una prueba en FreeCAD:** en los pop-ups
numéricos se puede decir "cero", esperar a que cambie el mensaje de estado, y
recién después "aceptar". En el de texto (nombrar / buscar) había que decir
**todo seguido y rápido**: si el mensaje alcanzaba a cambiar, la confirmación ya
no servía.

### 17.a La causa

`NumericInputPrompt` **acumula** el texto entre frases en `_AccumulatedText`, y
lo parsea recién cuando llega la confirmación. `StringInputPrompt` no lo hacía:
esperaba nombre y confirmación **en una sola frase**.

Al dictar por separado, la segunda frase llegaba con la confirmación sola. Sin
el nombre, `_StripConfirmation` la dejaba vacía y el prompt fallaba con "Text
value cannot be empty" — o se quedaba esperando, según el caso.

No era un timeout, aunque lo pareciera: era que cada frase se evaluaba aislada.

### 17.b El arreglo

`StringInputPrompt.ProcessFinalText` ahora usa el mismo patrón acumulativo del
numérico. La confirmación se acepta tanto sola ("aceptar") como cerrando la
frase ("rectangulo aceptar").

Beneficio extra: un nombre de dos palabras se puede dictar en partes —
"tapa" → "superior" → "aceptar" da `tapa superior`. Antes había que decirlo de
corrido y esperar que Vosk lo tomara entero.

Lo heredan los dos prompts que derivan de él: `NewObjectNameInputPrompt`
(nombrar) y `ObjectNameInputPrompt` (buscar). Verificado que el mapeo del
vocabulario de §15 sigue funcionando encima de la acumulación.

Casos verificados: nombre+confirmación separados · en la misma frase · nombre de
dos palabras en tres frases · cancelar a mitad · confirmar sin haber dicho nada.

### 17.c Nota sobre los acentos

En la prueba el reconocedor devolvió **"rectángulo" con tilde** y el vocabulario
escribe `Rectangulo` sin tilde. No es un problema: `ObjectNames/TraduceToEs.py`
mapea ambas grafías a la misma etiqueta, y `SelectByLabel` compara sin acentos
(§13.c). Conviene mantener esa doble entrada al agregar nombres nuevos con
tilde.

> **Sin verificar dentro de FreeCAD:** el arreglo se probó con un doble del
> prompt (sin Qt). Falta confirmar en vivo que se pueda decir el nombre, esperar,
> y confirmar después.
