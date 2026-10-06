# Estrutura do repositório

O repositório mistura duas coisas: o **código-fonte do FreeCAD** (o fork base
que é trazido completo) e o **código próprio do DAV** (a camada de voz). É
importante saber em qual metade você está trabalhando, porque os cabeçalhos de
licença e as regras são diferentes.

```
DAV/
├── FREECAD/          # Código-fonte do FreeCAD (fork base, NÃO se mexe nisto a menos que seja necessário)
│   ├── src/          #   Módulos Python e C++ do FreeCAD
│   │   ├── App/      #   Núcleo da aplicação (FreeCADInit.py)
│   │   ├── Gui/      #   Interface gráfica (FreeCADGuiInit.py)
│   │   ├── Ext/freecad/  #   Extensões Python próprias do FreeCAD
│   │   └── Mod/      #   Workbenches: Draft, Sketcher, Part, PartDesign,
│   │                 #     Assembly, TechDraw, etc.
│   └── CMakeLists.txt
├── Dav/              # ⭐ TODO o código próprio do projeto DAV
│   ├── dic/          #   Árvore de comandos por voz (veja abaixo)
│   ├── docs/         #   Documentação, planos, relatórios, normativas
│   ├── models/       #   Modelos Vosk es/en/pt (excluídos do git)
│   └── scr/          #   Código-fonte em Python
│       ├── ComponentesDAV/
│       │   ├── IntegracionGUI/  # Motor Browser (navigation/) + montagem do painel
│       │   ├── InterfazDAV/     # DavPanel: o widget da GUI (sem FreeCAD)
│       │   ├── Keychain/        # Leitura de chaves de dicionários
│       │   ├── Dav/             # InitGui.py — inicialização dentro do FreeCAD
│       │   ├── Logos/
│       │   └── scripts/
│       ├── PruebaIntegracion/
│       ├── selection/           # CreateObjects — extração de subelementos
│       └── validation/          # Validator — regras de validação de comandos
└── CLAUDE.md
```

## Onde vive cada coisa

| O que você está procurando? | Onde está? |
|---|---|
| Motor de navegação por voz (`Browser`) | `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/navigation/browser.py` |
| Árvore de comandos por voz | `Dav/dic/` |
| Tradução frase falada → comando | `TraduceTo*.py` dentro de cada pasta de `Dav/dic/` |
| Leitura de chaves de dicionários | `Dav/scr/ComponentesDAV/Keychain/` |
| Widget da GUI (painel) | `Dav/scr/ComponentesDAV/InterfazDAV/DavPanel.py` |
| Extração de subelementos (seleção) | `Dav/scr/selection/` |
| Validação de comandos | `Dav/scr/validation/` |
| Modelos Vosk (não versionados) | `Dav/models/` |
| Documentação do projeto | `Dav/docs/es/` (espanhol) e `Dav/docs/en/` (inglês) |

## A árvore de comandos por voz (`Dav/dic/`)

Cada **pasta** da árvore é um **nível de contexto** e tem:

- Um dicionário mestre: `<nome>.py` com as **chaves internas → callables**
  do FreeCAD (ex.: `explorer.py`, `sketcher.py`).
- Traduções por idioma: `TraduceToEs.py`, `TraduceToEn.py`, `TraduceToPT.py`
  que mapeiam **frases faladas → os mesmos callables**.

`Dav/dic/base.py` é o ponto de entrada: vincula os módulos de nível superior
(`explorer`, `stdview`, `workbench`, `lineattributes`, `preferences`).

O motor que percorre essa árvore em runtime é o `Browser`
(`Dav/scr/.../GUIFreeCad/navigation/browser.py`) + `DictionaryLoader`
(`navigation/dictionary_loader.py`).

> ⚠️ Importante: embora historicamente tenha existido um `DAVAgent` com
> `latentListening`, a implementação real usa `Browser.ProcessPhrase` +
> `DictionaryLoader`. Se um diagrama antigo mostra `DAVAgent`, é o design
> conceitual original, não o código vigente.

## A GUI é um painel acoplado

O painel (`DavPanel`) é um `QDockWidget` que roda dentro do FreeCAD e é
alimentado pelo `Browser` **em processo** via
`Dav/scr/.../GUIFreeCad/integration/dav_dock_panel.py`. O widget não importa
o FreeCAD: recebe dados e emite sinais, assim pode ser testado separadamente.

Já não existem `MainWindow.py`, seu motor de voz próprio (`_VoiceMap`/`_GroupMeta`)
nem `DiccionarioPrueba/`: foram removidos ao acoplar o painel.
