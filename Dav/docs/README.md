# Documentación DAV

Índice de `Dav/docs/`. Cada carpeta agrupa un tipo de documento.

---

## Por dónde empezar

| Si querés… | Leé |
|---|---|
| Saber qué falta hacer | [`estado/pendientes-dav.md`](estado/pendientes-dav.md) |
| Saber si algo ya se resolvió | [`estado/completados-dav.md`](estado/completados-dav.md) |
| Probar el sistema por voz | [`guias/`](#guias--probar-por-voz) |
| Entender una clase | [`diagramas/`](diagramas/README.md) |
| Tocar el motor de voz | [`referencia/acortador-gramatica-vosk.md`](referencia/acortador-gramatica-vosk.md) |

> **Antes de tocar diccionarios o navegación**, leer
> [`estado/pendientes-dav.md`](estado/pendientes-dav.md): tiene las convenciones
> y los modos de falla que ya costaron una sesión de depuración cada uno.

---

## `estado/` — qué está hecho y qué falta

| Archivo | Contenido |
|---|---|
| [`pendientes-dav.md`](estado/pendientes-dav.md) | Lo que sigue abierto: hallazgos de auditoría, convenciones, y qué falta para el MVP. **El documento más importante del proyecto.** |
| [`completados-dav.md`](estado/completados-dav.md) | Lo ya resuelto, con la **causa real** de cada caso. Consultar antes de re-diagnosticar algo que parece conocido. |

## `guias/` — probar por voz

Guías paso a paso, con las frases verificadas contra los diccionarios.

| Archivo | Cubre |
|---|---|
| [`guia-prueba-nombre-y-seleccion.md`](guias/guia-prueba-nombre-y-seleccion.md) | Nombrar un objeto al crearlo y después seleccionarlo diciendo su nombre |
| [`guia-pruebas-3d-voz.md`](guias/guia-pruebas-3d-voz.md) | Geometría con medidas dictadas, extrusión a 3D y juntas (PR #208, #209, #213) |
| [`guia-pruebas-partdesign-voz.md`](guias/guia-pruebas-partdesign-voz.md) | PartDesign con medidas dictadas: sólidos, cortes y acabados |
| [`guia-prueba-numeros-alumnos.md`](guias/guia-prueba-numeros-alumnos.md) | Guía para alumnos: probar funciones que reciben números por voz |

## `manuales/` — cómo se usa cada módulo

| Archivo | Módulo |
|---|---|
| [`manual-explorer-voz.md`](manuales/manual-explorer-voz.md) | Explorer: nuevo, abrir, guardar, exportar |
| [`manual-selection-voz.md`](manuales/manual-selection-voz.md) | Selection y el circuito de `CreateObjects` |

## `referencia/` — cómo funciona por dentro

| Archivo | Tema |
|---|---|
| [`acortador-gramatica-vosk.md`](referencia/acortador-gramatica-vosk.md) | Cómo se acota la gramática de Vosk al contexto activo. **Leer antes de tocar `SetGrammar` o el loop de audio.** |
| [`numeros-diccionario-gramatica.md`](referencia/numeros-diccionario-gramatica.md) | Implementación del reconocimiento de números |
| [`numeros-por-voz-limites-y-propuesta.md`](referencia/numeros-por-voz-limites-y-propuesta.md) | Qué números se pueden dictar hoy y cuál es el techo real |
| [`README-linux.md`](referencia/README-linux.md) | Script de arranque en Linux |

## `planes/` — diseños y migraciones

| Archivo | Estado |
|---|---|
| [`plan-unificacion-guis.md`](planes/plan-unificacion-guis.md) | Etapas 1-4 hechas, queda la 5 |
| [`plan_arbol_de_objetos_navegable.md`](planes/plan_arbol_de_objetos_navegable.md) | Completado y superado — se conserva por el contrato de datos |
| [`plan-migracion-hilos-qthread.md`](planes/plan-migracion-hilos-qthread.md) | Escrito para `InterfazDAV`, ya retirada. Queda como referencia del criterio |

## `diagramas/` — una clase, un archivo

Diagramas Mermaid con el nombre de la clase (`Browser.md`, `DavPanel.md`…).
Índice y vista general en [`diagramas/README.md`](diagramas/README.md).

## `prototipos/` — código retirado que se conserva

`PruebaIntegracion` y otros experimentos que ya no forman parte del programa,
guardados como referencia de diseño.

## `informes/` · `licencias/` · `normativas/`

Material de cátedra y documentación formal (GPL, IEEE 830).

---

## Convenciones al agregar un documento

- **Una guía de prueba** va en `guias/`, con las frases **verificadas contra los
  `TraduceTo*.py` reales** — no de memoria.
- **Un hallazgo** va en `estado/pendientes-dav.md` como sección numerada, con la
  causa real y qué quedó **sin verificar**.
- Cuando algo se cierra, se mueve a `estado/completados-dav.md`.
- Los enlaces entre documentos son relativos; si movés un archivo, verificá que
  no queden rotos.
