# Agregar un submenú (una carpeta nueva) al árbol de comandos

[Agregar un comando](agregar-comando.md) explica cómo sumar **una frase** a un
contexto que ya existe. Esta página cubre el caso siguiente: crear **un contexto
nuevo**, es decir, una carpeta con sus propios comandos que se entra diciendo una
palabra («archivo», «ejemplos»…).

El ejemplo real es `Dav/dic/Explorer/Examples/` (ver [`Examples`](../diagramas/Examples.md)).

---

## Qué tiene que tener la carpeta

```
Explorer/Examples/
├── __init__.py          # vacío, pero obligatorio
├── Examples.py          # diccionario maestro: claves internas → callables
├── ayuda.py             # explica los comandos del nivel
├── TraduceToEs.py       # frases habladas en español → los mismos callables
├── TraduceToEn.py       # ... en inglés
├── TraduceToPt.py       # ... en portugués
├── manual.svg           # ícono de la clave 'manual'
├── demos.svg            # ícono de la clave 'demos'
└── _manual.py, _demos.py  # código de los comandos (opcional, el guion bajo = uso interno)
```

| Regla | Detalle |
| --- | --- |
| **Carpeta, módulo y variable se llaman igual** | `Examples/Examples.py` define `examples` (la variable va en minúscula, como `explorer` en `Explorer/Explorer.py`) |
| **Una carpeta = un nivel** | Si un comando tiene variantes, esas variantes van en una carpeta hija |
| **`ayuda.py` en cada carpeta** | Su función `ayuda` va como clave `'help'` del diccionario maestro |
| **Cabezal obligatorio** | Todos los archivos nuevos, ver [convenciones](convenciones.md) |

---

## Paso a paso

### 1. Creá el diccionario maestro

Las claves internas son **una palabra en inglés**, sin repetir el contexto del padre.

```python
# Examples/Examples.py
from .ayuda import ayuda
from ._demos import startExample
from ._manual import openManual

examples = {
    'manual': openManual,
    'demos':  startExample,
    'help':   ayuda,
}
```

### 2. Enlazalo en el padre — **anidado, nunca aplanado**

```python
# Explorer/Explorer.py
from .Examples.Examples import examples

explorer.update({'examples': examples})   # CORRECTO: 'examples' queda navegable
explorer.update(examples)                 # INCORRECTO: aplana las hojas en el padre
```

Aplanar rompe dos cosas **sin avisar**: las claves repetidas entre hojas (`help`,
`create`…) se pisan y solo sobrevive la última, y la carpeta deja de ser un nodo
navegable, con lo que su `TraduceTo*.py` no se carga nunca. Hay una prueba que lo
controla (`test_no_flattened_updates_in_dic`); detalle en `pendientes-dav.md` §4.

### 3. Escribí los tres `TraduceTo*`

Cada uno mapea las **frases habladas de ese idioma** a los callables del diccionario
maestro, por objeto (`examples['manual']`), sin duplicar funciones.

```python
# Examples/TraduceToEs.py
from .Examples import examples

TraduceToEs = {
    'manual':      examples['manual'],
    'referencia':  examples['manual'],
    'ejemplos':    examples['demos'],
    'ayuda':       examples['help'],
}
```

Notas:

- **El nombre del archivo y de la variable coinciden** (`TraduceToEs.py` define `TraduceToEs`).
- En la raíz de `dic/` el portugués se llama `TraduceToPT.py`; en las subcarpetas,
  `TraduceToPt.py`. El `DictionaryLoader` acepta las dos grafías.
- Las tildes son opcionales: el motor compara sin acentos. La gramática de Vosk sí
  necesita la forma del vocabulario del modelo.
- «subir», «enviar», «cancelar» y «dónde estoy» **no** se definen acá: viven en
  `Dav/dic/NavCommands/` y valen en cualquier contexto.
- Las vistas estándar (`StdView.StandardViews`) se anexan al final de varios
  `TraduceTo*` para poder cambiar la vista desde cualquier contexto; copiá ese bloque
  de una carpeta hermana si querés lo mismo.

### 4. Agregá las frases para **entrar** en el `TraduceTo*` del padre

Sin esto la carpeta existe pero nadie puede llegar a ella.

```python
# Explorer/TraduceToEs.py
'ejemplos':        explorer['examples'],
'quiero aprender': explorer['examples'],
'aprender':        explorer['examples'],
```

Repetilo en `TraduceToEn.py` y `TraduceToPt.py`, y revisá que la frase no choque con
otra ya usada en ese contexto (una frase repetida en un mismo diccionario se pisa).

### 5. Poné los íconos — **se buscan por el nombre de la clave**

El panel pide el SVG con la clave del botón: la clave `manual` busca `manual.svg`.
[`IconLocator`](../diagramas/IconLocator.md) indexa todos los SVG de `Dav/dic/` y
`InterfazDAV/Icons/` y compara sin mayúsculas ni `_` `-`.

| Situación | Resultado |
| --- | --- |
| Hoja con `<clave>.svg` en cualquier carpeta de `dic/` | Muestra ese ícono |
| Hoja sin SVG | Botón con el respaldo de dos letras (no es un error) |
| **Dos SVG con el mismo nombre en carpetas distintas** | **Comparten ícono**: gana el primero que se encuentra |
| Carpeta cuya clave coincide con el nombre de un SVG existente | La carpeta **hereda** ese ícono |

Por eso importa cómo se nombran las claves. En `Examples` la hoja se llama `demos` y no
`examples`: como la carpeta se llama `examples`, una hoja con el mismo nombre le habría
puesto ícono a la carpeta, y se pedía que no tuviera. Antes de fijar una clave, buscá si
ya hay un SVG con ese nombre:

```powershell
Get-ChildItem Dav\dic -Recurse -Filter "<clave>.svg"
```

Si el ícono existe con otro nombre, copiá el SVG con el nombre de la clave (como
`manual.svg`, copia de `File/open.svg`) o sumá un alias en `IconLocator._ALIASES`.

### 6. Actualizá la ayuda

Sumá el submenú a la ayuda del padre (`Explorer/ayuda.py`) y describí las hojas en
`ayuda.py` de la carpeta nueva.

### 7. Verificá

```powershell
cd Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad
$env:PYTHONPATH = "<ruta>\Dav"
python -m unittest tests.test_real_dictionaries
```

Comprueba que `base.py` importa limpio, que ningún submenú está aplanado y que las
carpetas siguen siendo navegables. **Un solo import roto en una hoja profunda puede
dejar al `Browser` sin ningún comando**, y el `DictionaryLoader` lo captura y sigue,
así que sin esta prueba no te enterás. Para probar tus funciones sin abrir la interfaz,
ver [probando.md](probando.md).

---

## Checklist

- [ ] Carpeta con `__init__.py`, diccionario maestro, `ayuda.py` y los tres `TraduceTo*`.
- [ ] Enlazada **anidada** en el diccionario del padre.
- [ ] Frases de entrada agregadas en los tres `TraduceTo*` del padre.
- [ ] Cada hoja tiene su SVG con el nombre de la clave (o se aceptó el ícono de respaldo).
- [ ] La clave de la carpeta **no** coincide con el nombre de ningún SVG de sus hojas.
- [ ] `test_real_dictionaries` pasa.
- [ ] Cabezal en los archivos nuevos y docstrings en inglés.
- [ ] Diagrama en [`diagramas/`](../diagramas/README.md) si la carpeta trae clases o flujos nuevos.

---

Anterior: [Agregar un comando](agregar-comando.md) · Siguiente: [Agregar un diálogo de voz](agregar-prompt.md)
