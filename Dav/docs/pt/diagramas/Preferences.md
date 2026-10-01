# Preferences e Settings

> **Arquivos:**
> `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/preferences.py`
> `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/settings.py`

Duas classes com papéis distintos que convém não confundir: `Settings` persiste a
configuração em disco; `Preferences` expõe o idioma ativo ao `Browser` e
avisa quando ele muda.

```mermaid
classDiagram
    class Preferences {
        -list~Callable~ _language_callbacks

        +SetLanguage() LanguageCode
        +RegisterLanguageChange(callback) void
        +UnregisterLanguageChange(callback) void
    }

    class Settings {
        -dict _data

        +language() String
        +model_size() String
        +theme() String
        +startup_enabled() bool
        +auto_voice() bool
        +load() void
        +save() void
        +as_dict() dict
    }

    class LanguageCode {
        <<enumeration>>
        Es
        En
        PT
        +FromStorage(value)$ LanguageCode
    }

    Preferences ..> Settings : lê e escreve language
    Preferences ..> LanguageCode : tipo do idioma
    Browser ..> Preferences : RegisterLanguageChange
```

## O fluxo de uma troca de idioma

```mermaid
sequenceDiagram
    participant D as Diálogo Preferências
    participant P as Preferences
    participant S as Settings
    participant B as Browser
    participant V as DavVoiceService

    D->>P: SetLanguage = LanguageCode.Es
    P->>S: language = "es" ; save()
    P->>B: callback(anterior, novo)
    B->>B: ResetFromBase()
    Note over B: recarrega TraduceToEs.py<br/>de toda a árvore
    D->>V: reinicia o microfone
    Note over V: é preciso recarregar o modelo:<br/>é outro arquivo do Vosk
```

## Notas de design

- **`Preferences` é o único que deveria escrever o idioma.** É o ponto em que
  se dispara a recarga dos dicionários; escrever `settings.language` à mão
  a ignora.
- **O observer é uma lista, não um callback único** (`RegisterLanguageChange`),
  assim vários interessados podem se inscrever sem se sobrescrever.
- `Settings` salva em `config/settings.json`, que está no `.gitignore`: é
  configuração do usuário, não do repositório.
- Trocar o idioma **obriga a reiniciar a thread de voz**, porque o modelo Vosk
  é carregado uma única vez ao criar o recognizer e cada idioma é um modelo
  diferente.
