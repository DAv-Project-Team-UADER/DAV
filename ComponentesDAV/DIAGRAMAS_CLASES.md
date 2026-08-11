# Diagramas de Clases - ComponentesDAV

## 1. Diagrama General de Componentes

```mermaid
classDiagram
    class MainWindow {
        -color: str
        -lang: str
        -_T: dict
        -_Level: str
        -_ActiveGroup: str
        -_HelpWindow: HelpWindow
        -_VoiceMap: dict
        -_TreeImageLabel: QLabel
        -_RefreshTimer: QTimer
        -_CaptureTimer: QTimer
        +SetColor(mode: str)
        +SetLanguage(lang: str)
        +_SetupUi()
        +_StartVoiceRecognition()
        +OpenHelpWindow()
        +_RefreshTreeImage()
        +_AutoCapture()
        +_UpdateStyles()
        +_RebuildButtons()
    }

    class VoiceWorker {
        -model_path: str
        -running: bool
        -audio_queue: Queue
        +finished: Signal
        +partial_result: Signal
        +final_result: Signal
        +status_signal: Signal
        +audio_callback()
        +run()
        +stop()
    }

    class HelpWindow {
        -T: dict
        -L: dict
        +__init__(T, L, parent)
    }

    class FlashOverlay {
        -_Progress: float
        -_Direction: int
        -_Timer: QTimer
        +Trigger()
        +_Step()
        +paintEvent()
    }

    class Keychain {
        -FilePath: str
        -_Content: str
        +GetKeys()
        +GetValues()
        +GetIcons()
        +GetAllKeys()
        -_extract_keys_from_literal()
        -_extract_values_from_literal()
        -_extract_keys_from_dict_call()
        -_extract_values_from_dict_call()
    }

    class EspecialOperations {
        +Minimize()
        +Maximize()
        +Raise()
        +Lower()
        +RedoPrevious()
        +UndoPrevious()
    }

    MainWindow --> VoiceWorker
    MainWindow --> HelpWindow
    MainWindow --> FlashOverlay
    MainWindow --> Keychain
    MainWindow --> EspecialOperations
```

## 2. Componente InterfazDAV (Interfaz de Usuario)

```mermaid
classDiagram
    class MainWindow {
        -setWindowTitle()
        -setMinimumSize(width, height)
        -_HelpWindow: HelpWindow
        -_Level: str
        -_ActiveGroup: str
        -_ToolButtons: list
        -_GroupMeta: dict
        -_VoiceMap: dict
        -_TreeImageLabel: QLabel
        -_LastImageMtime: float
        -_MacroChecked: bool
        +__init__(color, lang)
        +SetColor(mode)
        +SetLanguage(lang)
        +_SetupUi()
        +_StartVoiceRecognition()
        +_MicQss(color)
        +_PanelQss(font, color, size)
        +_BtnQss()
        +_BackBtnQss()
        +_ThemeBtnQss()
        +_FlashButton(button)
        +OpenHelpWindow()
        +_RefreshTreeImage()
        +_AutoCapture()
        +_UpdateStyles()
    }

    class HelpWindow {
        -T: dict
        -L: dict
        -setWindowTitle(title)
        -setMinimumSize(width, height)
        -setModal(modal)
        +__init__(T, L, parent)
    }

    class FlashOverlay {
        -Parent: QWidget
        -_Progress: float
        -_Direction: int
        -_Timer: QTimer
        +__init__(Parent)
        +Trigger()
        +_Step()
        +paintEvent(event)
    }

    class VoiceWorker {
        -model_path: str
        -running: bool
        -audio_queue: Queue
        -finished: Signal
        -partial_result: Signal
        -final_result: Signal
        -status_signal: Signal
        +__init__(model_path)
        +audio_callback(indata, frames, time, status)
        +run()
        +stop()
    }

    MainWindow <|-- HelpWindow
    MainWindow --> FlashOverlay
    MainWindow --> VoiceWorker
```

## 3. Componente Keychain (Gestión de Diccionarios)

```mermaid
classDiagram
    class Keychain {
        -FilePath: str
        -_Content: str
        +__init__(FilePath)
        +GetKeys() list
        +GetValues() list
        +GetIcons(base_dir) list
        +GetAllKeys() list
        -_extract_keys_from_literal(start_idx)
        -_extract_values_from_literal(start_idx)
        -_extract_keys_from_dict_call(start_idx)
        -_extract_values_from_dict_call(start_idx)
        -_scan_nested_string(start_idx)
    }

    class Header {
        Note: Módulo de definición de encabezados
        Note: Contiene configuración de rutas y referencias
    }

    Keychain --> Header
```

## 4. Componente IntegracionGUI (Operaciones Especiales)

```mermaid
classDiagram
    class EspecialOperations {
        +Minimize()
        +Maximize()
        +Raise()
        +Lower()
        +RedoPrevious()
        +UndoPrevious()
    }

    class explorer {
        Note: Implementación del explorador de FreeCAD
    }

    class Base {
        Note: Diccionario con mapeos de comandos
        -explorer: explorer
        -Draft: explorer
        -minimize: EspecialOperations
        -maximize: EspecialOperations
        -raise: EspecialOperations
        -lower: EspecialOperations
        -redo_previous: EspecialOperations
        -undo_previous: EspecialOperations
    }

    Base --> EspecialOperations
    Base --> explorer
```

## 5. Módulos de Configuración (Paletas y Textos)

```mermaid
classDiagram
    class Paletas {
        +LIGHT: dict
        +DARK: dict
        +FONT_SANS: str
        +FONT_MONO: str
    }

    class Textos {
        +TEXTS: dict
        +MODEL_PARTS: dict
        +MODEL_PARTS_ALIASES: dict
    }

    Paletas <-- MainWindow
    Textos <-- MainWindow
```

## 6. Diagrama Jerárquico Completo

```mermaid
graph TB
    subgraph InterfazDAV["InterfazDAV - Interfaz de Usuario"]
        MainWindow["MainWindow<br/>Ventana Principal"]
        HelpWindow["HelpWindow<br/>Ventana de Ayuda"]
        FlashOverlay["FlashOverlay<br/>Animación Visual"]
        VoiceWorker["VoiceWorker<br/>Reconocimiento Voz"]
        Paletas["Paletas<br/>Temas de Color"]
        Textos["Textos<br/>Traducciones"]
    end

    subgraph Keychain_comp["Keychain - Gestión de Diccionarios"]
        Keychain["Keychain<br/>Parser de Diccionarios"]
        Header["Header<br/>Configuración"]
    end

    subgraph IntegracionGUI_comp["IntegracionGUI - Integración"]
        EspecialOperations["EspecialOperations<br/>Operaciones de Ventana"]
        explorer["explorer<br/>Explorador FreeCAD"]
        Base["Base<br/>Mapeos de Comandos"]
    end

    subgraph Dav_comp["DAV - Módulo de Aplicación"]
        DavCore["DAV Core<br/>Lógica Principal"]
    end

    MainWindow --> HelpWindow
    MainWindow --> FlashOverlay
    MainWindow --> VoiceWorker
    MainWindow --> Paletas
    MainWindow --> Textos
    MainWindow --> Keychain
    MainWindow --> EspecialOperations

    Keychain --> Header
    Base --> EspecialOperations
    Base --> explorer

    InterfazDAV --> IntegracionGUI_comp
    InterfazDAV --> Keychain_comp
    Dav_comp --> InterfazDAV
```

## 7. Flujo de Interacción Principal

```mermaid
sequenceDiagram
    participant Usuario
    participant MainWindow
    participant VoiceWorker
    participant Keychain
    participant EspecialOperations
    participant HelpWindow

    Usuario ->> MainWindow: Inicializa (color, idioma)
    MainWindow ->> Paletas: Carga tema
    MainWindow ->> Textos: Carga traducciones
    MainWindow ->> Keychain: Lee diccionarios
    MainWindow ->> VoiceWorker: Inicia reconocimiento

    Usuario ->> VoiceWorker: Habla comando
    VoiceWorker -->> MainWindow: Emite resultado
    MainWindow ->> Keychain: Busca comando

    alt Comando Encontrado
        MainWindow ->> EspecialOperations: Ejecuta operación
    else Ayuda Solicitada
        MainWindow ->> HelpWindow: Abre ventana
    else Comando Desconocido
        MainWindow -->> Usuario: Muestra error
    end
```

## Relaciones Entre Componentes

### Dependencias
- **MainWindow**: depende de VoiceWorker, HelpWindow, FlashOverlay, Keychain, Paletas, Textos
- **VoiceWorker**: depende de Vosk (librería externa) y sounddevice
- **HelpWindow**: depende de Paletas, Textos
- **FlashOverlay**: hereda de QWidget (PySide6)
- **Keychain**: módulo independiente de análisis de texto
- **EspecialOperations**: interactúa con FreeCADGui

### Composición
- MainWindow **contiene** elementos de UI (QLabel, QPushButton, QTextEdit)
- MainWindow **utiliza** VoiceWorker para captura de audio
- MainWindow **crea** HelpWindow cuando es necesario
- MainWindow **aplica** temas de Paletas y traducciones de Textos

### Interfaces
- Paletas: proporciona diccionarios de colores (LIGHT, DARK)
- Textos: proporciona diccionarios de traducciones (es, en, pt)
- Keychain: interfaz para lectura de diccionarios Python
