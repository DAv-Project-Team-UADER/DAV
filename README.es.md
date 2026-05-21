[🇺🇸 English](README.md) | 🇦🇷 Español
# DAV — Diseño Asistido por Voz en FreeCAD

**DAV** es un proyecto académico desarrollado en el marco de una **Práctica Educativa Territorial (PET)** en la **Universidad Autónoma de Entre Ríos (UADER)**. Está orientado a la integración de comandos de voz en el software de modelado FreeCAD.

El objetivo del proyecto es permitir que personas con dificultades motrices puedan crear y modificar modelos, dibujos y piezas 3D mediante instrucciones habladas. De esta manera, se busca reducir la dependencia exclusiva del teclado y el mouse, complementando la interacción tradicional dentro del entorno CAD y fomentando la accesibilidad tecnológica.

DAV funciona como una capa de asistencia sobre FreeCAD, integrándose mediante Python y aprovechando su API y arquitectura nativas. El reconocimiento de voz se procesa localmente utilizando **Vosk**, un motor ASR (*Automatic Speech Recognition*) de código abierto.

---

## Estado del proyecto

DAV se encuentra actualmente en una etapa temprana de **MVP** (*Minimum Viable Product*), enfocándose en el reconocimiento de comandos, la integración con FreeCAD y el desarrollo de la interfaz.

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

## Licencia

Este proyecto se distribuye bajo la licencia **GNU GPL v3**. 

Además, utiliza tecnologías y bibliotecas de terceros bajo distintas licencias open source, incluyendo componentes asociados a FreeCAD, Qt/PySide y Vosk.