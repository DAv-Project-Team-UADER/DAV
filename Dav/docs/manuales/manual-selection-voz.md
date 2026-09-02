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
submenú es inalcanzable por voz aunque el diccionario funcione (el caso que
describe `pendientes-dav.md` §4).

**`Dav/dic/TraduceToEs.py`** — `base.py` registraba `"selection": selection`
pero la traducción raíz no lo mencionaba: el módulo entero no tenía puerta de
entrada. Se agregó el import y seis frases.

**`Dav/dic/Workbench/DraftWork/TraduceToEs.py`** — de los 14 submenús de
`DraftWork.py` solo 11 estaban traducidos. Faltaban `creation`, `drafting` y
`modification`.

> Al agregarlas, ojo con pisar claves existentes: `'modificar'` ya apuntaba a
> `draft['modify']`, así que `modification` quedó como `'modificaciones'`.
> Una clave repetida no da error — la última gana, en silencio.

Falta replicar ambos arreglos en `TraduceToEn.py` y `TraduceToPT.py`.
