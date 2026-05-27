# Analisis de `Keychain.py`

`Keychain.py` define una clase llamada `Keychain`. Su objetivo es leer un archivo `.py` que contiene un diccionario y extraer sus claves, valores o nombres de iconos sin ejecutar ese archivo y sin construir realmente el diccionario en memoria.

En simple: funciona como un **lector textual de diccionarios Python**.

Por ejemplo, si tiene este archivo:

```python
draft_workbench = {
    'modification': modification,
    'drafting': drafting,
    'annotation': annotation,
    'array': array,
    'help': ayuda
}
```

`Keychain` puede devolver:

```python
['modification', 'drafting', 'annotation', 'array', 'help']
```

Y si se le pide iconos, genera:

```python
['modification.svg', 'drafting.svg', 'annotation.svg', 'array.svg', 'help.svg']
```

## Idea General

El archivo no usa `eval`, no usa `exec` y tampoco usa `ast`. Es decir, no interpreta Python de verdad. Lee el archivo como texto plano y busca patrones como:

```python
{
    'clave': valor
}
```

o:

```python
dict(clave=valor)
```

Esto es importante porque evita ejecutar codigo externo. Si el archivo que se analiza tuviera imports, funciones o variables, `Keychain` no las ejecuta; simplemente mira los caracteres del archivo.

## Constructor

```python
def __init__(self, FilePath: str):
    self.FilePath = FilePath
    with open(self.FilePath, 'r', encoding='utf-8') as f:
        self._Content = f.read()
```

Cuando creas un objeto:

```python
keychain = Keychain("dic/DraftWorkbench.py")
```

La clase guarda la ruta en `self.FilePath` y lee todo el contenido del archivo dentro de `self._Content`.

Desde ese momento, todos los metodos trabajan sobre ese texto cargado.

## `GetKeys`

```python
def GetKeys(self):
```

Este metodo devuelve las claves principales del diccionario.

Primero busca una llave `{`:

```python
start = self._Content.find('{')
```

Si encuentra una, asume que el archivo contiene un diccionario literal, como:

```python
mi_diccionario = {
    'uno': 1,
    'dos': 2
}
```

Entonces llama a:

```python
self._extract_keys_from_literal(start)
```

Si no encuentra `{`, busca `dict(`:

```python
start = self._Content.find('dict(')
```

Esto sirve para casos como:

```python
pepino = dict(llave1="pepino 2", llave2="valor2")
```

Entonces llama a:

```python
self._extract_keys_from_dict_call(start)
```

Si no encuentra ni `{` ni `dict(`, lanza:

```python
ValueError("No dictionary definition found...")
```

## `GetValues`

```python
def GetValues(self):
```

Hace algo parecido a `GetKeys`, pero devuelve los valores en bruto, como texto.

Con este diccionario:

```python
draft_workbench = {
    'modification': modification,
    'drafting': drafting
}
```

devolveria algo como:

```python
['modification', 'drafting']
```

No devuelve los objetos reales `modification` o `drafting`; devuelve las palabras como texto.

Esto es clave: no resuelve imports, no carga modulos, no evalua variables.

## `GetIcons`

```python
def GetIcons(self, base_dir=None):
```

Este metodo toma las claves y les agrega `.svg`.

Por ejemplo, si `GetKeys()` devuelve:

```python
['modification', 'drafting', 'help']
```

entonces `GetIcons()` devuelve:

```python
['modification.svg', 'drafting.svg', 'help.svg']
```

Si le pasas un directorio:

```python
keychain.GetIcons(base_dir="Keychain/dic")
```

entonces filtra y devuelve solamente los iconos que realmente existen como archivos en esa carpeta.

Internamente hace esto:

```python
full_path = os.path.join(base_dir, icon)
if os.path.isfile(full_path):
    existing.append(icon)
```

O sea: no inventa iconos existentes, solo propone nombres a partir de las claves y opcionalmente verifica si estan en disco.

## `GetAllKeys`

```python
def GetAllKeys(self):
    return self.GetKeys()
```

Es simplemente un alias de `GetKeys`. Esta mantenido por compatibilidad, probablemente porque antes otro codigo llamaba a `GetAllKeys()`.

## Como Lee Diccionarios Literales

El metodo principal para diccionarios con `{}` es:

```python
_extract_keys_from_literal(self, start_idx)
```

Este metodo recorre el texto caracter por caracter. Usa una variable llamada `depth` para saber en que nivel de llaves esta.

Ejemplo:

```python
{
    'a': 1,
    'b': {
        'interno': 2
    }
}
```

Cuando ve `{`, aumenta `depth`.

Cuando ve `}`, baja `depth`.

Solo extrae claves cuando:

```python
depth == 1
```

Eso significa que solo toma claves del diccionario principal, no de diccionarios internos.

En este ejemplo:

```python
{
    'a': 1,
    'b': {
        'interno': 2
    }
}
```

devolveria:

```python
['a', 'b']
```

No devolveria `'interno'`.

## Como Detecta Una Clave Literal

Busca strings entre comillas:

```python
'clave'
"clave"
```

Luego verifica que despues venga `:`. Si encuentra:

```python
'modification':
```

guarda:

```python
modification
```

Tambien contempla caracteres escapados dentro de strings, por ejemplo:

```python
'clave\'rara'
```

## Como Extrae Valores Literales

El metodo:

```python
_extract_values_from_literal(self, start_idx)
```

tambien recorre el diccionario, encuentra una clave, busca los dos puntos `:`, y despues toma todo lo que haya hasta la coma correspondiente o hasta el cierre del diccionario.

Ejemplo:

```python
{
    'a': 123,
    'b': "hola",
    'c': [1, 2, 3]
}
```

devolveria:

```python
['123', '"hola"', '[1, 2, 3]']
```

El metodo intenta respetar strings y estructuras internas como listas o diccionarios para no cortar por una coma que este adentro de un valor.

## Como Lee `dict(...)`

Para archivos como:

```python
pepino = dict(llave1="pepino 2", llave2="valor2")
```

usa:

```python
_extract_keys_from_dict_call(self, start_idx)
```

Ahi las claves no van entre comillas, sino que son nombres de argumentos:

```python
llave1=
llave2=
```

Entonces busca identificadores validos antes de un `=`.

Devolveria:

```python
['llave1', 'llave2']
```

Para los valores usa:

```python
_extract_values_from_dict_call(self, start_idx)
```

y extrae el texto que aparece despues del `=`.

## Relacion Con `main.py`

En `main.py`, la clase se usa asi:

```python
keychain = Keychain(full_path)
keys = keychain.GetAllKeys()
icons = keychain.GetIcons(base_dir=dict_dir)
```

El programa pide al usuario un archivo dentro de `Keychain/dic`, lo analiza con `Keychain`, imprime las claves encontradas y despues intenta abrir los iconos `.svg` que coincidan con esas claves.

Por eso la clase se llama `Keychain`: funciona como un llavero que extrae las llaves de un diccionario.

## Limitaciones

El codigo es util, pero tiene varias limitaciones:

1. No parsea Python realmente. Solo escanea texto.
2. Si hay una `{` antes del diccionario real, por ejemplo en un comentario o string, puede confundirse.
3. En diccionarios literales solo detecta claves escritas como strings, por ejemplo `'clave'` o `"clave"`. No detectaria bien claves como `123: valor` o `variable: valor`.
4. En `dict(...)`, solo detecta claves tipo identificador, como `llave1=valor`. No sirve para claves con espacios o simbolos.
5. No ejecuta imports ni resuelve valores. Si el valor es `modification`, devuelve el texto `"modification"`, no el objeto importado.
6. El lector de `dict(...)` puede comportarse raro con algunos cierres `)` o valores complejos, porque esta hecho manualmente caracter por caracter.
