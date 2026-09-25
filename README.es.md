[<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1fa-1f1f8.png" width="18" style="vertical-align: middle;"> English](README.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e6-1f1f7.png" width="18" style="vertical-align: middle;"> Español](README.es.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e7-1f1f7.png" width="18" style="vertical-align: middle;"> Português](README.pt.md)
# DAV — Diseño Asistido por Voz

<p align="center">
  <img src="Dav/scr/ComponentesDAV/Logos/color.png" alt="Logo de DAV" width="200">
</p>

**DAV** es un desarrollo inclusivo pensado para promover la participación de personas con discapacidad motriz en el diseño 2D/3D.

Nació como un proyecto académico en el marco de una **Práctica Educativa Territorial (PET)** ([Res. CD-FCYT N° 574-25](Dav/docs/normativas/Res.%20CD-FCYT%20N%C2%BA%20574-25%20-%20%20PET%20-%20DAV%20%28Dise%C3%B1o%20Asistido%20por%20Voz%29....pdf)) de la Facultad de Ciencia y Tecnología, sede Concepción del Uruguay, de la [**Universidad Autónoma de Entre Ríos (UADER)**](https://uader.edu.ar/). Está orientado a la integración de comandos de voz en el software de modelado [**FreeCAD**](https://www.freecad.org/index.php).

El objetivo del proyecto es permitir que personas con discapacidad motriz puedan crear y modificar modelos, dibujos y piezas 3D mediante comandos de voz. De esta manera, se busca ofrecer una alternativa de interacción por voz que complemente el teclado y el mouse dentro del entorno CAD, ampliando las posibilidades de participación y fomentando la accesibilidad tecnológica.

DAV funciona como una capa de asistencia sobre [**FreeCAD**](https://www.freecad.org/index.php), integrándose mediante Python y aprovechando su API y su arquitectura nativa. El reconocimiento de voz se procesa localmente utilizando [**Vosk**](https://alphacephei.com/vosk/), un motor ASR (*Automatic Speech Recognition*) de código abierto.

---

## Estado del proyecto

DAV se encuentra actualmente en una etapa temprana de **MVP** (*Minimum Viable Product*, Producto Mínimo Viable). Se enfoca en el modelado 2D/3D y no incluye todos los entornos de trabajo (*Workbenches*) de [**FreeCAD**](https://www.freecad.org/index.php), pero cuenta con las herramientas indispensables para que un profesional pueda utilizarlo en su práctica cotidiana.

## Características Principales

- **Accesibilidad:** Creación y modificación de geometría básica mediante comandos de voz.
- **Integración fluida:** Comunicación directa con el entorno de [**FreeCAD**](https://www.freecad.org/index.php).
- **Feedback en tiempo real:** Retroalimentación visual y textual en la interfaz.
- **Uso complementario:** Compatibilidad simultánea con el uso de teclado y mouse.
- **Multilingüe:** Reconocimiento de voz disponible en español, inglés y portugués.

## Tecnologías Utilizadas

- **Lenguaje principal:** Python
- **Entorno CAD:** FreeCAD API
- **Reconocimiento de Voz:** Vosk
- **Captura de Audio:** SoundDevice
- **Interfaz Gráfica:** PySide6
- **Control de Versiones:** Git

## Requerimientos mínimos del sistema 

- **Sistema operativo:** Windows 10 (64-bit) o superior; o cualquier distribución linux de 64 bits (por ejemplo: Ubuntu 20.04)
- **Procesador**: CPU x86 de 64 bits (Intel Core o AMD Athlon/Ryzen).
- **Memoria RAM**: 8 GB mínimo 
- **Almacenamiento:** 2.5 GB de espacio libre en disco.
- **Micrófono:** necesario para los comandos de voz; se recomienda una dicción clara y un ambiente con poco ruido.

## Manual de Usuario

- [Manual de Usuario (PDF)](Manual_Usuario.pdf)
- [VideoTutoriales (Youtube)](https://www.youtube.com/watch?v=DwHS8yIz_Mw&list=PLNZ1JD1zPONA&pp=sAgC)

## Licencia

Este proyecto se distribuye bajo la licencia [**GNU GPL v3**](https://www.gnu.org/licenses/gpl-3.0.html). 

Además, utiliza tecnologías y bibliotecas de terceros bajo distintas licencias open source, incluyendo componentes asociados a [**FreeCAD**](https://www.freecad.org/index.php), Qt/PySide y Vosk.

## Agradecimientos

Queremos agradecer especialmente a la [**Facultad de Ciencia y Tecnología, sede Concepción del Uruguay, de la Universidad Autónoma de Entre Ríos (UADER)**](https://fcytcdelu.uader.edu.ar/), por brindarnos el espacio y los recursos necesarios para llevar adelante este proyecto.

- A los docentes a cargo del proyecto, Eduardo Velazquez y Guillermo Gerard.
- A Jesús Valenzuela y Bernabe Arias, por su colaboración, acompañamiento y orientación durante el proceso.
- A los comunicadores Naitria Peralta Montoya y Bruno Contigiani, por su colaboración y aportes en el desarrollo y la difusión del proyecto.
- Al [**INTECLAB**](http://fcytcdelu.uader.edu.ar/investigacionlaboratoriointeclab), por sus revisiones y orientación.

A todas las personas que, de una u otra manera, contribuyeron a que este proyecto fuera posible, muchas gracias.
