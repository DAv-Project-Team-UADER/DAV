# Code conventions

These are the DAV project conventions. They apply to **all of our own code**
(the code that lives in `Dav/`). The pre-existing FreeCAD files keep their
own rules (and their original header).

> Main source: the repo's `CLAUDE.md`.

## Naming

| Type | Convention | Example |
|---|---|---|
| Classes | `PascalCase` | `DavAgent`, `VoskModel` |
| Attributes / Properties | `PascalCase` | `LineColor`, `ShapeColor` |
| Functions / Methods | `camelCase` (lowercase initial) | `addObject()`, `recompute()` |
| Internal use | `_leadingUnderscore` | `_internalMethod` |

## File organization

- **One class = one file**
- **One dictionary = one file**
- The file name equals the class name (`DavAgent.py`)

## Mandatory header (all of our own files)

Every DAV file of our own must start with this license header (it is copied
verbatim, in Spanish, as the project's official text):

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

> The pre-existing FreeCAD files **keep their original header**
> (LGPL-2.1-or-later). Do not replace it.

## Docstrings

- Every **class and public method** must have a docstring in **English**.
- Format: short first line (summary), blank line, then `Args:`, `Returns:`,
  `Example::` sections as appropriate.
- The docstring is what IDEs (VS Code, PyCharm) show as a tooltip when
  calling the class or method.
- Developer **comments** (`# ...`) are written in **Spanish**.

## Documentation

- Document with **Mermaid** (class diagrams, architecture, flows).
- **UML** standard for our own code and for what is consumed from FreeCAD.

## Design principles

- **KISS** — Keep It Simple. Less is more.
- **SOLID** — Single Responsibility, Open/Closed, Liskov Substitution,
  Interface Segregation, Dependency Inversion.
- **Document-View architecture** — the same one FreeCAD uses internally
  (Document ↔ View ↔ Storage).

## Critical rule: nested subcontexts, never flattened

When building a folder's master dictionary, each submenu goes **as a value
under its own key**, never merged with `.update(sub_dict)`:

```python
explorer.update({'file': file})   # CORRECT — 'file' stays navigable
explorer.update(file)             # WRONG — flattens the child's leaves
```

Flattening silently breaks two things: it collides keys repeated between leaves
(`create`, `help`, `center`), keeping only the last one, and it leaves the folder
out of the navigable tree, so its `TraduceTo*.py` is never loaded.
Full details in `pendientes-dav.md` §4.

## Git / commits

- **Do not add `Co-Authored-By` or any mention of the assistant** in commit
  messages.
- **Do not `commit` or `push`** unless the user explicitly asks for it.
- Commit messages in Spanish, descriptive (e.g. `Sketcher: selección de
  plano por voz al crear nuevo boceto`).
- Do not commit generated artifacts or keys/secrets. The voice models in
  `Dav/models/` are excluded from git.

---

Next: [Adding a voice command](add-command.md)
