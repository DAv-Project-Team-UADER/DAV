# Cómo ejecutar la prueba funcional (modo demo)

Este documento explica paso a paso cómo ejecutar la prueba funcional que valida el flujo de carga, traducción, navegación y ejecución de funciones en `PruebaIntegracion` sin depender de un micrófono ni de `Vosk`.

Requisitos mínimos

- Python 3.8+ (probado con Python 3.11)
- Entorno virtual recomendado

Opcional (para modo real)

- `vosk` y `sounddevice` instalados y un modelo Vosk descargado.

Archivos relevantes

- `PruebaIntegracion/main.py` — arranque flexible (modo demo o real).
- `PruebaIntegracion/dic/` — contiene módulos cargables (se incluye un ejemplo `dic/Demo`).
- `PruebaIntegracion/core/CargadorConTraducciones.py` — escanea `dic/` y crea el árbol.
- `PruebaIntegracion/core/ExploradorVoz.py` — bucle principal de navegación y ejecución.

1. Preparar entorno (opcional pero recomendado)

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

2. Ejecutar con Vosk (modo real)

Si querés probar con micrófono y Vosk, instala las dependencias y pasa `--modelo` apuntando al directorio del modelo (por ejemplo, `modelo/vosk-model-small-es-0.42`). El comando es:

```bash
python -m main --modelo modelo/vosk-model-small-es-0.42
```

Notas y troubleshooting

- Si `dic/` está vacío, `main.py` usa un fallback demo (ver `dic/Demo`). Agregá carpetas y `TraduceTo*.py` para ampliar.
- Si la ejecución se queda esperando, verificá que el script demo tenga `enviar` al final de la frase de selección, porque `Command` usa `enviar` como confirmación.
- Para el modo real, si `vosk` lanza errores al cargar el modelo, asegurate que la ruta `--modelo` sea correcta y que el paquete `vosk` esté instalado en el entorno activo.


