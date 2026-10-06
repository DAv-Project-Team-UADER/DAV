# Rutas de voz — Selection y creación de objetos

Guía para probar por voz el módulo `Selection` y el circuito de
`CreateObjects`. Frases verificadas contra los diccionarios de `Dav/dic/`.

---

## Ruta A — Crear objetos (dispara CreateObjects)

Ejercita el `CreateObjects` de `Dav/scr/selection/`, porque cada primitiva de
`creation.py` lo invoca al terminar.

| Paso | Decir | Contexto |
|---|---|---|
| 1 | **"banco de trabajo"** | `workbench` |
| 2 | **"borrador"** | `workbench > draft` |
| 3 | **"creacion"** | `draft > creation` |
| 4 | **"rectangulo"** | ejecuta → `CreateObjects(...).Execute()` |

Otras primitivas del paso 4: **"punto"**, **"poligono"**, **"cuadrilatero"**,
**"dibujar rectangulo"**, **"marcar punto"**, **"dibujar poligono"**.

Cada una llama `CreateObjects(ObjectName=..., Is3D=False).Execute()`
(`creation.py:31,38,45`), que es el camino que pasa por el `Tagger`.

Sinónimos del paso 3: creacion · creación · crear · crear objeto · primitivas.

---

## Ruta B — Navegar la selección

| Paso | Decir | Ejecuta |
|---|---|---|
| 1 | **"seleccion"** | entra a `selection` |
| 2 | **"siguiente"** | `SelectNext()` |
| 3 | **"anterior"** | `SelectPrevious()` |
| 4 | **"todos"** | `SelectAll()` |
| 5 | **"nada"** | `DeselectAll()` |

Sinónimos del paso 1: seleccion · selección · seleccionar ·
seleccion de objetos · objetos.

Dentro de `selection` (ya existían en `Selection/TraduceToEs.py`):

- **next** — avanzar · otro · otra · pasar · siguiente · siguiente objeto ·
  objeto siguiente · siguiente elemento · seleccionar siguiente
- **previous** — retroceder · volver · anterior · anterior objeto ·
  objeto anterior · seleccionar anterior
- **selectall** — todos · todo · seleccionar todos · seleccionar todo ·
  seleccionar todos los objetos
- **deselectall** — nada · ninguno · ninguna · quitar · quitar todos ·
  desmarcar · desmarcar todo

Otras hojas del módulo: `current` (objeto actual) y `count` (cuántos hay).

---

## Ruta C — Borrar, buscar, pintar y dar material

Además de recorrer la selección, el módulo borra, busca por nombre y cambia el
aspecto de lo seleccionado, sin diálogos nativos (todo se elige por voz):

| Para | Decir | Qué hace |
|---|---|---|
| Borrar el objeto elegido | **"borrar"** · "borrar objeto" · "eliminar" · "suprimir" | Primero **"siguiente"/"anterior"** hasta el objeto y luego **"borrar"** |
| Buscar un objeto por su nombre | **"buscar por deletreo"** · "deletrear" · "buscar objeto" | Se deletrea el nombre y se selecciona el más parecido |
| Pintar | **"pintar objeto"** · "colorear objeto" · "cambiar color" · "poner color" | Lista corta de colores (rojo, naranja, amarillo, verde, celeste, azul, violeta, rosa, marrón, negro, blanco, gris) |
| Dar material | **"material de objeto"** · "poner material" · "elegir material" | Materiales de la biblioteca de FreeCAD (aluminio, acero, inoxidable, hierro, cobre, latón, bronce, titanio, oro, plata, PLA, ABS, plástico, acrílico, vidrio, madera); solo se ofrecen los que la instalación tenga |

- El color y el material se aplican a lo que esté **seleccionado**; si no hay nada,
  se elige antes con **"siguiente"** o **"buscar por deletreo"**.
- En el cuadro de colores y de materiales, **"arriba"** y **"abajo"** mueven la
  selección, **"okey"** la confirma y **"cancelar"** sale sin cambiar nada.
- **"borrar"** quita el objeto sin pedir confirmación aparte; para borrar con
  confirmación por voz usar los comandos globales de corrección
  ("borrar objeto", "borrar último", "borrar rotos"; ver el manual PDF).

Código: `Dav/dic/Selection/selection.py` y `_aspecto.py`.

---

## Navegación general

Definidos en `Dav/dic/NavCommands/TraduceToEs.py`, sirven en cualquier nivel:

| Para | Decir |
|---|---|
| Subir un nivel | **"subir"** · "atrás" · "salir" · "regresar" |
| Ver dónde estás | **"contexto"** · "dónde estoy" · "qué puedo decir" |
| Confirmar | **"aceptar"** · "ok" · "confirmar" · "enviar" |
| Cancelar | **"cancelar"** |

Si te perdés, **"contexto"** lista lo que se puede decir en ese punto.

---

## Prueba directa desde la consola Python

Sin pasar por voz, para aislar si un problema es del motor o del diccionario:

```python
import sys
sys.path.insert(0, r"C:\Users\Jose\Desktop\j\DAV\Dav\scr\selection")

from object_selection import ObjectSelection
sel = ObjectSelection()
sel.SelectAll()
sel.SelectNext()
print(sel.GetCurrentObject())
```

Circuito de creación + etiquetado:

```python
import FreeCAD as App
from createobjects import CreateObjects

doc = App.ActiveDocument
CreateObjects(ObjectName=doc.ActiveObject.Name, Is3D=False).Execute()
```

---

## Traducciones que se agregaron para esto

Las funciones ya existían; faltaban las frases de entrada, sin las cuales el
submenú es inalcanzable por voz aunque el diccionario funcione.

**`Dav/dic/TraduceToEs.py`** — `base.py` registraba `"selection": selection`
pero la traducción raíz no lo mencionaba: el módulo entero no tenía puerta de
entrada. Se agregó el import y seis frases.

**`Dav/dic/Workbench/DraftWork/TraduceToEs.py`** — de los 14 submenús de
`DraftWork.py` solo 11 estaban traducidos. Faltaban `creation`, `drafting` y
`modification`.

> Al agregarlas, ojo con pisar claves existentes: `'modificar'` ya apuntaba a
> `draft['modify']`, así que `modification` quedó como `'modificaciones'`.
> Una clave repetida no da error — la última gana, en silencio.

Ambos arreglos ya están replicados en `TraduceToEn.py` y `TraduceToPT.py` (raíz y
`Workbench/DraftWork/`).
