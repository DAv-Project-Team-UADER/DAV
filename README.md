[<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1fa-1f1f8.png" width="18" style="vertical-align: middle;"> English](README.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e6-1f1f7.png" width="18" style="vertical-align: middle;"> Español](README.es.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e7-1f1f7.png" width="18" style="vertical-align: middle;"> Português](README.pt.md)

# DAV — Voice-Assisted Design

**DAV** is an academic project developed as part of a **Territorial Educational Practice (PET)** at the [**Universidad Autónoma de Entre Ríos (UADER)**](https://uader.edu.ar/). It is focused on integrating voice commands into the [**FreeCAD**](https://www.freecad.org/index.php) modeling software.

The goal of the project is to enable people with motor difficulties in their arms (but without speech disorders) to create and modify 3D models, drawings, and parts through spoken instructions. In doing so, it seeks to reduce exclusive reliance on keyboard and mouse, complementing traditional interaction within the CAD environment and promoting technological accessibility.

DAV works as an assistance layer on top of FreeCAD, integrating through Python and leveraging its native API and architecture. Voice recognition is processed locally using **Vosk**, an open-source ASR (*Automatic Speech Recognition*) engine.

---

## Project Status

DAV is currently in an early **MVP** (*Minimum Viable Product*) stage, focusing on 2D/3D modeling. Not all FreeCAD workbenches are available, but it includes the essential tools required for a professional to use it in daily practice.

## Key Features

- **Accessibility:** Creation and modification of basic geometry through voice commands.
- **Seamless Integration:** Direct communication with the FreeCAD environment.
- **Real-time Feedback:** Visual and textual feedback within the interface.
- **Complementary Use:** Simultaneous compatibility with keyboard and mouse.

## Technologies Used

- **Primary Language:** Python
- **CAD Environment:** FreeCAD API
- **Voice Recognition:** Vosk
- **Audio Capture:** SoundDevice
- **Graphical Interface:** PySide6
- **Version Control:** Git

## License: GPLv3

## Documentation

## User Manual

This project is distributed under the **GNU GPL v3** license.

It also makes use of third-party technologies and libraries under various open-source licenses, including components associated with FreeCAD, Qt/PySide, and Vosk.
