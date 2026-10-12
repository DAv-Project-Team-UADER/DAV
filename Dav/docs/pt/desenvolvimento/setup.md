# Colocação em funcionamento (setup)

Guia para subir o DAV e testar o motor de voz em uma máquina local.

> ⚠️ **Os dois interpretadores.** O venv de desenvolvimento
> (`IntegracionGUI/GUIFreeCad/.venv`) usa um Python mais novo que o Python
> embutido do FreeCAD. O código tem que rodar em ambos: **os scripts que
> são carregados dentro do FreeCAD usam o interpretador do FreeCAD, não o venv.**
> As extensões do FreeCAD devem usar **PySide6**, não PyQt, por
> compatibilidade construtiva com o framework nativo.

## 1. Clonar o repositório

O fluxo de contribuição é feito com **fork pessoal** + **Pull Request** (veja
o fluxo completo em `CLAUDE.md` e em `guia-desenvolvimento-dav.md` → GitFlow).

```bash
git clone https://github.com/<tu-usuario>/DAV.git
cd DAV
```

Se você quiser o repositório central diretamente:

```bash
git clone https://github.com/DAv-Project-Team-UADER/DAV.git
```

## 2. Dependências Python (venv de desenvolvimento)

O ambiente de desenvolvimento vive em
`Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/.venv` com as dependências
declaradas em `requirements.txt`:

```
PySide6>=6.6.0
vosk>=0.3.45
sounddevice>=0.4.6
numpy>=1.24.0
requests>=2.31.0
tqdm>=4.66.0
```

Para recriá-lo/instalá-lo:

```bash
cd Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad
python -m venv .venv
.venv\Scripts\activate          # Windows
# ou: source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

> Este venv serve para **desenvolver/testar o widget de GUI e os prompts** de
> forma isolada. Para testar a voz **dentro do FreeCAD** é preciso ter as
> dependências disponíveis para o interpretador do FreeCAD (módulos instalados
> no ambiente que roda o FreeCAD).

## 3. Modelos de voz Vosk

Os modelos vivem em `Dav/models/` (excluídos do git — veja
`Dav/models/README.md`):

| Modelo | Idioma |
|---|---|
| `vosk-model-small-es-0.42` | Espanhol |
| `vosk-model-small-en-us-0.15` | Inglês |
| `vosk-model-small-pt-0.3` | Português |

Não é preciso baixá-los manualmente: `core/model_manager.py` e
`ui/download_dialog.py` (em `IntegracionGUI/GUIFreeCad/`) os baixam se
faltarem. Existe também o script `scripts/setup_models.py`.

> Para maior precisão em espanhol existe o `vosk-model-es-0.42` (mais pesado), não
> incluído por padrão.

## 4. Rodar o DAV dentro do FreeCAD

O DAV inicia dentro do **console Python** do FreeCAD (Exibir → Painéis →
Console Python) ou como **macro**. O `DAVCore` deve ser iniciado igual ao
`FreeCADGuiInit.py`, ou seja, ao iniciar a aplicação.

Passos gerais:

1. Abra o FreeCAD com um documento novo.
2. Abra o **Console Python**.
3. Carregue e execute a inicialização do motor de voz (o bootstrap que monta o
   `Browser` + microfone). Veja `integration/voice_bootstrap.py` e o
   `InitGui.py` em `scr/.../Dav/` para a inicialização automática com o FreeCAD.
4. Configure o idioma em **Preferências DAV** se não for espanhol.

> O painel DAV é montado como `QDockWidget` dentro do FreeCAD via
> `integration/dav_dock_panel.py`. Se iniciar como janela flutuante, pode ser
> ancorado em qualquer borda.

## 5. Comandos básicos para verificar o setup

Com o motor ativo, teste frases de navegação do próprio Browser (não mexem em
nada do documento):

- **`donde estoy`** (onde estou) — mostra o contexto atual.
- **`subir`** (subir) — sobe um nível da árvore de navegação.

E um comando real, por exemplo:

```
banco de trabajo → diseñador de piezas    (ir ao workbench PartDesign)
```

Os comandos de confirmação/aborto de pop-ups (compartilhados pelos prompts):

- **Confirmar um valor**: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`
- **Abortar um pop-up**: `cancelar`

## Portas / problemas comuns

- **O microfone usa PyAudio/SoundDevice** — se o stream não abre, verifique
  se o dispositivo está disponível e desocupado.
- **No Linux o microfone roda em um processo separado** (`speech/voice_worker.py`,
  com o Python do `.venv`): se o PortAudio ou o Vosk caírem, o FreeCAD continua
  aberto e o erro aparece no Relatório. Para usar o modo anterior (dentro do
  FreeCAD) exporte `DAV_VOICE_INPROCESS=1`.
- **Se o FreeCAD fechar de repente** — veja `GUIFreeCad/config/dav.log` (a última
  linha indica em que passo estava) e `dav_fault.log` (criado em uma queda nativa).
- **O modelo não foi carregado** → confirme que existe em `Dav/models/<idioma>` ou
  que `setup_models.py` o baixou.
- **A gramática é restrita por contexto** — certos prompts (numéricos, de
  seleção de plano) limitam de propósito quais palavras o Vosk escuta. Se um
  comando "não é entendido", verifique se há um prompt ativo restringindo a
  gramática (veja `encurtador-gramatica-vosk.md`).

---

Próximo: [Convenções de código](convencoes.md)
