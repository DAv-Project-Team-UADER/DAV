# Prototipos retirados

Código que **no se ejecuta**. Se conserva como referencia de diseño, no como
parte del programa. Nada de acá está en el camino de arranque de DAV.

> Si buscás el motor vivo: `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/`
> — `navigation/browser.py` (`Browser`) + `integration/voice_bootstrap.py`.

## `PruebaIntegracion/`

DAVCore completo y autónomo (40 archivos, ~2.700 líneas): `core/VoiceExplorer.py`,
`core/Navigator.py`, `core/Command.py`, `core/FunctionWrapper.py`,
`modelo/VoskModel.py`, `hilos/GestorDeHilos.py`, GUI y tests propios.

Es la implementación literal del UML de `CLAUDE.md` (`DAVAgent` + `VoskModel`),
y por eso vale como referencia: muestra el diseño conceptual original del
proyecto antes de que la implementación convergiera en `Browser`.

Usaba su propio diccionario (`diccionario/`), no el árbol oficial `Dav/dic/`.

## `cad_session.py`, `cad_voice_adapter.py`

Los dos puentes que habrían conectado `PruebaIntegracion` con FreeCAD. Nunca los
llamó nadie: `voice_bootstrap.py` arma el motor con `Browser` +
`BrowserVoiceAdapter`, no con `ExploradorVoz` + `CadVoiceAdapter`.

## `voice_aliases.py`

Tabla de sinónimos es/pt que operaba sobre `NodoContexto` de `PruebaIntegracion`.
Sólo lo alcanzaba `cad_session.py`, así que se retira con él.

> El equivalente vivo son los archivos `TraduceTo*.py` de cada carpeta de
> `Dav/dic/`, que cumplen la misma función sobre el árbol oficial.

## Por qué se retiraron (2026-08-10)

Ver `Dav/docs/pendientes-dav.md` §9. Resumen: llegaron a existir tres motores de
voz en paralelo por desarrollo simultáneo, no por diseño. Quedó uno.

## Nota para quien lo mueva de nuevo

`PruebaIntegracion/` se usaba como **marcador de filesystem** para localizar la
raíz `Dav/scr/` en `integration/dav_paths.py` y en `tests/test_browser.py`. Eso
ya se cambió a `validation/` + `selection/`. Si se reubica esta carpeta otra vez,
no hace falta tocar nada: ya no la busca nadie.
