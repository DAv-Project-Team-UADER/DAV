[<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1fa-1f1f8.png" width="18" style="vertical-align: middle;"> English](README.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e6-1f1f7.png" width="18" style="vertical-align: middle;"> Español](README.es.md)
# DAV — Voice-Assisted Design in FreeCAD

**DAV** is an academic project developed as part of a **Territorial Educational Practice (PET)** at the **Universidad Autónoma de Entre Ríos (UADER)**. It is focused on integrating voice commands into the FreeCAD modeling software.

The goal of the project is to enable people with motor disabilities to create and modify 3D models, drawings, and parts through spoken instructions. In doing so, it seeks to reduce exclusive reliance on keyboard and mouse, complementing traditional interaction within the CAD environment and promoting technological accessibility.

DAV works as an assistance layer on top of FreeCAD, integrating through Python and leveraging its native API and architecture. Voice recognition is processed locally using **Vosk**, an open-source ASR (*Automatic Speech Recognition*) engine.

---

## Project Status

DAV is currently in an early **MVP** (*Minimum Viable Product*) stage, focusing on command recognition, FreeCAD integration, and interface development.

## Key Features

- **Accessibility:** Creation and modification of basic geometry through voice commands.
- **Seamless Integration:** Direct communication with the FreeCAD environment.
- **Real-time Feedback:** Visual and textual feedback within the interface.
- **Complementary Use:** Works alongside traditional keyboard and mouse input.

## Technologies Used

- **Primary Language:** Python
- **CAD Environment:** FreeCAD API
- **Voice Recognition:** Vosk
- **Audio Capture:** SoundDevice
- **Graphical Interface:** PySide6
- **Version Control:** Git

## License

This project is distributed under the **GNU GPL v3** license.

It also makes use of third-party technologies and libraries under various open-source licenses, including components associated with FreeCAD, Qt/PySide, and Vosk.
