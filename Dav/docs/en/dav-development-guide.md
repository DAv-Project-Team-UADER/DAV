# DAV Development Guide

> **DAV — Voice-Assisted Design (Diseño Asistido por Voz)**
> Territorial Educational Practice — Faculty of Science and Technology (FCyT) — UADER

This guide explains **how the DAV project is developed and contributed to**: how
to get it running, which conventions to follow, how to add a voice command and
how to test your changes. It is intended for team members who join the
development, both for DAV's own code and for the voice command
dictionary.

It is written from what was learned in practice. If something becomes outdated or
you change a convention, **update this guide** in the same PR that touches the
code.

---

## Index

| Section | Contents |
|---|---|
| [Repository structure](development/structure.md) | What each repo folder does and where everything lives |
| [Getting started (setup)](development/setup.md) | How to clone, install dependencies, models and run DAV in FreeCAD |
| [Code conventions](development/conventions.md) | Names, mandatory header, docstrings, design principles |
| [Adding a voice command](development/add-command.md) | Step by step with a real example, from the dictionary to the TraduceTo |
| [Adding a submenu](development/add-submenu.md) | A new folder: nested without flattening, the three `TraduceTo*` files, icons by key name |
| [Adding a voice dialog](development/add-prompt.md) | Existing and new prompts, and how to restrict the Vosk grammar |
| [How to test and validate](development/testing.md) | Manual tests, `freecadcmd` and Qt offscreen without opening the GUI, and links to the existing guides |

---

## Quick summary

- **DAV** is a **voice** control layer on top of **FreeCAD** using **Vosk**
  as the recognizer.
- The code of our own lives in `Dav/`; the voice command tree in `Dav/dic/`;
  the engine that walks that tree is `Browser`
  (`Dav/scr/.../navigation/browser.py`).
- Spoken phrases are defined in the `TraduceToEs.py` / `TraduceToEn.py` /
  `TraduceToPT.py` of each folder; each folder's master dictionary
  links the internal keys with FreeCAD callables.
- Golden rule: **subcontexts go nested under their own key**, never
  flattened with `.update(sub_dict)`. See [pendientes-dav.md](pendientes-dav.md) §4.

---

## Reference material

- **[CLAUDE.md](../../CLAUDE.md)** — general project documentation:
  architecture, GitFlow, voice model, licenses. It is the source of most
  of the conventions cited here.
- **[pendientes-dav.md](pendientes-dav.md)** — what is still open. **Read
  before touching dictionaries or navigation.**
- **[dav-completed.md](dav-completed.md)** — problems already solved and their
  real cause. Check before re-diagnosing something known.
- `README.md` / `README.es.md` / `README.pt.md` — project overview.
