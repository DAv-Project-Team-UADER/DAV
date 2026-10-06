# Documentación de DAV (Español)

**DAV — Diseño Asistido por Voz** es una capa de control por voz sobre [FreeCAD](https://www.freecad.org/) que usa [Vosk](https://alphacephei.com/vosk/) como reconocedor. Esta carpeta reúne la documentación del **desarrollo** del proyecto, para quien quiera entender cómo está hecho, instalarlo desde el código o contribuir.

> Si solo querés usar DAV, el material para usuarios está en el [README principal](../../../README.es.md) (manual de usuario y videotutoriales).

Esta documentación existe también en [English](../en/README.md) y [Português](../pt/README.md).

---

## Por dónde empezar

| Si querés... | Leé |
|---|---|
| Entender el proyecto y cómo se trabaja en él | [Guía de desarrollo](guia-desarrollo-dav.md) |
| Saber qué hay en cada carpeta del repositorio | [Estructura del repositorio](desarrollo/estructura.md) |
| Poner DAV en marcha desde el código | [Puesta en marcha (setup)](desarrollo/setup.md) |
| Instalar DAV | [Windows](guia-instalacion-Windows.md) · [Linux](guia-instalacion-Linux.md) |
| Ver las clases y cómo se relacionan | [Diagramas de clases](diagramas/README.md) |

## Desarrollo

- [Convenciones de código](desarrollo/convenciones.md): nombres, cabezal de licencia, docstrings y principios de diseño.
- [Agregar un comando por voz](desarrollo/agregar-comando.md)
- [Agregar un submenú](desarrollo/agregar-submenu.md)
- [Agregar un diálogo de voz](desarrollo/agregar-prompt.md)
- [Cómo probar y validar](desarrollo/probando.md)
- [Portear DAV a un nuevo idioma](portear-a-nuevo-idioma.md)
- [Regenerar el manual de usuario en PDF](regenerar-manual-pdf.md)
- [GitFlow: historial real del repositorio](gitflow-gitgraph.md)

## Cómo funciona el reconocimiento de voz

- [Diccionario de números y su gramática](numeros-diccionario-gramatica.md)
- [Números por voz: límites y propuesta](numeros-por-voz-limites-y-propuesta.md)
- [Acortador de gramática de Vosk](acortador-gramatica-vosk.md)

## Manuales y guías de uso por voz

- [Manual del Explorer](manual-explorer-voz.md)
- [Manual de selección por voz](manual-selection-voz.md)
- [Manual de croquis y grabado por voz](manual-croquis-y-grabado-voz.md)
- [Guía de las tijeras](guia-tijeras-voz.md)

## Pruebas e informes

- [Pruebas de PartDesign por voz](guia-pruebas-partdesign-voz.md)
- [Pruebas 3D por voz](guia-pruebas-3d-voz.md)
- [Prueba de números con alumnos](guia-prueba-numeros-alumnos.md)
- [Informe de pruebas del banco Draft](informe_pruebas_draftwork.md)

## Estado y planificación

- [Completados](completados-dav.md): problemas ya resueltos y su causa real.
- [Plan de unificación de GUIs](plan-unificacion-guis.md)
- [Plan de migración del hilo de voz a QThread](plan-migracion-hilos-qthread.md)
- [Plan del árbol de objetos navegable](plan_arbol_de_objetos_navegable.md)

## Documentos institucionales y legales

- [Normativas](normativas/): resolución de la Práctica Educativa Territorial y norma IEEE 830.
- [Licencia GPL v3](licencias/)
- [Prototipos de integración](prototipos/README.md) (archivado).

## Otros recursos de esta carpeta

- [`../assets/`](../assets/): gráfico de GitFlow y presentación de ejemplos.
- [`../ejemplo-tijeras/`](../ejemplo-tijeras/): archivos del ejemplo de las tijeras.
- [`../manual/`](../manual/): scripts que generan los manuales PDF.
