# DAV Documentation (English)

**DAV — Voice-Assisted Design** (*Diseño Asistido por Voz*) is a voice-control layer on top of [FreeCAD](https://www.freecad.org/) that uses [Vosk](https://alphacephei.com/vosk/) as its speech recognizer. This folder gathers the **development** documentation, for anyone who wants to understand how the project is built, install it from source or contribute.

> If you only want to use DAV, the end-user material is in the [main README](../../../README.md) (user manual and video tutorials).

This documentation is also available in [Español](../es/README.md) and [Português](../pt/README.md).

---

## Where to start

| If you want to... | Read |
|---|---|
| Understand the project and how work is done on it | [Development guide](dav-development-guide.md) |
| Know what each repository folder contains | [Repository structure](development/structure.md) |
| Run DAV from source | [Setup](development/setup.md) |
| Install DAV | [Windows](windows-installation-guide.md) · [Linux](linux-installation-guide.md) |
| See the classes and how they relate | [Class diagrams](diagrams/README.md) |

## Development

- [Code conventions](development/conventions.md): naming, licence header, docstrings and design principles.
- [Add a voice command](development/add-command.md)
- [Add a submenu](development/add-submenu.md)
- [Add a voice dialog](development/add-prompt.md)
- [How to test and validate](development/testing.md)
- [Port DAV to a new language](port-to-new-language.md)
- [Regenerate the user manual PDF](regenerate-user-manual-pdf.md)
- [GitFlow: the real history of the repository](gitflow-gitgraph.md)

## How voice recognition works

- [Numbers dictionary and grammar](numbers-dictionary-grammar.md)
- [Spoken numbers: limits and proposal](voice-numbers-limits-and-proposal.md)
- [Vosk grammar shortener](vosk-grammar-shortener.md)

## Voice manuals and guides

- [Explorer manual](voice-explorer-manual.md)
- [Voice selection manual](voice-selection-manual.md)
- [Voice sketch and engraving manual](voice-sketch-and-engraving-manual.md)
- [Scissors guide](voice-scissors-guide.md)

## Tests and reports

- [Voice PartDesign testing guide](voice-partdesign-testing-guide.md)
- [Voice 3D testing guide](voice-3d-testing-guide.md)
- [Student number test guide](student-number-test-guide.md)
- [Draft workbench test report](draftwork-test-report.md)

## Status and planning

- [Completed](dav-completed.md): problems already solved and their real cause.
- [GUI unification plan](gui-unification-plan.md)
- [QThread migration plan](qthread-migration-plan.md)
- [Navigable object tree plan](navigable-object-tree-plan.md)

## Institutional and legal documents

- [Regulations](regulations/): the IEEE 830 standard. The Territorial Educational Practice resolution is in the [Spanish folder](../es/normativas/).
- [GPL v3 licence](licenses/)
- [Integration prototypes](prototypes/DOCUMENTACION.md) (archived).

## Other resources in this folder

- [`../assets/`](../assets/): GitFlow chart and examples presentation.
- [`../ejemplo-tijeras/`](../ejemplo-tijeras/): files for the scissors example.
- [`../manual/`](../manual/): scripts that build the PDF manuals.
