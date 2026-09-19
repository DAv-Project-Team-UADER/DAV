[<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1fa-1f1f8.png" width="18" style="vertical-align: middle;"> English](README.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e6-1f1f7.png" width="18" style="vertical-align: middle;"> Español](README.es.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e7-1f1f7.png" width="18" style="vertical-align: middle;"> Português](README.pt.md)
# DAV — Diseño Asistido por Voz

**DAV** es un proyecto académico desarrollado en el marco de una **Práctica Educativa Territorial (PET)** de la [**Universidad Autónoma de Entre Ríos (UADER)**](https://uader.edu.ar/). Está orientado a la integración de comandos de voz en el software de modelado [**FreeCAD**](https://www.freecad.org/index.php).

El objetivo del proyecto es permitir que personas con dificultades motrices en brazos pero sin reastornos del habla puedan crear y modificar modelos, dibujos y piezas 3D mediante comandos de voz. De esta manera, se busca reducir la dependencia exclusiva del teclado y el mouse, complementando la interacción tradicional dentro del entorno CAD y fomentando la accesibilidad tecnológica.

DAV funciona como una capa de asistencia sobre FreeCAD, integrándose mediante Python y aprovechando  arquitectura nativa. El reconocimiento de voz se procesa localmente utilizando [**Vosk**](https://alphacephei.com/vosk/), un motor ASR (*Automatic Speech Recognition*) de código abierto.

---

## Estado del proyecto

DAV se encuentra actualmente en una etapa temprana de **MVP** (*Minimum Viable Product*), enfocándose en el modelado en 2D/3D,por lo que no todas las herrramientas (WorkBenchs) de FreeCAD, más si posee las herramientas indispensable para que un profesional pueda utilizarlo en su práctica cotidiana.

## Características Principales

- **Accesibilidad:** Creación y modificación de geometría básica mediante comandos de voz.
- **Integración fluida:** Comunicación directa con el entorno de FreeCAD.
- **Feedback en tiempo real:** Retroalimentación visual y textual en la interfaz.
- **Uso complementario:** Compatibilidad simultánea con el uso de teclado y mouse.

## Tecnologías Utilizadas

- **Lenguaje principal:** Python
- **Entorno CAD:** FreeCAD API
- **Reconocimiento de Voz:** Vosk
- **Captura de Audio:** SoundDevice
- **Interfaz Gráfica:** PySide6
- **Control de Versiones:** Git

## Requerimientos mínimos del sistema 

- **Sistema operativo:** Windows 10 (64-bit) o superior; o cualquier distribución linux de 64 bits (por ejemplo: Ubuntu 20.04)
-**Procesador**: CPU x86 de 64 bits (Intel Core o AMD Athlon/Ryzen).
-**Memoria RAM**: 8 GB mínimo 
-**Almacenamiento:** 2.5 GB de espacio libre en disco.

## Manual de Usuario

- [Manual de Usuario (PDF)](Manual_Usuario.pdf)
- [VideoTutoriales (Youtube)](https://www.youtube.com/watch?v=DwHS8yIz_Mw&list=PLNZ1JD1zPONA&pp=sAgC)

## Licencia

Este proyecto se distribuye bajo la licencia **GNU GPL v3**. 

Además, utiliza tecnologías y bibliotecas de terceros bajo distintas licencias open source, incluyendo componentes asociados a FreeCAD, Qt/PySide y Vosk.
## Agradecimientos
Queremos agradecer especialmente a la Universidad Autónoma de Entre Ríos (UADER) por brindarnos el espacio y los recursos necesarios para llevar adelante este proyecto; a los profesores Jesús Valenzuela y Bernabe Arias, por su acompañamiento, orientación y disposición durante el
proceso; y a los comunicadores Naitria Peralta Montoya y Bruno Contigiani, por su colaboración y aportes en el desarrollo y difusión del proyecto.

A todas las personas que, de una u otra manera, contribuyeron a que este proyecto fuera posible,
muchas gracias.
