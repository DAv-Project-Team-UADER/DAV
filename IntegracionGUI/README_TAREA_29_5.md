# Browser + Preferences — Documentación de implementación

## ¿Qué es esto?

Este módulo implementa la navegación por voz sobre diccionarios de carpetas para el sistema DAV en FreeCAD.
La idea es que el usuario pueda decir palabras en su idioma y el sistema navegue entre menús y ejecute comandos.

---

## Estado actual

| Parte | Estado |
|---|---|
| Preferences + LanguageCode | ✅ Completo |
| Browser base + BaseContext + Keychain | ✅ Completo |
| Motor de búsqueda (descenso + ascenso) | ❌ Pendiente — ver TODO en `browser.py` |
| Integración con voz (Vosk) | ❌ Pendiente — ver TODO en `voice_bootstrap.py` |

---

## Archivos implementados

### `GUIFreeCad/core/language_code.py`
Enum `LanguageCode` con los tres idiomas: `En`, `Es`, `PT`.
Provee el nombre del archivo de traducción correspondiente (`TraduceToEn`, `TraduceToEs`, `TraduceToPT`).

### `GUIFreeCad/core/preferences.py`
Clase `Preferences` con la variable pública `SetLanguage` (tipo `LanguageCode`).
Cuando `SetLanguage` cambia, notifica a los objetos registrados via callbacks.
El `Browser` se registra acá para recargarse automáticamente al cambiar de idioma.

### `GUIFreeCad/navigation/browser.py`
Clase principal `Browser`. Implementa la navegación por voz.

**Listas públicas:**
- `BaseContext` — comandos del nivel base (`base.py`), fijos, no cambian al navegar
- `Context` — comandos del nivel actual
- `OriginalContext` — snapshot antes de una búsqueda ascendente (para Developer 3)

**Método principal:** `ProcessPhrase(spoken)`
- Si es un comando de `BaseContext` → salta directo a ese contexto ✅
- Si está en `Context` → descender o ejecutar (**TODO**)
- Si no está → buscar hacia arriba (**TODO**)

### `GUIFreeCad/navigation/context_entry.py`
Clase inmutable `ContextEntry` con tres campos:
- `Spoken` — lo que dice el usuario
- `InternalKey` — nombre interno del diccionario
- `Target` — subdiccionario o función ejecutable

Métodos: `IsSubContext()`, `IsCallable()`.

### `GUIFreeCad/navigation/dictionary_loader.py`
Clase `DictionaryLoader`. Carga los archivos del diccionario usando Keychain.

- `LoadBaseModuleDict()` — carga `base.py`
- `LoadTranslateMap(carpeta, idioma)` — carga `TraduceTo*.py` del idioma en esa carpeta
- `ResolveSubFolder(carpeta, clave)` — resuelve la ruta de la subcarpeta
- Propiedad `IsReady` — si la carpeta del diccionario no existe, retorna `False` sin crashear

### `GUIFreeCad/tests/test_browser.py`
10 tests unitarios para Preferences y Browser. **No dependen de ningún archivo en disco** — usan un `MockDictionaryLoader` en memoria.

Para correr los tests:
```
"L:\Programas\Freecad\bin\python.exe" -m unittest discover -s luigiIntegracionV1\GUIFreeCad\tests -v
```

---

## Archivos modificados

### `GUIFreeCad/core/settings.py`
Agregado el setting `auto_voice` (por defecto `False`).
Cuando está activo, el micrófono inicia solo al abrir FreeCAD.

### `GUIFreeCad/ui/preferences_dialog.py`
- Sincroniza `Preferences.SetLanguage` al cambiar idioma en la interfaz
- Nuevo checkbox: **"Micrófono: iniciar al abrir FreeCAD"**

### `GUIFreeCad/integration/voice_bootstrap.py`
Agrega sincronización de `Preferences.SetLanguage` al iniciar la voz.
Contiene **TODO** marcado para que el equipo conecte `BrowserVoiceAdapter` cuando esté el motor de búsqueda listo.

### `GUIFreeCad/integration/cad_session.py`
Corrección: `"pt"` ahora mapea a `"PT"` para Vosk (antes usaba `"ES"` por error).

### `Dav/scr/gui/freecad_wb.py`
- `_force_show_dav_toolbar()` — la barra DAV siempre queda visible al abrir el workbench
- `_auto_start_voice_if_needed()` — si `auto_voice` está activo, el micrófono arranca solo a los 2 segundos de cargar FreeCAD

---

## Qué queda por hacer

### Pendiente 1 — Motor de búsqueda (`browser.py`)

En `ProcessPhrase` hay un bloque **TODO** claro. Hay que implementar:

**Descenso manual:** cuando el usuario dice un comando que está en `Context` y es un subcontexto, bajar a ese nivel y cargar sus comandos.

**Búsqueda ascendente:** cuando el usuario dice algo que no está en el `Context` actual:
1. Guardar `OriginalContext`
2. Subir nivel por nivel usando la pila interna `_stack`
3. Si lo encuentra → ejecutar y actualizar contexto
4. Si no lo encuentra en ningún nivel → restaurar `Context = OriginalContext`

### Pendiente 2 — Integración con voz (`voice_bootstrap.py`)

En `voice_bootstrap.py` hay un **TODO** marcado. Hay que:
1. Completar `BrowserVoiceAdapter` (esqueleto en `integration/browser_voice_adapter.py`, **no está en el repo**)
2. Reemplazar `CadStreamingAdapter` por `BrowserVoiceAdapter`
3. Agregar los tests de integración correspondientes

---

## Estructura del diccionario esperada

```
mi_diccionario/
├── base.py              ← Base = {"explorer": explorer_dict, ...}
├── TraduceToEs.py       ← TraduceToEs = {"explorador": explorer_dict, ...}
├── TraduceToEn.py
├── TraduceToPT.py
└── explorer/
    ├── __init__.py
    ├── explorer.py      ← explorer = {"print": print_cmds, "refresh": lambda...}
    ├── TraduceToEs.py
    └── print/
        ├── print_cmds.py
        └── TraduceToEs.py
```

El `Browser` recibe la ruta raíz del diccionario como parámetro. Si la carpeta no existe, arranca con contextos vacíos sin crashear.
