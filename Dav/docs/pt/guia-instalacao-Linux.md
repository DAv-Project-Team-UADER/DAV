# DAV — Guia de instalação (Linux)

**DAV (Design Assistido por Voz)** é um programa que permite controlar o **FreeCAD** com a voz. Em vez de clicar, você diz comandos como _"vista frontal"_ ou _"crear boceto"_ e o DAV os executa para você.

O DAV não é um programa separado: **roda dentro do FreeCAD**, como mais um módulo. Por isso primeiro se instala o FreeCAD, e depois se adiciona o DAV.

---

## Escolha o seu caminho

Há duas formas de instalar o DAV no Linux, conforme o que você precisa fazer:

| Se você quer… | Siga este caminho |
| :--- | :--- |
| **Apenas usar o DAV** sem mexer no código | [Caminho A → Usuário final](#caminho-a--usuário-final) |
| **Trabalhar com o código** do projeto | [Caminho B → Desenvolvedores](#caminho-b--desenvolvedores) |

---

## O que você precisa em qualquer um dos dois caminhos

| Você precisa de | Para quê |
| :--- | :--- |
| **FreeCAD 1.1.4 (AppImage)** | É o programa base. [Baixe o AppImage](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage) e guarde-o na sua pasta de **Descargas** (ou **Downloads**). |
| **Microfone** | Para usar os comandos de voz. |
| **Conexão com a Internet** | **Obrigatória durante a instalação** (na primeira vez): são instalados pacotes do sistema e dependências do Python, e é baixado o modelo de voz Vosk (≈ 40 MB). |
| **Senha de administrador (sudo)** | Na primeira vez, o instalador a pede **uma única vez** para instalar pacotes do sistema (áudio, FUSE) e conceder permissões de microfone. Ao digitá-la nada aparece na tela: é normal. |
| **Python 3.10+** | Geralmente já vem instalado por padrão nas distribuições Linux modernas (Ubuntu, Mint, Fedora). Para criar o ambiente do DAV também é necessário o pacote `python3-venv` (`sudo apt install python3 python3-venv python3-pip`). |

> **Importante:** sem conexão com a Internet a instalação falha. Depois de instalado, o DAV funciona offline.

> **Não é preciso** baixar modelos de voz manualmente. O DAV cuida de tudo isso automaticamente na primeira vez que você o abre.

---

## Caminho A — Usuário final

Para quem **só quer usar o DAV**, sem abrir o código nem usar o terminal. É um único arquivo executável.

### Passo 1 — Baixe o FreeCAD
1. [Baixe o FreeCAD 1.1.4 (AppImage para Linux)](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage).
2. Se preferir outra versão, todas estão em <https://www.freecad.org/downloads.php> (use sempre a série **1.x** no formato `.AppImage`).
3. Salve o arquivo exatamente na sua pasta pessoal de **Descargas** (ou **Downloads** se o seu sistema estiver em inglês ou português).
4. **IMPORTANTE:** Sem o AppImage do FreeCAD baixado, o DAV não pode ser aberto.

### Passo 2 — Baixe o instalador do DAV
Baixe o arquivo **`DAV_Installer_1.0-Linux`**.

### Passo 3 — Dê permissões de execução
Por segurança, o Linux não executa arquivos baixados da internet com duplo clique de imediato. É preciso autorizar:
1. Faça **clique direito** em `DAV_Installer_1.0-Linux`.
2. Selecione **Propriedades**.
3. Vá à aba **Permissões**.
4. Marque a caixa **"Permitir executar o arquivo como programa"** (ou similar).
5. Feche a janela.

### Passo 4 — Execute o instalador
Dê **duplo clique** em `DAV_Installer_1.0-Linux` e selecione **Executar**.
*(Se o duplo clique não funcionar no seu ambiente, você pode abrir o terminal nessa pasta e digitar `./DAV_Installer_1.0-Linux`).*

O programa fará o seguinte de forma automática:
1. Copia os arquivos do DAV para a sua pasta de módulos do FreeCAD (`~/.local/share/FreeCAD/v1-1/Mod/`).
2. Instala as dependências de voz e baixa o modelo em espanhol.
3. **Abre o FreeCAD** com o painel do DAV integrado.

> **Nota:** Na primeira vez pode demorar alguns minutos por causa do download do modelo de voz.

### Passo 5 — Hora de usar o DAV!
Quando o FreeCAD abrir, você verá o **painel do DAV** com o botão do microfone. Diga **"vista frontal"** para testar. 

Para abri-lo novamente no futuro, basta executar de novo o arquivo `DAV_Installer_1.0-Linux` (ele detectará que já está instalado e abrirá o FreeCAD diretamente).

---

## Caminho B — Desenvolvedores

Para **colegas da equipe** que precisam acessar o código-fonte, modificá-lo e testar as mudanças em tempo real.

### 1. Instale os pré-requisitos
* Certifique-se de ter o **Git** instalado (`sudo apt install git`).
* Ter o **Python 3.10+** com venv e pip: `sudo apt install python3 python3-venv python3-pip`.
* [Baixe o **AppImage do FreeCAD 1.1.4**](https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage) e deixe-o na sua pasta `~/Descargas/`.

### 2. Clone o repositório
Abra um terminal e execute:
```bash
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
cd DAV
```

### 3. Execute o instalador
Dentro da pasta do projeto que você acabou de clonar, execute o instalador:
```bash
chmod +x LinuxInstaller.sh iniciar_dav.sh
./LinuxInstaller.sh
```

O instalador prepara tudo de forma automática. **Ele pede a senha de administrador (`sudo`) uma única vez**, porque alguns passos instalam pacotes do sistema e concedem permissões de áudio:
1. Cria o ambiente virtual (`GUIFreeCad/.venv`) e instala as dependências de voz (`PySide6`, `Vosk`, `sounddevice`, …).
2. Baixa os modelos de voz Vosk em `Dav/models/` (se já estiverem lá, não os baixa de novo).
3. Cria um link simbólico do seu código-fonte para `~/.local/share/FreeCAD/v1-1/Mod/DAV`.
4. Cria os atalhos: `ejecutar.desktop` na pasta do projeto, uma entrada **DAV** no menu de aplicativos e `DAV_V1.desktop` na Área de Trabalho (se ainda não existir).
5. Instala os pacotes de áudio do sistema (PortAudio, ALSA) e, se faltar, a `libfuse2`, que o AppImage do FreeCAD precisa para abrir.
6. Instala as dependências de voz (`sounddevice`, `vosk`) também para o Python do FreeCAD, em `GUIFreeCad/.freecad_deps`.
7. Adiciona o seu usuário ao grupo `audio`, para poder usar o microfone. Se o adicionar, **encerre a sessão e entre de novo uma vez** para que tenha efeito.
8. Verifica o seu computador e avisa, sem interromper a instalação, se não há microfone, se não há um padrão ou se a CPU não oferece AVX (o Vosk precisa dele).

### 4. Abra o DAV
Dê duplo clique no atalho **DAV** (ou execute `./iniciar_dav.sh` no terminal). O script procura a AppImage do FreeCAD na sua pasta de Descargas, utilizando um caminho universal (`$HOME`), e lança o FreeCAD com o seu código carregado. Qualquer mudança que você salvar no código Python será refletida ao reiniciar o FreeCAD.

Opções úteis do `iniciar_dav.sh`:
```bash
./iniciar_dav.sh /caminho/para/FreeCAD.AppImage   # usar um FreeCAD específico
./iniciar_dav.sh --install-only                   # só preparar o ambiente, sem abrir o FreeCAD
./iniciar_dav.sh --skip-models                    # não baixar os modelos de voz
```

---

## Problemas frequentes

| Problema | Solução |
| :--- | :--- |
| **"Permissão negada" ao dar duplo clique** | Faltou o Passo 3 do Caminho A. Clique direito no arquivo > Propriedades > Permissões > Permitir executar como programa. |
| **"FreeCAD não encontrado"** | Verifique que o arquivo do FreeCAD termine em `.AppImage` e esteja diretamente na pasta `Descargas` (ou `Downloads`). |
| **"Não foi possível criar GUIFreeCad/.venv"** | Falta o pacote de ambientes virtuais. Execute `sudo apt install python3-venv python3-pip` e rode o instalador de novo. |
| **O microfone não responde / Erro do Vosk** | Execute `./iniciar_dav.sh` no terminal e leia os avisos da verificação do microfone. Se o instalador o adicionou ao grupo `audio`, encerre a sessão e entre de novo. Se ainda assim falhar, instale manualmente: `sudo apt install libportaudio2 portaudio19-dev python3-pyaudio`. |
| **"Nenhum microfone foi detectado"** | O DAV abre mas não consegue ouvir. Em uma **máquina virtual** é preciso habilitar a entrada de áudio: no VMware, a placa de som (*Sound Card*) da VM conectada e o microfone do computador hospedeiro disponível; no VirtualBox, *Configurações > Áudio > Habilitar entrada de áudio*. Em um PC, conecte um microfone e selecione-o como entrada nas configurações de som (`pavucontrol`). |
| **"A CPU não oferece AVX" / `Illegal instruction`** | O Vosk usa instruções AVX. Em uma máquina virtual, use uma versão de hardware recente e ative a virtualização de CPU (você pode verificar com `grep -w avx /proc/cpuinfo`). O DAV continua aberto e mostra o erro no Relatório do FreeCAD; sem AVX o reconhecimento de voz não pode funcionar. |
| **O FreeCAD não abre ou nada acontece ao iniciá-lo (FUSE)** | O AppImage precisa da `libfuse2`. O instalador tenta instalá-la; se não conseguir, o DAV executa o AppImage sem FUSE (demora mais para abrir). Manualmente: `sudo apt install libfuse2` (no Ubuntu 24.04 chama-se `libfuse2t64`). |
| **Na primeira vez demora muito** | É normal, está baixando o modelo de voz em segundo plano. |

## Se algo falhar: o que verificar e o que enviar

O DAV guarda registros em `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/config/`:

| Arquivo | O que contém |
| :--- | :--- |
| `dav.log` | O que o DAV faz: início da voz, erros e avisos. É a primeira coisa a olhar. |
| `dav_fault.log` | É criado se o FreeCAD fechar de repente por uma falha nativa; registra em que ponto do código estava. |

No Linux, o reconhecimento de voz roda em um **processo separado**: se esse processo cair, o FreeCAD continua aberto e o motivo aparece no Relatório do FreeCAD e no `dav.log`.

Para relatar um problema, envie:
1. As últimas linhas do `dav.log` (e o conteúdo do `dav_fault.log`, se existir).
2. O que o terminal mostra ao abrir com `./iniciar_dav.sh`.
3. A sua versão do Ubuntu/Lubuntu e se é uma máquina virtual.
