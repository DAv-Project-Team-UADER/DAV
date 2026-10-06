# Pruebas automáticas de las correcciones de voz (v1.0.4)

Este documento explica los tests que protegen las correcciones hechas tras el informe
de pruebas funcionales de DAV v1.0.4 (revisión 2): qué verifica cada uno, cómo
ejecutarlo y qué **no** cubre.

| Archivo | Entorno | Qué protege |
|---|---|---|
| `test_voice_fixes.py` | Python del venv (sin FreeCAD) | Gramática de la lista de objetos y frases de color/material |
| `freecad_new_assembly_check.py` | `freecadcmd.exe` (FreeCAD sin interfaz) | Creación del ensamblaje por voz |

## Por qué existen

| Falla del informe | Causa | Corrección | Test |
|---|---|---|---|
| "avanzar" y "buscar por deletreo" no se reconocían en las listas | La lista de objetos no acotaba la gramática de Vosk | `ObjectSelectionInputPrompt.GrammarPhrases` + `askObject` la activa | `ObjectListGrammarTest` |
| "nuevo ensamblaje" figuraba como ejecutado pero no creaba nada | `Assembly_CreateAssembly` queda inactivo (diálogo abierto o ensamblaje raíz existente) y `runCommand` falla en silencio | `new_assembly()` crea el objeto directamente | `freecad_new_assembly_check.py` |
| Color y material inconsistentes | Pasos intermedios sin gramática y dos cuadros por comando | Frases de una sola vez ("pintar rojo") | `OneShotPhrasesTest` |

## Cómo ejecutarlos

Desde la raíz del repositorio (PowerShell o Git Bash).

### Tests unitarios

```bash
Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/.venv/Scripts/python.exe -m unittest Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/tests/test_voice_fixes.py -v
```

Resultado esperado: `Ran 8 tests ... OK`.

Si `InputPrompts` no se puede importar (por ejemplo, falta PySide), los tests de
`ObjectListGrammarTest` se **saltan** con `skipTest` en lugar de fallar. Un resultado
con "skipped" no es una verificación completa: revisar el entorno.

### Chequeo en FreeCAD sin interfaz

```powershell
cmd /c '"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" "<repo>\Dav\scr\ComponentesDAV\IntegracionGUI\GUIFreeCad\tests\freecad_new_assembly_check.py" 2>&1'
```

Resultado esperado: la última línea útil es `CHECK OK`. Si algo falla, el script
imprime el traceback y `CHECK FAILED` y termina con código 1. La salida incluye
mucho texto del solver ("MbD: ...") y porcentajes de avance; es normal.

Los avisos `No se pudo salir del modo edición` y `No se pudo actualizar la vista` son
esperados sin interfaz: `FreeCADGui` no tiene `ActiveDocument` ni `updateGui`.

> **Atención:** FreeCAD carga primero el DAV instalado en
> `%APPDATA%\FreeCAD\v1-1\Mod\DAV`, que es otra copia del código. El script descarta
> los módulos `dic*` y `Workbench*` ya cargados para probar el código **de este
> repositorio**. Si probás con la interfaz, usás la copia instalada: hay que
> reinstalar o sincronizarla para ver los cambios.

## `test_voice_fixes.py`

El archivo carga `_aspecto.py` aislado con un stub de `FreeCAD`, porque esas funciones
no necesitan un documento real.

### `ObjectListGrammarTest` (4 tests)

Prueban `ObjectSelectionInputPrompt.GrammarPhrases(Language)`.

| Test | Verifica |
|---|---|
| `test_spanish_grammar_has_browse_search_confirm_and_cancel` | Están `avanzar`, `buscar`, `buscar por deletreo`, `deletreo`, `okey` y `cancelar` |
| `test_grammar_has_no_duplicates_and_no_up_down` | Sin duplicados; sin `arriba`/`abajo` (en este cuadro no mueven la selección) |
| `test_unknown_language_falls_back_to_spanish` | Un idioma desconocido devuelve la gramática en español |
| `test_every_search_word_of_the_grammar_is_understood_by_the_prompt` | `buscar`, `deletreo` y `deletrear` de la gramática pertenecen a `SearchWords`, es decir, lo que Vosk puede oír dispara la búsqueda |

El último test evita que la gramática y `ProcessFinalText` se desincronicen: una
palabra en la gramática que el cuadro no entiende sería otro fallo silencioso.

### `OneShotPhrasesTest` (4 tests)

Prueban `oneShotPhrases(Language)` de `dic/Selection/_aspecto.py`.

| Test | Verifica |
|---|---|
| `test_colour_and_material_phrases_exist` | Existen `pintar rojo`, `colorear azul`, `pintar de verde`, `poner material acero`, `usar material pla` |
| `test_every_colour_and_material_is_reachable_in_every_language` | Los 12 colores y 16 materiales se pueden decir en es, en y pt |
| `test_phrases_call_the_right_key_without_arguments` | Cada frase se llama sin argumentos y pasa la clave correcta: `red`, `Steel-Generic`, `Steel-X5CrNi18-10` |
| `test_unknown_language_falls_back_to_spanish` | Un idioma desconocido usa las frases en español |

El tercer test reemplaza `paintObject` y `setMaterial` por registradores. Por eso no
toca FreeCAD ni abre cuadros.

## `freecad_new_assembly_check.py`

Ejecuta `new_assembly()` y `new_part()` en un documento nuevo de FreeCAD real y
comprueba, en orden:

1. No hay ensamblaje antes de crearlo (`_ActiveAssembly` devuelve `None`).
2. Tras `new_assembly()`, `_ActiveAssembly` lo encuentra (es la falla original).
3. El objeto es un `Assembly::AssemblyObject`.
4. Tiene su grupo `Assembly::JointGroup`.
5. Llamarlo dos veces no crea un segundo ensamblaje.
6. `new_part()` funciona enseguida (crea `Pieza`).

## Lo que estos tests NO cubren

- **Reconocimiento de voz real.** Los tests no usan Vosk ni micrófono: comprueban que las
  frases estén en la gramática, no que el reconocedor las distinga.
- **Ventana de FreeCAD.** Sin interfaz, `Gui.ActiveDocument.setEdit` falla y se ignora.
  Que el ensamblaje quede en modo edición en la interfaz real sigue sin probarse.
- **Flujos completos de los cuadros** (deletreo, elegir de la lista con `okey`).
- **Juntas, fijar pieza, lista de materiales y vista explosionada.** Siguen requiriendo la
  prueba manual de la sección 5c de la lista de pruebas por voz.
- **Revolución por ángulo.** La corrección (apuntar las frases a `revolution`) no tiene
  test propio.

Estos puntos se repiten a mano con voz real según la lista de pruebas del informe.

## Problemas conocidos del entorno

- `test_real_dictionaries.py` ya fallaba antes de estas correcciones (1 failure y
  1 error: `No module named 'dic'` al cargar el diccionario de TechDraw). No está
  relacionado con estos tests.

## Cómo ampliarlos

- **Nueva frase de una sola vez:** agregar el verbo a `_PAINT_VERBS` o `_MATERIAL_VERBS`
  en `_aspecto.py`; el test de alcanzabilidad la cubre sin cambios.
- **Nuevo color o material:** agregar la fila a `_COLORS` o `_MATERIALS` con sus palabras
  en los tres idiomas; el mismo test falla si falta uno.
- **Nuevo cuadro con gramática propia:** seguir el patrón de `GrammarPhrases` y agregar
  tests equivalentes a `ObjectListGrammarTest`.
- **Nuevo comando de ensamblaje:** agregar sus comprobaciones a
  `freecad_new_assembly_check.py`, después de `new_assembly()`.
