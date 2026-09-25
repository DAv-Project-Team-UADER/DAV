[<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1fa-1f1f8.png" width="18" style="vertical-align: middle;"> English](README.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e6-1f1f7.png" width="18" style="vertical-align: middle;"> Español](README.es.md) | [<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f1e7-1f1f7.png" width="18" style="vertical-align: middle;"> Português](README.pt.md)

# DAV — Desenho Assistido pela Voz

<p align="center">
  <img src="Dav/scr/ComponentesDAV/Logos/color.png" alt="Logo do DAV" width="200">
</p>

**DAV** é um desenvolvimento inclusivo pensado para promover a participação de pessoas com deficiência motora no desenho 2D/3D.

Nasceu como um projeto acadêmico no contexto de uma **Prática Educativa Territorial (PET)** ([Res. CD-FCYT N° 574-25](Dav/docs/normativas/Res.%20CD-FCYT%20N%C2%BA%20574-25%20-%20%20PET%20-%20DAV%20%28Dise%C3%B1o%20Asistido%20por%20Voz%29....pdf)) da Faculdade de Ciência e Tecnologia, sede Concepción del Uruguay, da [**Universidad Autónoma de Entre Ríos (UADER)**](https://uader.edu.ar/). O projeto é voltado para a integração de comandos de voz no software de modelagem [**FreeCAD**](https://www.freecad.org/index.php).

O objetivo do projeto é permitir que pessoas com deficiência motora possam criar e modificar modelos, desenhos e peças 3D usando comandos de voz. Dessa forma, busca-se oferecer uma alternativa de interação por voz que complemente o teclado e o mouse dentro do ambiente CAD, ampliando as possibilidades de participação e promovendo a acessibilidade tecnológica.

O DAV funciona como uma camada de assistência sobre o [**FreeCAD**](https://www.freecad.org/index.php), integrando-se através de Python e aproveitando sua API e sua arquitetura nativa. O reconhecimento de voz é processado localmente utilizando [**Vosk**](https://alphacephei.com/vosk/), um motor ASR (*Automatic Speech Recognition*) de código aberto.

---

## Estado do projeto

O DAV está atualmente em uma fase inicial de **MVP** (*Minimum Viable Product*, Produto Mínimo Viável). Ele se concentra na modelagem 2D/3D e não inclui todos os ambientes de trabalho (*Workbenches*) do [**FreeCAD**](https://www.freecad.org/index.php), mas já conta com as ferramentas essenciais para que um profissional possa utilizá-lo no dia a dia.

## Principais Características

- **Acessibilidade:** Criação e modificação de geometria básica através de comandos de voz.
- **Integração fluida:** Comunicação direta com o ambiente do [**FreeCAD**](https://www.freecad.org/index.php).
- **Feedback em tempo real:** Retorno visual e textual na interface.
- **Uso complementar:** Compatibilidade simultânea com teclado e mouse.
- **Multilíngue:** Reconhecimento de voz disponível em espanhol, inglês e português.

## Tecnologias Utilizadas

- **Linguagem principal:** Python
- **Ambiente CAD:** API do FreeCAD
- **Reconhecimento de Voz:** Vosk
- **Captura de Áudio:** SoundDevice
- **Interface Gráfica:** PySide6
- **Controle de Versão:** Git

## Requisitos mínimos do sistema

- **Sistema operacional:** Windows 10 (64-bit) ou superior; ou qualquer distribuição Linux de 64 bits (por exemplo: Ubuntu 20.04)
- **Processador:** CPU x86 de 64 bits (Intel Core ou AMD Athlon/Ryzen).
- **Memória RAM:** 8 GB ou mais
- **Armazenamento:** 2,5 GB de espaço livre em disco.
- **Microfone:** necessário para os comandos de voz; recomenda-se dicção clara e um ambiente com pouco ruído.

## Manual do Usuário

- [Manual do Usuário (PDF)](Manual_do_Usuario.pdf)

## Licença

Este projeto é distribuído sob a licença [**GNU GPL v3**](https://www.gnu.org/licenses/gpl-3.0.html).

Além disso, utiliza tecnologias e bibliotecas de terceiros sob diferentes licenças open source, incluindo componentes relacionados ao [**FreeCAD**](https://www.freecad.org/index.php), Qt/PySide e Vosk.

## Agradecimentos

Queremos agradecer especialmente à [**Faculdade de Ciência e Tecnologia, sede Concepción del Uruguay, da Universidad Autónoma de Entre Ríos (UADER)**](https://fcytcdelu.uader.edu.ar/), por nos oferecer o espaço e os recursos necessários para levar adiante este projeto.

- Aos docentes responsáveis pelo projeto, Eduardo Velazquez e Guillermo Gerard.
- A Jesús Valenzuela e Bernabe Arias, pela colaboração, acompanhamento e orientação durante o processo.
- Aos comunicadores Naitria Peralta Montoya e Bruno Contigiani, pela colaboração e contribuições no desenvolvimento e na divulgação do projeto.
- Ao [**INTECLAB**](http://fcytcdelu.uader.edu.ar/investigacionlaboratoriointeclab), pelas revisões e orientação.

A todas as pessoas que, de uma forma ou de outra, contribuíram para tornar este projeto possível, muito obrigado.
