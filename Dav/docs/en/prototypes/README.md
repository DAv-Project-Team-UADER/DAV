# Retired prototypes

Code that **is not run**. It is kept as a design reference, not as
part of the program. Nothing here is on DAV's startup path.

> If you are looking for the live engine: `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/`
> — `navigation/browser.py` (`Browser`) + `integration/voice_bootstrap.py`.

## `PruebaIntegracion/`

A complete, standalone DAVCore (40 files, ~2,700 lines): `core/VoiceExplorer.py`,
`core/Navigator.py`, `core/Command.py`, `core/FunctionWrapper.py`,
`modelo/VoskModel.py`, `hilos/GestorDeHilos.py`, its own GUI and tests.

It is the literal implementation of the UML in `CLAUDE.md` (`DAVAgent` + `VoskModel`),
and that is why it is worth keeping as a reference: it shows the project's original
conceptual design before the implementation converged on `Browser`.

It used its own dictionary (`diccionario/`), not the official `Dav/dic/` tree.

## `cad_session.py`, `cad_voice_adapter.py`

The two bridges that would have connected `PruebaIntegracion` to FreeCAD. Nobody ever
called them: `voice_bootstrap.py` builds the engine with `Browser` +
`BrowserVoiceAdapter`, not with `ExploradorVoz` + `CadVoiceAdapter`.

## `voice_aliases.py`

An es/pt synonym table that operated on `NodoContexto` from `PruebaIntegracion`.
Only `cad_session.py` reached it, so it is retired along with it.

> The live equivalent is the `TraduceTo*.py` files in each folder of
> `Dav/dic/`, which serve the same purpose on the official tree.

## Why they were retired (2026-08-10)

See `Dav/docs/es/pendientes-dav.md` §9. Summary: three voice engines ended up
existing in parallel because of simultaneous development, not by design. One remains.

## Note for whoever moves it again

`PruebaIntegracion/` was used as a **filesystem marker** to locate the
`Dav/scr/` root in `integration/dav_paths.py` and in `tests/test_browser.py`. That
has already been changed to `validation/` + `selection/`. If this folder is relocated again,
nothing needs to be touched: nobody looks for it anymore.
