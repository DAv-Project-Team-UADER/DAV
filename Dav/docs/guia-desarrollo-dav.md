# Guía de desarrollo de DAV

> **DAV — Diseño Asistido por Voz**
> Práctica Educativa Territorial — Facultad de Ciencia y Tecnología (FCyT) — UADER

Esta guía explica **cómo se desarrolla y contribuye al proyecto DAV**: cómo
ponerlo en marcha, qué convenciones seguir, cómo agregar un comando por voz y
cómo probar los cambios. Está pensada para integrantes del equipo que se
suman al desarrollo, tanto para el código propio de DAV como para el
diccionario de comandos por voz.

Está escrita desde lo aprendido en la práctica. Si algo quedó desactualizado o
cambiás una convención, **actualizá esta guía** en el mismo PR que toca el
código.

---

## Índice

| Sección | Contenido |
|---|---|
| [Estructura del repositorio](desarrollo/estructura.md) | Qué hace cada carpeta del repo y dónde vive cada cosa |
| [Puesta en marcha (setup)](desarrollo/setup.md) | Cómo clonar, instalar dependencias, modelos y correr DAV en FreeCAD |
| [Convenciones de código](desarrollo/convenciones.md) | Nombres, cabezal obligatorio, docstrings, principios de diseño |
| [Agregar un comando por voz](desarrollo/agregar-comando.md) | Paso a paso con ejemplo real, desde el diccionario hasta el TraduceTo |
| [Cómo probar y validar](desarrollo/probando.md) | Pruebas manuales, qué esperar, y enlaces a las guías existentes |

---

## Resumen rápido

- **DAV** es una capa de control por **voz** sobre **FreeCAD** usando **Vosk**
  como reconocedor.
- El código propio vive en `Dav/`; el árbol de comandos por voz en `Dav/dic/`;
  el motor que recorre ese árbol es `Browser`
  (`Dav/scr/.../navigation/browser.py`).
- Las frases habladas se definen en los `TraduceToEs.py` / `TraduceToEn.py` /
  `TraduceToPT.py` de cada carpeta; el diccionario maestro de cada carpeta
  enlaza las claves internas con callables de FreeCAD.
- Regla de oro: **los subcontextos van anidados bajo su propia clave**, nunca
  aplanados con `.update(sub_dict)`. Ver [pendientes-dav.md](pendientes-dav.md) §4.

---

## Material de referencia

- **[CLAUDE.md](../../CLAUDE.md)** — documentación general del proyecto:
  arquitectura, GitFlow, modelo de voz, licencias. Es la fuente de la mayoría
  de las convenciones citadas acá.
- **[pendientes-dav.md](pendientes-dav.md)** — lo que sigue abierto. **Leer
  antes de tocar diccionarios o navegación.**
- **[completados-dav.md](completados-dav.md)** — problemas ya resueltos y su
  causa real. Consultar antes de re-diagnosticar algo conocido.
- `README.md` / `README.es.md` / `README.pt.md` — presentación del proyecto.
