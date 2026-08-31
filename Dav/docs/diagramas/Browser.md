# Browser

> **Archivo:** `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/navigation/browser.py`

Motor de navegación del árbol de comandos por voz. Recorre `Dav/dic/`
manteniendo una pila de contextos: cada frase reconocida se resuelve contra el
nivel actual, y si es un submenú se desciende.

Es el `DAVAgent` del diseño conceptual original, con otro nombre y otra
implementación: `ProcessPhrase` + `DictionaryLoader` en vez de
`latentListening` + `searchInstruction`.

```mermaid
classDiagram
    class Browser {
        +list~ContextEntry~ BaseContext
        +list~ContextEntry~ Context
        +list~ContextEntry~ OriginalContext
        -Preferences _prefs
        -DictionaryLoader _loader
        -LanguageCode _language
        -list~_ContextFrame~ _stack
        -dict _base_translate
        -dict _base_module
        -dict _nav_translate
        -dict _nav_actions
        -Callable _on_execute
        -Callable _on_descend
        -Callable _on_context_change

        +SetLanguage() LanguageCode
        +CurrentContextName() String
        +ContextPath() String
        +DescribeContext() String
        +GetNavWords(action) set~String~
        +GetSpokenPhrases() list~String~
        +ResetFromBase() void
        +ProcessPhrase(spoken) BrowserResult
        -_AscendOneLevel() String
        -_DescendToSubContext(entry) bool
        -_SearchUpwardAndExecute(spoken) BrowserResult
        -_ResolveNavAction(spoken) Callable
        -_ExecuteNavAction(action) BrowserResult
        -_BuildBaseContextEntries() list~ContextEntry~
        -_BuildContextForFrame(frame) list~ContextEntry~
        -_NotifyContextChanged() void
        -_OnLanguageChanged(prev, new) void
    }

    class _ContextFrame {
        <<dataclass>>
        +Path Folder
        +dict ModuleDict
        +String InternalName
    }

    class BrowserResult {
        <<dataclass>>
        +bool Success
        +String Action
        +String Message
    }

    Browser "1" *-- "1..*" _ContextFrame : pila de navegación
    Browser ..> BrowserResult : devuelve
    Browser "1" o-- "1" DictionaryLoader : carga diccionarios
    Browser "1" o-- "1" Preferences : idioma activo
    Browser ..> ContextEntry : construye
```

## Responsabilidades

| Método | Qué hace |
| --- | --- |
| `ProcessPhrase(spoken)` | Punto de entrada. Resuelve una frase contra el contexto activo: comando de navegación, salto a raíz, descenso a submenú, ejecución, o búsqueda ascendente |
| `GetSpokenPhrases()` | Gramática de Vosk del nivel activo. Ver [`acortador-gramatica-vosk.md`](../acortador-gramatica-vosk.md) |
| `GetNavWords(action)` | Palabras ligadas a un sentinel de `NavCommands` (`up`, `send`, `cancel`, `show_context`) en el idioma activo |
| `DescribeContext()` | Texto legible de dónde está parado el usuario y qué puede decir |
| `ResetFromBase()` | Recarga todo desde `base.py`. Se dispara al cambiar de idioma |

## Notas de diseño

- **No conoce FreeCAD.** Ejecuta callables que vienen de los diccionarios; quién
  los provee es problema del `DictionaryLoader`.
- **Un idioma por vez.** `_OnLanguageChanged` está registrado en `Preferences`,
  así que cambiar el idioma reconstruye los contextos.
- `_on_context_change` notifica a quien tenga que recalcular la gramática de voz.
  Hoy lo usa `BrowserVoiceAdapter`.
