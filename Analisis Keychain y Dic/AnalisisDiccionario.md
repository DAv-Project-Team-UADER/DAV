# Analisis de `ejemplo de diccionario terminado`

La carpeta `ejemplo de diccionario terminado` contiene un ejemplo de diccionario de comandos para FreeCAD. La idea principal es organizar acciones de FreeCAD en una estructura navegable, donde cada palabra clave apunta a otra categoria, a una funcion ejecutable o a una ayuda.

En terminos simples, funciona como un mapa de comandos:

```python
palabra -> accion
palabra -> subdiccionario
palabra -> ayuda
```

Por ejemplo, en el nivel principal existe la clave `file`, que no ejecuta un comando directamente, sino que lleva a otro diccionario con comandos de archivo como `new`, `open`, `save` y `saveas`.

## Para Que Sirve

Este directorio sirve para demostrar como se puede construir un sistema de comandos por voz o por texto usando diccionarios Python.

Cada diccionario relaciona una palabra con una accion. Esa accion puede ser:

1. Un comando de FreeCAD ejecutado con `Gui.runCommand`.
2. Una funcion propia, como `_undo()` o `_redo()`.
3. Otro diccionario de comandos.
4. Una funcion de ayuda.

La estructura permite que un programa externo pueda recibir una palabra, buscarla en el diccionario y ejecutar lo que corresponda.

Un flujo posible seria:

```text
usuario dice "file"
el sistema entra al diccionario file
usuario dice "save"
el sistema ejecuta Std_Save en FreeCAD
```

Tambien podria funcionar con traducciones:

```text
usuario dice "archivo"
el sistema lo traduce o lo asocia con file
usuario dice "guardar"
el sistema ejecuta Std_Save
```

## Estructura General

La carpeta tiene esta forma:

```text
ejemplo de diccionario terminado/
|-- explorer.py
|-- ayuda.py
|-- TraduceToEs.py
|-- TraduceToEn.py
|-- TraduceToPT.py
|-- file.svg
|-- edit.svg
|-- print.svg
|-- screenshot.svg
|-- file/
|   |-- file.py
|   |-- ayuda.py
|   |-- TraduceToEs.py
|   |-- TraduceToEn.py
|   |-- TraduceToPT.py
|-- edit/
|   |-- edit.py
|   |-- ayuda.py
|   |-- TraduceToEs.py
|   |-- TraduceToEn.py
|   |-- TraduceToPT.py
|-- print/
|   |-- print_cmds.py
|   |-- ayuda.py
|   |-- TraduceToEs.py
|   |-- TraduceToEn.py
|   |-- TraduceToPT.py
|-- doc/
|   |-- doc.py
|   |-- ayuda.py
|   |-- TraduceToEs.py
|   |-- TraduceToEn.py
|   |-- TraduceToPT.py
```

## Nivel Principal: `explorer.py`

El archivo `explorer.py` es el punto de entrada del diccionario.

Importa los subdiccionarios:

```python
from .file.file import file
from .edit.edit import edit
from .print.print_cmds import print_cmds
from .doc.doc import doc
from .ayuda import ayuda
```

Luego define el diccionario principal:

```python
explorer = {
    'file':       file,
    'edit':       edit,
    'print':      print_cmds,
    'doc':        doc,
    'refresh':    lambda: Gui.runCommand('Std_Refresh', 0),
    'screenshot': lambda: Gui.runCommand('Std_ViewScreenShot', 0),
    'textdoc':    lambda: Gui.runCommand('Std_TextDocument', 0),
    'help':       ayuda,
}
```

Este diccionario mezcla dos tipos de entradas.

Las primeras entradas son categorias:

```python
'file': file
'edit': edit
'print': print_cmds
'doc': doc
```

Estas no ejecutan necesariamente una accion final. En cambio, llevan hacia otro diccionario mas especifico.

Las otras entradas son comandos directos:

```python
'refresh': lambda: Gui.runCommand('Std_Refresh', 0)
'screenshot': lambda: Gui.runCommand('Std_ViewScreenShot', 0)
'textdoc': lambda: Gui.runCommand('Std_TextDocument', 0)
```

Estas si ejecutan comandos de FreeCAD directamente.

Finalmente:

```python
'help': ayuda
```

apunta a una funcion que imprime los comandos disponibles.

## Subdiccionario `file`

La carpeta `file` contiene comandos relacionados con operaciones de archivo.

El archivo principal es `file/file.py`:

```python
file = {
    'new':    lambda: Gui.runCommand('Std_New', 0),
    'open':   lambda: Gui.runCommand('Std_Open', 0),
    'close':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
    'save':   lambda: Gui.runCommand('Std_Save', 0),
    'saveas': lambda: Gui.runCommand('Std_SaveAs', 0),
    'help':   ayuda,
}
```

Cada clave representa una accion de archivo:

| Clave | Accion |
| --- | --- |
| `new` | Crea un documento nuevo |
| `open` | Abre un documento existente |
| `close` | Cierra la ventana activa |
| `save` | Guarda el documento activo |
| `saveas` | Guarda el documento con otro nombre |
| `help` | Muestra ayuda del grupo `file` |

Todas las acciones principales usan:

```python
Gui.runCommand(...)
```

Eso significa que le piden a FreeCAD que ejecute un comando interno de la interfaz grafica.

## Subdiccionario `edit`

La carpeta `edit` contiene comandos de edicion.

El archivo principal es `edit/edit.py`:

```python
edit = {
    'undo':      lambda: Gui.runCommand('Std_Undo', 0),
    'redo':      lambda: Gui.runCommand('Std_Redo', 0),
    'copy':      lambda: Gui.runCommand('Std_Copy', 0),
    'cut':       lambda: Gui.runCommand('Std_Cut', 0),
    'paste':     lambda: Gui.runCommand('Std_Paste', 0),
    'delete':    lambda: Gui.runCommand('Std_Delete', 0),
    'selectall': lambda: Gui.runCommand('Std_SelectAll', 0),
    'help':      ayuda,
}
```

Sus comandos cubren acciones clasicas de edicion:

| Clave | Accion |
| --- | --- |
| `undo` | Deshace |
| `redo` | Rehace |
| `copy` | Copia |
| `cut` | Corta |
| `paste` | Pega |
| `delete` | Borra |
| `selectall` | Selecciona todo |
| `help` | Muestra ayuda del grupo `edit` |

## Subdiccionario `print`

La carpeta `print` contiene comandos de impresion.

El archivo principal es `print/print_cmds.py`:

```python
print_cmds = {
    'print': lambda: Gui.runCommand('Std_Print', 0),
    'pdf':   lambda: Gui.runCommand('Std_PrintPdf', 0),
    'help':  ayuda,
}
```

Este grupo es mas chico y contiene:

| Clave | Accion |
| --- | --- |
| `print` | Imprime usando el comando estandar de FreeCAD |
| `pdf` | Exporta o imprime a PDF |
| `help` | Muestra ayuda del grupo `print` |

## Subdiccionario `doc`

La carpeta `doc` contiene comandos asociados al documento activo de FreeCAD, pero usando la API core en lugar de comandos de GUI.

El archivo principal es `doc/doc.py`:

```python
import FreeCAD as App

def _undo():
    App.ActiveDocument.undo()

def _redo():
    App.ActiveDocument.redo()

doc = {
    'undo': _undo,
    'redo': _redo,
    'help': ayuda,
}
```

A diferencia de `edit`, este modulo no usa `FreeCADGui`. Usa:

```python
import FreeCAD as App
```

Eso significa que trabaja directamente con el documento activo:

```python
App.ActiveDocument.undo()
App.ActiveDocument.redo()
```

La diferencia conceptual es:

| Grupo | Forma de ejecucion |
| --- | --- |
| `edit` | Usa comandos de interfaz grafica con `Gui.runCommand` |
| `doc` | Usa la API interna de FreeCAD con `App.ActiveDocument` |

## Archivos `ayuda.py`

Cada nivel tiene un archivo `ayuda.py`.

En el nivel principal, `ayuda.py` imprime los comandos disponibles en `explorer`:

```python
def ayuda():
    print('Comandos disponibles en explorer:')
    print('  file       - Subconjunto: operaciones de archivo (new, open, close, save, saveas)')
    print('  edit       - Subconjunto: edicion (undo, redo, copy, cut, paste, delete, selectall)')
    print('  print      - Subconjunto: impresion (print, pdf)')
    print('  doc        - Subconjunto: API core sin GUI (undo, redo)')
    print('  refresh    - Refresca la vista del documento')
    print('  screenshot - Captura de pantalla de la vista 3D')
    print('  textdoc    - Crea un documento de texto')
```

Las subcarpetas tambien tienen su propia ayuda. Por ejemplo, `file/ayuda.py` explica los comandos de archivo.

Esto permite que el usuario pida ayuda dentro de un contexto especifico:

```text
explorer -> help
file -> help
edit -> help
print -> help
doc -> help
```

## Archivos de Traduccion

La carpeta incluye archivos como:

```text
TraduceToEs.py
TraduceToEn.py
TraduceToPT.py
```

Tambien existen archivos de traduccion dentro de cada subcarpeta:

```text
file/TraduceToEs.py
edit/TraduceToEs.py
print/TraduceToEs.py
doc/TraduceToEs.py
```

Su funcion es permitir que el sistema acepte palabras en distintos idiomas o sinonimos.

Por ejemplo, en el nivel principal, `TraduceToEs.py` contiene entradas como:

```python
'Carpeta': file
'Archivo': file
'editar': edit
'imprimir': print_cmds
'refrescar': lambda: Gui.runCommand('Std_Refresh', 0)
'foto': lambda: Gui.runCommand('Std_ViewScreenShot', 0)
'documento de texto': lambda: Gui.runCommand('Std_TextDocument', 0)
'ayuda': ayuda
```

Esto permite que varias palabras apunten al mismo comando o categoria.

Ejemplo:

```python
'refrescar': lambda: Gui.runCommand('Std_Refresh', 0)
'recargar': lambda: Gui.runCommand('Std_Refresh', 0)
'actualizar': lambda: Gui.runCommand('Std_Refresh', 0)
```

Las tres palabras ejecutan el mismo comando.

## Funcionamiento Por Capas

El ejemplo se puede entender como una estructura por capas.

Primera capa:

```text
explorer
```

Segunda capa:

```text
file
edit
print
doc
```

Tercera capa:

```text
new, open, save, undo, redo, pdf, etc.
```

Visualmente:

```text
explorer
|-- file
|   |-- new
|   |-- open
|   |-- close
|   |-- save
|   |-- saveas
|   |-- help
|-- edit
|   |-- undo
|   |-- redo
|   |-- copy
|   |-- cut
|   |-- paste
|   |-- delete
|   |-- selectall
|   |-- help
|-- print
|   |-- print
|   |-- pdf
|   |-- help
|-- doc
|   |-- undo
|   |-- redo
|   |-- help
|-- refresh
|-- screenshot
|-- textdoc
|-- help
```

## Relacion Con Los Iconos

En la raiz aparecen archivos SVG:

```text
file.svg
edit.svg
print.svg
screenshot.svg
```

Estos nombres coinciden con algunas claves del diccionario principal:

```python
'file'
'edit'
'print'
'screenshot'
```

Esto encaja con la logica de `Keychain.py`, que puede tomar las claves de un diccionario y generar nombres de iconos agregando `.svg`.

Por ejemplo:

```python
file -> file.svg
edit -> edit.svg
print -> print.svg
screenshot -> screenshot.svg
```

Asi, el diccionario no solo sirve para ejecutar comandos, sino tambien para asociar comandos o categorias con iconos visuales.

## Como Se Ejecuta Un Comando

La mayoria de los comandos usan funciones lambda:

```python
'save': lambda: Gui.runCommand('Std_Save', 0)
```

Esto significa que la accion no se ejecuta cuando se crea el diccionario. Se ejecuta despues, cuando alguien llama a esa funcion.

Por ejemplo:

```python
accion = file['save']
accion()
```

En ese momento se ejecuta:

```python
Gui.runCommand('Std_Save', 0)
```

Ese patron es importante porque permite guardar acciones dentro del diccionario sin dispararlas inmediatamente.

## Observaciones Importantes

Hay algunos detalles a tener en cuenta:

1. El ejemplo depende de FreeCAD. Para ejecutarlo correctamente debe existir el modulo `FreeCADGui` o `FreeCAD`.
2. Los diccionarios principales estan pensados para usarse dentro de un paquete, porque varios imports usan rutas relativas como `from .ayuda import ayuda`.
3. Algunas traducciones usan imports no relativos, como `import ayuda` o `from file import file`. Dependiendo de como se ejecute el codigo, eso puede requerir ajustar el `PYTHONPATH` o convertir esos imports a relativos.
4. En algunos archivos de traduccion hay diferencias de nombres. Por ejemplo, puede aparecer `TraduceToEnUs`, `TraduceToPtBr` o `TraduceToEs` segun el archivo.
5. Algunas traducciones devuelven directamente diccionarios o funciones, mientras que otras devuelven strings como `'file'` o `'edit'`. Para usarlo de forma uniforme, el cargador del sistema deberia contemplar ambos casos.

## Resumen

`ejemplo de diccionario terminado` es una maqueta funcional de un sistema de comandos jerarquico para FreeCAD.

Su proposito es:

1. Agrupar comandos por categoria.
2. Asociar palabras con acciones ejecutables.
3. Permitir sinonimos y traducciones.
4. Incluir ayudas por contexto.
5. Relacionar claves del diccionario con iconos `.svg`.

La carpeta muestra una idea central del proyecto DAV: construir una capa intermedia entre instrucciones humanas, como palabras o comandos de voz, y acciones concretas dentro de FreeCAD.
