# Diagrama de Flujo: Programa con `Keychain` y Diccionario de Comandos

Este diagrama describe como podria funcionar un programa que use `Keychain.py` junto con un diccionario como `ejemplo de diccionario terminado`.

El objetivo es:

1. Recibir un diccionario raiz, por ejemplo `explorer.py`.
2. Recibir un idioma, por ejemplo espanol.
3. Recuperar los comandos de voz disponibles para ese idioma.
4. Cambiar de contexto si el comando reconocido apunta a un subdiccionario.
5. Si no hay coincidencia en el contexto actual, buscar de forma ascendente en los contextos superiores.
6. Diferenciar comandos repetidos segun la carpeta o contexto donde fueron encontrados.
7. Si no hay coincidencia en ningun nivel, imprimir error.

## Diagrama Principal

```mermaid
flowchart TD
    A([Inicio]) --> B[Recibir diccionario raiz e idioma]
    B --> C[Ubicar carpeta del diccionario raiz]
    C --> D[Crear pila de contextos]
    D --> E[Contexto actual = raiz]

    E --> F[Buscar archivo de idioma en el contexto actual]
    F --> G{Existe archivo de idioma?}

    G -- Si --> H[Usar Keychain sobre archivo de idioma]
    H --> I[Obtener comandos de voz del idioma]

    G -- No --> J[Usar Keychain sobre archivo base del contexto]
    J --> K[Obtener comandos base]

    I --> L[Esperar comando de voz]
    K --> L

    L --> M[Normalizar comando reconocido]
    M --> N[Iniciar busqueda desde contexto actual]

    N --> O[Buscar en archivo de idioma del contexto evaluado]
    O --> P{Coincide en idioma?}

    P -- Si --> Q[Recuperar resultado con ruta del contexto]
    P -- No --> R[Buscar en archivo base del contexto evaluado]

    R --> S[Archivo .py que no inicia con TraduceTo/TranslateTo y no es ayuda.py]
    S --> T[Usar Keychain sobre archivo base]
    T --> U{Coincide en archivo base?}

    U -- Si --> Q
    U -- No --> V{Hay contexto padre?}

    V -- Si --> W[Subir al contexto padre]
    W --> O

    V -- No --> X[Imprimir error: comando no reconocido]
    X --> L

    Q --> Y{El resultado es un subdiccionario?}

    Y -- Si --> Z[Cambiar contexto al subdiccionario encontrado]
    Z --> AA[Actualizar pila de contextos]
    AA --> F

    Y -- No --> AB{El resultado es un comando ejecutable?}
    AB -- Si --> AC[Ejecutar comando]
    AC --> L

    AB -- No --> AD[Imprimir error: accion invalida]
    AD --> L
```

## Version Resumida del Flujo

```mermaid
flowchart LR
    A[Diccionario raiz + idioma] --> B[Cargar comandos del idioma]
    B --> C[Escuchar comando de voz]
    C --> D[Buscar desde contexto actual]
    D --> E{Coincide en idioma o base?}
    E -- Si --> F{Es subdiccionario?}
    F -- Si --> G[Cambiar contexto]
    G --> B
    F -- No --> H[Ejecutar comando]
    H --> C
    E -- No --> I{Hay contexto padre?}
    I -- Si --> J[Subir un nivel]
    J --> E
    I -- No --> K[Error]
    K --> C
```

## Explicacion Paso a Paso

### 1. Entrada del programa

El programa recibe dos datos iniciales:

```text
diccionario raiz = explorer.py
idioma = espanol
```

Con esos datos se ubica la carpeta donde esta el diccionario principal:

```text
ejemplo de diccionario terminado/
```

El contexto inicial pasa a ser `explorer`.

### 2. Carga de comandos por idioma

Si el idioma elegido es espanol, el programa deberia buscar un archivo de traduccion como:

```text
TraduceToEs.py
```

Tambien podria contemplar variantes de nombre, por ejemplo:

```text
TranslateToEs.py
TraduceToES.py
```

Una vez encontrado el archivo, se usa `Keychain` para recuperar sus claves.

Ejemplo:

```python
keychain = Keychain("TraduceToEs.py")
comandos_voz = keychain.GetKeys()
```

Eso permite obtener comandos de voz como:

```text
Archivo
editar
imprimir
refrescar
foto
ayuda
```

Estos son los comandos aceptados en el contexto actual.

### 3. Reconocimiento del comando

El programa espera una entrada de voz ya convertida a texto:

```text
"archivo"
```

Antes de comparar, conviene normalizar el texto:

```text
Archivo -> archivo
 archivo  -> archivo
```

La normalizacion puede incluir:

1. Pasar a minusculas.
2. Quitar espacios al inicio y al final.
3. Opcionalmente quitar tildes.
4. Unificar multiples espacios.

### 4. Coincidencia con comandos del idioma

El programa compara el texto reconocido con las claves del archivo de idioma.

Si coincide, recupera el valor asociado.

Ejemplo conceptual:

```python
'Archivo': file
```

En ese caso, `Archivo` apunta al subdiccionario `file`.

### 5. Si coincide con un subdiccionario

Si el comando reconocido apunta a un diccionario y no a una accion final, el programa debe cambiar de contexto.

Ejemplo:

```text
contexto actual = explorer
comando reconocido = archivo
valor asociado = file
```

Entonces el nuevo contexto pasa a ser:

```text
contexto actual = file
```

El programa entra a:

```text
ejemplo de diccionario terminado/file/
```

Y vuelve a cargar los comandos aceptados para ese contexto.

Para espanol, buscaria:

```text
file/TraduceToEs.py
```

Ahora los comandos aceptados podrian ser:

```text
nuevo
abrir
cerrar
guardar
salvar
guardar como
salvar como
ayuda
```

Esto cumple la condicion B: cuando se entra a un subdiccionario, cambian los comandos que acepta el programa.

### 6. Si no coincide en el contexto actual

Si el comando no aparece en el archivo de traduccion del contexto actual, el programa debe buscar en el archivo base de esa misma capa.

El archivo base es el `.py` principal del contexto, excluyendo:

```text
TraduceTo...
TranslateTo...
ayuda.py
```

Por ejemplo, en la raiz:

```text
explorer.py
```

En la carpeta `file`:

```text
file.py
```

En la carpeta `edit`:

```text
edit.py
```

En la carpeta `print`:

```text
print_cmds.py
```

El programa vuelve a usar `Keychain`:

```python
keychain_base = Keychain("explorer.py")
comandos_base = keychain_base.GetKeys()
```

Si el usuario dijo `file`, aunque no haya usado la traduccion `Archivo`, igual podria coincidir con el comando base.

Esto cumple la condicion C.

### 7. Busqueda ascendente

Si el comando no aparece ni en el archivo de idioma ni en el archivo base del contexto actual, el programa debe subir al contexto padre y repetir la busqueda.

Por ejemplo, si el contexto actual es:

```text
explorer/file
```

el orden de busqueda seria:

```text
1. file/TraduceToEs.py
2. file/file.py
3. TraduceToEs.py
4. explorer.py
```

Si el contexto actual fuera mas profundo, el programa seguiria subiendo nivel por nivel hasta llegar a la raiz.

La regla principal es:

```text
Siempre gana la coincidencia encontrada en el contexto mas cercano al actual.
```

Esto permite diferenciar comandos repetidos. Por ejemplo, si `edit` y `doc` tuvieran un comando llamado `undo`, no alcanza con saber que existe `undo`; tambien hay que saber desde que contexto se lo encontro.

Ejemplo:

```text
explorer/edit/undo
explorer/doc/undo
```

Aunque ambos se llamen `undo`, pueden ejecutar acciones diferentes.

Por eso el resultado de la busqueda deberia guardar informacion como:

```python
{
    "comando": "undo",
    "contexto": "explorer/edit",
    "archivo": "edit.py",
    "accion": accion_encontrada
}
```

### 8. Si coincide con el archivo de idioma o con el archivo base

Si el comando coincide con una clave del archivo de idioma o del archivo base, se aplica la misma decision:

```text
Es subdiccionario? -> cambiar contexto
Es comando final? -> ejecutar
```

Ejemplo:

```text
comando reconocido = screenshot
```

En `explorer.py` existe:

```python
'screenshot': lambda: Gui.runCommand('Std_ViewScreenShot', 0)
```

Entonces el programa ejecuta la captura de pantalla.

### 9. Si no coincide con nada

Si no coincide con:

1. El archivo de idioma del contexto actual.
2. El archivo base del contexto actual.
3. Los archivos de idioma de los contextos superiores.
4. Los archivos base de los contextos superiores.

Entonces el programa imprime error:

```text
Error: comando no reconocido
```

Esto cumple la condicion D.

## Pseudocodigo

```python
def ejecutar_programa(diccionario_raiz, idioma):
    pila_contextos = [crear_contexto(diccionario_raiz)]

    while True:
        comando = escuchar_comando()
        comando = normalizar(comando)

        resultado = buscar_ascendente(
            comando=comando,
            pila_contextos=pila_contextos,
            idioma=idioma,
        )

        if resultado is None:
            print("Error: comando no reconocido")
            continue

        accion = resultado["accion"]

        if es_subdiccionario(accion):
            nuevo_contexto = cambiar_a_subdiccionario(
                contexto_origen=resultado["contexto"],
                subdiccionario=accion,
            )
            pila_contextos.append(nuevo_contexto)
            continue

        if es_comando_ejecutable(accion):
            accion()
            continue

        print("Error: accion invalida")


def buscar_ascendente(comando, pila_contextos, idioma):
    for contexto in reversed(pila_contextos):
        resultado = buscar_en_contexto(comando, contexto, idioma)

        if resultado is not None:
            return resultado

    return None


def buscar_en_contexto(comando, contexto, idioma):
    comandos_idioma = cargar_comandos_idioma(contexto, idioma)
    resultado = buscar(comando, comandos_idioma)

    if resultado is not None:
        return {
            "accion": resultado,
            "contexto": contexto,
            "origen": "idioma",
        }

    comandos_base = cargar_comandos_base(contexto)
    resultado = buscar(comando, comandos_base)

    if resultado is not None:
        return {
            "accion": resultado,
            "contexto": contexto,
            "origen": "base",
        }

    return None
```

## Regla Para Encontrar El Archivo Base

Dentro de cada carpeta, el archivo base puede detectarse asi:

```text
Tomar archivos .py
Descartar archivos que empiecen con TraduceTo
Descartar archivos que empiecen con TranslateTo
Descartar ayuda.py
El archivo restante es el diccionario base de esa capa
```

Ejemplo en la raiz:

```text
explorer.py        <- archivo base
ayuda.py           <- se descarta
TraduceToEs.py     <- se descarta
TraduceToEn.py     <- se descarta
TraduceToPT.py     <- se descarta
```

Ejemplo en `file/`:

```text
file.py            <- archivo base
ayuda.py           <- se descarta
TraduceToEs.py     <- se descarta
TraduceToEn.py     <- se descarta
TraduceToPT.py     <- se descarta
```

## Resultado Esperado

Con este flujo, el programa puede:

1. Arrancar desde `explorer.py`.
2. Cargar comandos de voz en espanol desde `TraduceToEs.py`.
3. Entrar a subdiccionarios como `file`, `edit`, `print` o `doc`.
4. Cambiar dinamicamente los comandos aceptados segun el contexto.
5. Buscar comandos base si no hay coincidencia con la traduccion.
6. Subir a contextos superiores si no encuentra el comando en la capa actual.
7. Diferenciar comandos repetidos por ruta, por ejemplo `explorer/edit/undo` y `explorer/doc/undo`.
8. Informar error si el comando no existe en ningun nivel valido.
