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
| **FreeCAD 1.1.3 (AppImage)** | É o programa base. Baixe-o em [FreeCAD](https://www.freecad.org/downloads.php) e guarde-o na sua pasta de **Descargas** (ou **Downloads**). |
| **Microfone** | Para usar os comandos de voz. |
| **Internet** | Somente na primeira vez: o DAV baixa o modelo de voz Vosk (≈ 40 MB) e dependências. |
| **Python 3.10+** | Geralmente já vem instalado por padrão nas distribuições Linux modernas (Ubuntu, Mint, Fedora). |

> **Não é preciso** baixar modelos de voz manualmente. O DAV cuida de tudo isso automaticamente na primeira vez que você o abre.

---

## Caminho A — Usuário final

Para quem **só quer usar o DAV**, sem abrir o código nem usar o terminal. É um único arquivo executável.

### Passo 1 — Baixe o FreeCAD
1. Acesse <https://www.freecad.org/downloads.php>.
2. Baixe a versão **1.x** no formato `.AppImage` (Linux).
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
* Baixe o **AppImage do FreeCAD 1.1.3** e deixe-o na sua pasta `~/Descargas/`.

### 2. Clone o repositório
Abra um terminal e execute:
```bash
git clone [https://github.com/DAv-Project-Team-UADER/DAV.git](https://github.com/DAv-Project-Team-UADER/DAV.git)
cd DAV
```

### 3. Execute o script de início
Dentro da pasta do projeto que você acabou de clonar, conceda permissões e execute o automatizador:
```bash
chmod +x inicio_dav.sh
./inicio_dav.sh
```

O script `inicio_dav.sh` se encarrega de:
1. Criar um link simbólico do seu código-fonte para `~/.local/share/FreeCAD/v1-1/Mod/DAV`.
2. Procurar a AppImage do FreeCAD na sua pasta de Descargas utilizando um caminho universal (`$HOME`).
3. Lançar o FreeCAD com o seu ambiente de desenvolvimento carregado. Qualquer mudança que você salvar no código Python será refletida ao reiniciar o FreeCAD.

---

## Problemas frequentes

| Problema | Solução |
| :--- | :--- |
| **"Permissão negada" ao dar duplo clique** | Faltou o Passo 3 do Caminho A. Clique direito no arquivo > Propriedades > Permissões > Permitir executar como programa. |
| **"FreeCAD não encontrado"** | Verifique que o arquivo do FreeCAD termine em `.AppImage` e esteja diretamente na pasta `Descargas` (ou `Downloads`). |
| **O microfone não responde / Erro do Vosk** | É possível que faltem dependências de áudio no Linux. Abra um terminal e execute `sudo apt install portaudio19-dev python3-pyaudio`. |
| **Na primeira vez demora muito** | É normal, está baixando o modelo de voz em segundo plano. |
