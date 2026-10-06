# Como executar o teste funcional (modo demo)

Este documento explica passo a passo como executar o teste funcional que valida o fluxo de carregamento, tradução, navegação e execução de funções em `PruebaIntegracion` sem depender de um microfone nem do `Vosk`.

Requisitos mínimos

- Python 3.8+ (testado com Python 3.11)
- Ambiente virtual recomendado

Opcional (para modo real)

- `vosk` e `sounddevice` instalados e um modelo Vosk baixado.

Arquivos relevantes

- `PruebaIntegracion/main.py` — inicialização flexível (modo demo ou real).
- `PruebaIntegracion/dic/` — contém módulos carregáveis (inclui um exemplo `dic/Demo`).
- `PruebaIntegracion/core/CargadorConTraducciones.py` — varre `dic/` e cria a árvore.
- `PruebaIntegracion/core/ExploradorVoz.py` — loop principal de navegação e execução.

1. Preparar o ambiente (opcional, mas recomendado)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
# instalar dependencias opcionales (solo para modo real)
pip install vosk sounddevice
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install vosk sounddevice
```

2. Executar com Vosk (modo real)

Se você quiser testar com microfone e Vosk, instale as dependências e passe `--modelo` apontando para o diretório do modelo (por exemplo, `modelo/vosk-model-small-es-0.42`). O comando é:

```bash
python -m main --modelo modelo/vosk-model-small-es-0.42
```

Notas e troubleshooting

- Se `dic/` está vazio, `main.py` usa um fallback demo (veja `dic/Demo`). Adicione pastas e `TraduceTo*.py` para ampliar.
- Se a execução ficar esperando, verifique que o script demo tenha `enviar` no final da frase de seleção, porque `Command` usa `enviar` como confirmação.
- Para o modo real, se o `vosk` lançar erros ao carregar o modelo, certifique-se de que o caminho `--modelo` esteja correto e que o pacote `vosk` esteja instalado no ambiente ativo.
