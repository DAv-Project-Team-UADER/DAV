# DAV — Guia de instalação

**DAV (Design Assistido por Voz)** é um programa que permite controlar o **FreeCAD** com a
voz. Em vez de clicar, você diz comandos como _"vista frontal"_ ou _"crear boceto"_ e o DAV
os executa para você.

O DAV não é um programa separado: **roda dentro do FreeCAD**, como mais um módulo. Por isso
primeiro se instala o FreeCAD, e depois se adiciona o DAV.

---

## Escolha o seu caminho

Há duas formas de instalar o DAV, conforme o que você quiser fazer:

| Se você quer…                                             | Siga este caminho                                                          |
| --------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Apenas usar o DAV** sem mexer no código (Windows)       | [Caminho A → usuário final](#caminho-a--usuário-final-windows)             |
| **Trabalhar com o código** do projeto (Windows ou Linux)  | [Caminho B → desenvolvedores](#caminho-b--desenvolvedores-windows-e-linux) |

---

## O que você precisa em qualquer um dos dois caminhos

| Você precisa de  | Para quê                                                                                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FreeCAD 1.x**  | É o programa que o DAV controla. É **gratuito** e está em <https://www.freecad.org/downloads.php>. O DAV **não o inclui**: é preciso instalá-lo antes.                 |
| **Microfone**    | Para usar os comandos de voz.                                                                                                                                         |
| **Internet**     | Somente na primeira vez: o DAV baixa o modelo de voz Vosk (≈ 40 MB).                                                                                                  |
| **Python 3.10+** | Somente na primeira vez: o DAV o usa para criar seu ambiente de voz. Se você não o tem, instale-o em <https://www.python.org/downloads/> marcando **"Add Python to PATH"**. |

> **Não é preciso** baixar mais nada: nem o código do FreeCAD, nem modelos de voz, nem
> editores. O DAV cuida de tudo isso sozinho, na primeira vez.

---

## Caminho A — Usuário final (Windows)

Para quem **só quer usar o DAV**, sem abrir o código. É um único arquivo com duplo clique.

### Passo 1 — Instale o FreeCAD

1. Acesse <https://www.freecad.org/downloads.php>.
2. Baixe e instale a versão **1.x** (Windows, 64 bits).
3. **IMPORTANTE:** o DAV não traz o FreeCAD dentro. Sem o FreeCAD instalado, o DAV não pode ser aberto.

### Passo 2 — Baixe o instalador do DAV

Baixe o arquivo **`DAV_Installer_1.0.exe`**.

### Passo 3 — Execute o instalador

Dê **duplo clique** em `DAV_Installer_1.0.exe`.

**O Windows diz "O Windows protegeu o seu computador"?**
O instalador ainda não está assinado digitalmente (é normal). Para que ele rode:

1. Clique em **"Mais informações"**.
2. Depois em **"Executar assim mesmo"**.

### Passo 4 — Deixe-o trabalhar (quase sozinho)

Aparece uma **janela preta** (o console) que vai mostrando em verde os passos que cumpre:

1. Copia o DAV para a sua pasta de usuário.
2. Cria o ambiente de voz (instala o que faltava).
3. Baixa o modelo de voz **em espanhol**.
4. **Abre o FreeCAD** com o painel do DAV ativo.

> A **primeira vez pode demorar entre 5 e 15 minutos**: é o download dos modelos e das
> dependências. Não feche a janela preta. Nas vezes seguintes é quase instantâneo.

### Passo 5 — Hora de usar o DAV!

Quando o FreeCAD abrir, você verá o **painel do DAV** (com o botão do microfone).

Experimente falar: **"vista frontal"**. A vista deve mudar. É só isso — você já está usando o DAV.

### Para abrir o DAV novamente depois

Dê duplo clique em: **`%USERPROFILE%\DAV\iniciar_dav.bat`**
(ou execute o instalador de novo: ele percebe que já está tudo pronto e só abre o FreeCAD).

---

## Caminho B — Desenvolvedores (Windows e Linux)

Para **colegas da equipe** que querem trabalhar com o código do DAV e modificá-lo.

### Windows — instalação a partir do repositório

#### 1. Instale os pré-requisitos

- **Git** → <https://git-scm.com/downloads>
- **FreeCAD 1.x** → <https://www.freecad.org/downloads.php>
- **Python 3.10+** → <https://www.python.org/downloads/> (marque **"Add Python to PATH"**)

#### 2. Clone o repositório

```bat
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
cd DAV
```

#### 3. Abra o launcher

Dê **duplo clique** em **`iniciar_dav.bat`** (ou execute-o pelo terminal).

O launcher faz o mesmo que o instalador do Caminho A, mas usando a sua cópia do código:

1. Detecta o Python do sistema e cria o ambiente virtual local.
2. Instala as dependências de voz (`PySide6`, `Vosk`, `sounddevice`, …).
3. Baixa os modelos de voz se faltarem.
4. Encontra o seu `FreeCAD.exe` e vincula o workbench DAV dentro do FreeCAD.
5. Abre o FreeCAD com o seu código carregado.

#### Opções úteis do launcher

Se precisar de mais controle, converta-o no terminal:

```powershell
# Probar con un FreeCAD específico
.\iniciar_dav.ps1 -FreeCADExe "C:\ruta\bin\FreeCAD.exe"

# Solo preparar el entorno, sin abrir FreeCAD
.\iniciar_dav.ps1 -InstallOnly

# Controlar la voz al arrancar
.\iniciar_dav.ps1 -StartVoice
.\iniciar_dav.ps1 -NoStartVoice
```

### Linux — instalação a partir do repositório

1. Baixe a AppImage do FreeCAD **1.1.3** para `~/Descargas/`.
2. Clone o repositório:

   ```bash
   git clone https://github.com/DAv-Project-Team-UADER/DAV.git
   cd DAV
   ```

3. Execute o launcher do Linux:

   ```bash
   chmod +x iniciar_dav.sh
   ./iniciar_dav.sh
   ```

O script cria o link do workbench DAV em
`~/.local/share/FreeCAD/v1-1/Mod/DAV` e abre o FreeCAD.

> Explicação passo a passo e solução de problemas do Linux: veja
> **`Dav/docs/es/README-linux.md`**.

---

## Problemas frequentes (ambos os caminhos)

| Problema                              | Solução                                                                                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| O Windows diz "protegeu o seu computador" | Clique em **"Mais informações"** → **"Executar assim mesmo"** (é porque o instalador ainda não está assinado).       |
| Diz "No se encontró FreeCAD.exe"      | O FreeCAD não está instalado (ou está em outro caminho). Instale-o, ou passe o caminho com `-FreeCADExe` (Caminho B).    |
| Diz "No se encontró Python 3"         | Instale o Python 3.10+ marcando **"Add Python to PATH"**.                                                                |
| Na primeira vez demora muito          | É normal: baixa os modelos de voz. Não feche a janela.                                                                   |
| O microfone não responde no FreeCAD   | Faltam bibliotecas de voz no Python do FreeCAD. Rode `iniciar_dav.bat` de novo e deixe-o reinstalar as dependências.     |

---

## Documentação relacionada

| Tema                                                                                                      | Onde está                                           |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Guia detalhado do Linux                                                                                   | `Dav/docs/es/README-linux.md`                          |
| **Documentação técnica do instalador** (como o `.exe` foi gerado, como funciona e como regenerá-lo)      | `Dav/scr/ComponentesDAV/scripts/iexpress/README.md` |
