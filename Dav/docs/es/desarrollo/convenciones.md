# Convenciones de código

Estas son las convenciones del proyecto DAV. Aplican a **todo el código propio**
(el que vive en `Dav/`). Los archivos preexistentes de FreeCAD conservan sus
propias reglas (y su cabezal original).

> Fuente principal: `CLAUDE.md` del repo.

## Nomenclatura

| Tipo | Convención | Ejemplo |
|---|---|---|
| Clases | `PascalCase` | `DavAgent`, `VoskModel` |
| Atributos / Propiedades | `PascalCase` | `LineColor`, `ShapeColor` |
| Funciones / Métodos | `camelCase` (minúscula inicial) | `addObject()`, `recompute()` |
| Uso interno | `_guiónBajo` | `_internalMethod` |

## Organización de archivos

- **Una clase = un archivo**
- **Un diccionario = un archivo**
- El nombre del archivo es igual al nombre de la clase (`DavAgent.py`)

## Cabezal obligatorio (todos los archivos propios)

Cada archivo propio DAV debe empezar con este cabezal de licencia:

```python
# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
```

> Los archivos de FreeCAD preexistentes **conservan su cabezal original**
> (LGPL-2.1-or-later). No los reemplaces.

## Docstrings

- Toda **clase y método público** debe tener un docstring en **inglés**.
- Formato: primera línea corta (resumen), línea en blanco, luego secciones
  `Args:`, `Returns:`, `Example::` según corresponda.
- El docstring es lo que los IDEs (VS Code, PyCharm) muestran como tooltip al
  invocar la clase o el método.
- Los **comentarios** de desarrollador (`# ...`) van en **español**.

## Documentación

- Documentar con **Mermaid** (diagramas de clases, arquitectura, flujos).
- Estándar **UML** para lo propio y lo que se consume de FreeCAD.

## Principios de diseño

- **KISS** — Keep It Simple. Menos es más.
- **SOLID** — Responsabilidad Única, Abierto/Cerrado, Sustitución de Liskov,
  Segregación de Interfaces, Inversión de Dependencias.
- **Arquitectura Document-View** — la misma que usa FreeCAD internamente
  (Documento ↔ Vista ↔ Storage).

## Regla crítica: subcontextos anidados, nunca aplanados

Al armar el diccionario maestro de una carpeta, cada submenú va **como valor
bajo su propia clave**, nunca fusionado con `.update(sub_dict)`:

```python
explorer.update({'file': file})   # CORRECTO — 'file' queda navegable
explorer.update(file)             # INCORRECTO — aplana las hojas del hijo
```

Aplanar rompe dos cosas en silencio: colisiona claves repetidas entre hojas
(`create`, `help`, `center`) quedándose solo con la última, y deja la carpeta
fuera del árbol navegable, con lo cual su `TraduceTo*.py` no se carga nunca.
Detalle completo en `pendientes-dav.md` §4.

## Git / commits

- **No agregar `Co-Authored-By` ni ninguna mención al asistente** en los
  mensajes de commit.
- **No hacer `commit` ni `push`** salvo que el usuario lo pida explícitamente.
- Mensajes de commit en español, descriptivos (ej. `Sketcher: selección de
  plano por voz al crear nuevo boceto`).
- No commitear artefactos generados ni claves/secrets. Los modelos de voz en
  `Dav/models/` están excluidos de git.

---

Siguiente: [Agregar un comando por voz](agregar-comando.md)
