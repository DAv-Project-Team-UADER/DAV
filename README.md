[<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1fa-1f1f8.png" width="18" style="vertical-align: middle;"> English](README.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e6-1f1f7.png" width="18" style="vertical-align: middle;"> Español](README.es.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e7-1f1f7.png" width="18" style="vertical-align: middle;"> Português](README.pt.md)

# DAV — Voice-Assisted Design

<p align="center">
  <img src="Dav/scr/ComponentesDAV/Logos/color.png" alt="DAV logo" width="200">
</p>

**DAV** is an inclusive development designed to promote the participation of people with motor disabilities in 2D/3D design.

It began as an academic project within a **Territorial Educational Practice (PET)** ([Res. CD-FCYT No. 574-25](Dav/docs/normativas/Res.%20CD-FCYT%20N%C2%BA%20574-25%20-%20%20PET%20-%20DAV%20%28Dise%C3%B1o%20Asistido%20por%20Voz%29....pdf)) at the Faculty of Science and Technology, Concepción del Uruguay campus, of the [**Universidad Autónoma de Entre Ríos (UADER)**](https://uader.edu.ar/). It is focused on integrating voice commands into the [**FreeCAD**](https://www.freecad.org/index.php) modeling software.

The goal of the project is to enable people with motor disabilities to create and modify 3D models, drawings, and parts through spoken instructions. In doing so, it seeks to offer a voice-based alternative that complements the keyboard and mouse within the CAD environment, broadening opportunities for participation and promoting technological accessibility.

DAV works as an assistance layer on top of [**FreeCAD**](https://www.freecad.org/index.php), integrating through Python and leveraging its native API and architecture. Voice recognition is processed locally using [**Vosk**](https://alphacephei.com/vosk/), an open-source ASR (*Automatic Speech Recognition*) engine.

---

## Project Status

DAV is currently in an early **MVP** (*Minimum Viable Product*) stage. It focuses on 2D/3D modeling and does not include all [**FreeCAD**](https://www.freecad.org/index.php) workbenches, but it provides the essential tools a professional needs to use it in daily practice.

## Key Features

- **Accessibility:** Creation and modification of basic geometry through voice commands.
- **Seamless Integration:** Direct communication with the [**FreeCAD**](https://www.freecad.org/index.php) environment.
- **Real-time Feedback:** Visual and textual feedback within the interface.
- **Complementary Use:** Simultaneous compatibility with keyboard and mouse.
- **Multilingual:** Voice recognition available in Spanish, English, and Portuguese.

## Technologies Used

- **Primary Language:** Python
- **CAD Environment:** FreeCAD API
- **Voice Recognition:** Vosk
- **Audio Capture:** SoundDevice
- **Graphical Interface:** PySide6
- **Version Control:** Git

## Minimum system requirements

- **Operating system:** Windows 10 (64-bit) or higher; or any 64-bit Linux distribution (e.g., Ubuntu 20.04)
- **Processor:** 64-bit x86 CPU (Intel Core or AMD Athlon/Ryzen).
- **RAM:** 8 GB minimum
- **Storage:** 2.5 GB of free disk space.
- **Microphone:** required for voice commands; clear speech and a low-noise environment are recommended.

## Documentation

- [User Manual (PDF)](User_Manual.pdf)

## License

This project is distributed under the [**GNU GPL v3**](https://www.gnu.org/licenses/gpl-3.0.html) license.

It also makes use of third-party technologies and libraries under various open-source licenses, including components associated with [**FreeCAD**](https://www.freecad.org/index.php), Qt/PySide, and Vosk.

## Acknowledgements

We would like to extend our special thanks to the [**Faculty of Science and Technology, Concepción del Uruguay campus, of the Autonomous University of Entre Ríos (UADER)**](https://fcytcdelu.uader.edu.ar/), for providing us with the space and resources necessary to carry out this project.

- To the teachers in charge of the project, Eduardo Velazquez and Guillermo Gerard.
- To Jesús Valenzuela and Bernabe Arias, for their collaboration, support, and guidance throughout the process.
- To the communicators Naitria Peralta Montoya and Bruno Contigiani, for their collaboration and contributions to the development and dissemination of the project.
- To [**INTECLAB**](http://fcytcdelu.uader.edu.ar/investigacionlaboratoriointeclab), for their reviews and guidance.

To everyone who, in one way or another, contributed to making this project possible, thank you very much.
