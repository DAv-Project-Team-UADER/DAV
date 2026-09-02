# Diagramas de clases — DAV

Un archivo por clase, con el nombre de la clase. Cada uno tiene el diagrama en
Mermaid, la tabla de responsabilidades y las notas de diseño que no se ven en la
firma de los métodos.

> Antes esto era un único `diagramas_clases_DAV.md`. Se separó y se actualizó:
> documentaba `MainWindow` y `VoiceWorker`, que ya no existen (ver
> [`completados-dav.md`](../estado/completados-dav.md)).

## Motor de navegación

| Clase | Rol |
| --- | --- |
| [`Browser`](Browser.md) | Recorre el árbol de `Dav/dic/` y resuelve cada frase |
| [`ContextEntry`](ContextEntry.md) | Una entrada del contexto: frase → clave → target |
| [`DictionaryLoader`](DictionaryLoader.md) | Carga los módulos del diccionario desde disco |

## Voz

| Clase | Rol |
| --- | --- |
| [`DavVoiceService`](DavVoiceService.md) | Singleton del micrófono y el recognizer Vosk |
| [`BrowserVoiceAdapter`](BrowserVoiceAdapter.md) | Une la voz con el `Browser` y publica al panel |

Cómo se acota la gramática al contexto:
[`acortador-gramatica-vosk.md`](../referencia/acortador-gramatica-vosk.md).

## Interfaz y configuración

| Clase | Rol |
| --- | --- |
| [`DavPanel`](DavPanel.md) | El widget acoplado dentro de FreeCAD |
| [`Preferences`](Preferences.md) | Idioma activo y persistencia de la configuración |
| [`DAVWorkbench`](DAVWorkbench.md) | Workbench de FreeCAD y comandos de la barra |
| [`Keychain`](Keychain.md) | Lee diccionarios `.py` sin ejecutarlos |

---

## Vista general

Cómo se conectan las piezas cuando el usuario dice algo.

```mermaid
classDiagram
    namespace Workbench {
        class DAVWorkbench
        class voice_bootstrap
    }

    namespace Voz {
        class DavVoiceService
        class BrowserVoiceAdapter
    }

    namespace Navegacion {
        class Browser
        class ContextEntry
        class DictionaryLoader
    }

    namespace Interfaz {
        class DavPanel
        class Preferences
    }

    DAVWorkbench ..> voice_bootstrap : arranca la voz
    voice_bootstrap ..> Browser : construye
    voice_bootstrap ..> BrowserVoiceAdapter : construye
    voice_bootstrap ..> DavVoiceService : start_cad

    DavVoiceService ..> BrowserVoiceAdapter : frase reconocida
    BrowserVoiceAdapter ..> Browser : ProcessPhrase
    BrowserVoiceAdapter ..> DavVoiceService : set_grammar
    BrowserVoiceAdapter ..> DavPanel : historial y contexto

    Browser o-- DictionaryLoader : carga Dav/dic
    Browser ..> ContextEntry : construye
    Browser o-- Preferences : idioma activo
    Preferences ..> Browser : avisa cambio de idioma
```

## El recorrido de una frase

```mermaid
flowchart TD
    A["Usuario dice «archivo»"] --> B[DavVoiceService<br/>hilo del micrófono]
    B --> C[BrowserVoiceAdapter<br/>_extract_token]
    C --> D{¿es enviar<br/>o cancelar?}
    D -->|cancelar| E[descarta]
    D -->|enviar| F[cierra la frase]
    D -->|comando| G[Browser.ProcessPhrase]
    F --> G
    G --> H{¿qué es?}
    H -->|submenú| I[desciende un nivel]
    H -->|callable| J[ejecuta en FreeCAD]
    H -->|nav| K[subir / contexto]
    I --> L[recalcula gramática]
    K --> L
    L --> M[DavVoiceService.set_grammar]
    J --> N[publica en DavPanel]
    I --> N
```
