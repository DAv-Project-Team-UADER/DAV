# Guía de prueba — nombrar por voz y seleccionar por nombre

Prueba de punta a punta: crear un cuadrado, nombrarlo, extruirlo a un cubo y
volver a seleccionarlo diciendo su nombre.

Todas las frases de acá están verificadas contra los `TraduceTo*.py` reales.
Lo implementado se documenta en [`pendientes-dav.md`](../estado/pendientes-dav.md) §13.

---

## Antes de empezar

- Abrir FreeCAD con el arranque de DAV (el panel DAV tiene que estar visible).
- **Crear un documento nuevo, común y corriente** — ver abajo.
- Tener el micrófono andando (el panel muestra lo que va reconociendo).

### Qué documento crear

**Uno común** (`Archivo → Nuevo`, o por voz **"explorador"** → **"archivo"** →
**"nuevo"**). En FreeCAD hay **un solo tipo de documento**: no existe un
"documento 2D" aparte.

Lo que puede confundir es que el diálogo de arranque de FreeCAD ofrece
plantillas o que ciertos workbenches (Sketcher, Draft) trabajen en 2D. Eso es
el **banco de trabajo**, no el documento: el mismo archivo `.FCStd` guarda
geometría 2D y 3D mezclada. De hecho esta prueba hace exactamente eso —
empieza con un rectángulo plano y termina con un sólido.

Así que: documento nuevo normal, y el 2D/3D lo decide el comando que uses.

> Si te perdés en cualquier punto, decí **"contexto"** y el panel lista lo que
> se puede decir ahí. Para volver un nivel, **"subir"**.

---

## Parte 1 — Crear el cuadrado y ponerle nombre

| Paso | Decir | Qué pasa |
|---|---|---|
| 1 | **"banco de trabajo"** | entra a `workbench` |
| 2 | **"borrador"** | entra a Draft |
| 3 | **"creacion"** | entra a las primitivas |
| 4 | **"rectangulo"** | FreeCAD pide los puntos del rectángulo |

Dibujá el rectángulo (por ahora los puntos se marcan con el mouse).

**Al terminar aparece el pop-up "DAV — Nombre del objeto".**

| Paso | Decir | Qué pasa |
|---|---|---|
| 5 | **"mesa"** | se ve en el recuadro del pop-up |
| 6 | **"aceptar"** | confirma y cierra |

En el árbol de FreeCAD el objeto queda con el label **`mesa`**.

> **Importante:** el nombre tiene que salir del **vocabulario de nombres**
> (`Dav/dic/ObjectNames/`). Vosk no transcribe texto libre: sólo reconoce
> palabras de su gramática activa. Ver la lista abajo.

### Nombres que se pueden dictar

Están en [`Dav/dic/ObjectNames/TraduceToEs.py`](../../dic/ObjectNames/TraduceToEs.py)
— 56 en español:

| Grupo | Palabras |
|---|---|
| Formas | cubo · cuadrado · rectangulo · circulo · triangulo · cilindro · esfera · cono · prisma · anillo · aro |
| Piezas | base · tapa · placa · chapa · columna · viga · eje · tubo · caño · barra · perno · tornillo · tuerca · arandela · brida · soporte · brazo · engranaje · rueda · resorte |
| Muebles | mesa · silla · pata · patas · estante · puerta · cajon · marco · pared · techo · piso |
| Genéricos | pieza · cuerpo · bloque · objeto · figura · molde · tapa superior · tapa inferior · parte alta · parte baja |

**¿Falta uno?** Agregá una línea a ese archivo — no hace falta tocar código:

```python
"pilar": "Pilar",
```

Que sea una palabra corriente del español: Vosk no reconoce inventos ni siglas.

> Si cancelás o no se entiende, el objeto queda como **`Objeto 1`** y la
> creación **no se bloquea**. Eso es lo esperado, no un error.

### Qué más vas a ver

El rectángulo se descompone en sus partes: aparecen también `Linea 1`…`Linea 4`
y `Punto 1`…`Punto 4`. Es lo que hace `CreateObjects` (descompone, no crea).
El pop-up de nombre sale **una sola vez**, para el objeto padre — las líneas y
puntos los nombra el `Tagger` solo.

---

## Parte 1-bis — Variante sin mouse: dictar las medidas

El camino de arriba usa el mouse para marcar las esquinas. Si querés dictar
**todo**, incluidas las coordenadas, existe otra ruta:

| Paso | Decir | Qué pasa |
|---|---|---|
| 1 | **"banco de trabajo"** | entra a `workbench` |
| 2 | **"croquis"** | entra a Sketcher |
| 3 | **"geometria"** | entra a la geometría |
| 4 | **"rectangulo"** | entra al submenú del rectángulo |
| 5 | **"rectangulo por esquinas"** | arranca el dictado de coordenadas |

Ahí se abren **cuatro pop-ups seguidos**, uno por coordenada, en este orden:

| Pop-up | Pide | Para un cuadrado de 40×40 decir |
|---|---|---|
| 1 | `x1` | **"cero"** → "aceptar" |
| 2 | `y1` | **"cero"** → "aceptar" |
| 3 | `x2` | **"cuarenta"** → "aceptar" |
| 4 | `y2` | **"cuarenta"** → "aceptar" |

Y **recién ahí** aparece el pop-up del nombre: **"mesa"** → **"aceptar"**.

> **El nombre va al final, no al principio.** Primero las medidas, después se
> crea el objeto, y último el nombre — no se puede etiquetar algo que todavía
> no existe.

### Dos cosas que conviene saber de esta ruta

**No crea un croquis.** Pese a estar en la carpeta Sketcher, `create_by_corners`
crea un `Part::Feature` suelto (usa `Part.makePolygon`, no
`Sketcher::SketchObject`). Para esta prueba es **mejor así**: un croquis hay que
apoyarlo en un plano y abrirlo en edición, y `extruir` lo toma sin vueltas
justamente por ser un objeto suelto.

**Los números de 100 en adelante hay que deletrearlos.** Hasta 99 se dicen
normal ("cuarenta", "treinta y cinco"); de ahí en más va dígito por dígito
("uno cero cero" = 100). Detalle en
[`numeros-por-voz-limites-y-propuesta.md`](../referencia/numeros-por-voz-limites-y-propuesta.md).

### ¿Cuál de las dos usar?

| | Draft (Parte 1) | Sketcher por esquinas (1-bis) |
|---|---|---|
| Esquinas | con el mouse | dictadas |
| Pop-ups | 1 (el nombre) | 5 (4 medidas + nombre) |
| Medidas exactas | no | sí |

Para **probar el nombre y la selección**, que es lo nuevo, conviene Draft: menos
pasos y menos chances de que falle el reconocimiento numérico. Para probar el
**dictado completo sin tocar el mouse**, esta variante.

---

## Parte 2 — Extruir el cuadrado a un cubo

La extrusión **actúa sobre lo que esté seleccionado**, así que primero hay que
seleccionar, y de paso probamos la búsqueda por nombre.

| Paso | Decir | Qué pasa |
|---|---|---|
| 1 | **"subir"** (3 veces) | vuelve a la raíz |
| 2 | **"seleccion"** | entra al módulo Selection |
| 3 | **"buscar"** | abre "DAV — Buscar objeto" |
| 4 | **"mesa"** | dictás el nombre buscado |
| 5 | **"aceptar"** | confirma |

El objeto `mesa` queda resaltado en la vista 3D y en el árbol.

Ahora sí, la extrusión:

| Paso | Decir | Qué pasa |
|---|---|---|
| 6 | **"subir"** | vuelve a la raíz |
| 7 | **"banco de trabajo"** → **"pieza"** | entra a Part |
| 8 | **"extruir"** | extruye 10 mm en Z → **queda un cubo** |

Al terminar, **el pop-up de nombre aparece otra vez** (la extrusión crea un
objeto nuevo). Decí **"cubo"** y **"aceptar"**.

> El cuadrado original se oculta (`Visibility = False`), no se borra: sigue en
> el árbol como `mesa`.

---

## Parte 3 — Probar la selección por nombre

Ahora hay dos objetos con nombre dictado: `mesa` y `cubo`.

| Decir | Resultado esperado |
|---|---|
| **"seleccion"** → **"buscar"** → **"cubo"** → **"aceptar"** | resalta el cubo |
| **"seleccion"** → **"buscar"** → **"mesa"** → **"aceptar"** | resalta el cuadrado |

Otras frases que también entran a la búsqueda: *por nombre* · *buscar objeto* ·
*buscar por nombre* · *seleccionar por nombre* · *nombre* · *llamar*.

### El resto del módulo Selection

Dentro de `seleccion`, sin pop-up:

| Decir | Hace |
|---|---|
| **"siguiente"** | pasa al objeto siguiente |
| **"anterior"** | vuelve al anterior |
| **"todos"** | selecciona todo |
| **"nada"** | deselecciona |
| **"cual"** | dice cuál está seleccionado |
| **"cuantos"** | cuántos hay |

---

## Atajo: probarlo sin voz, desde la consola Python

Para aislar si un problema es del motor de voz o de la lógica. Consola Python
de FreeCAD (`Vista → Paneles → Consola de Python`):

```python
import sys
sys.path.insert(0, r"C:\Users\Jose\Desktop\j\DAV\Dav\scr\selection")

import FreeCAD as App
from tagger import Tagger
from object_selection import ObjectSelection

doc = App.activeDocument()

# Nombrar a mano el ultimo objeto creado, sin pop-up
t = Tagger("es", doc)
print(t.ApplyCustomName(doc.ActiveObject, "mesa"))

# Buscarlo por nombre
sel = ObjectSelection()
print(sel.SelectByLabel("mesa"))      # -> Name interno del objeto
print(sel.SelectByLabel("MESA"))      # -> igual: ignora mayusculas
print(sel.SelectByLabel("inexistente"))  # -> None + aviso
```

Crear y descomponer sin que pregunte el nombre:

```python
from createobjects import CreateObjects
CreateObjects(ObjectName=doc.ActiveObject.Name, Is3D=True, AskName=False).Execute()
```

---

## Qué mirar si algo falla

| Síntoma | Dónde mirar |
|---|---|
| No aparece el pop-up | ¿Hay documento activo? ¿El panel DAV está cargado? |
| El pop-up sale pero no entiende el nombre | Probá una palabra más común: Vosk no inventa vocabulario (§13.e) |
| "buscar" no encuentra un objeto que existe | El label tiene que estar en la gramática; probá primero con **"siguiente"** para confirmar que Selection responde |
| FreeCAD se cierra de golpe | Mirá `config/dav.log`: si corta en «aplicando gramatica» sin el «gramatica aplicada» que sigue, es el crash de `SetGrammar` (§10) |

El log vive en `config/dav.log` y registra cada frase reconocida y cada cambio
de gramática.

---

## Lo que todavía no se probó

Esta guía describe el camino previsto; **el circuito no se ejerció dentro de
FreeCAD con micrófono**. Lo verificado hasta ahora fue fuera de FreeCAD con
dobles: nombrado, desambiguación de duplicados, búsqueda laxa, y que sin GUI
degrade al nombre automático en vez de romper.

Lo de mayor riesgo, y lo primero que conviene mirar al probar: que el cambio de
gramática del pop-up de búsqueda **no tumbe el proceso** (§13.g).
