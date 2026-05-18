<<<<<<< Updated upstream
# DAVCore - Grupo 1

## Estado Actual del Proyecto
=======
# Transcripción de voz a texto y Reconocimiento de Comandos con Vosk (español)

Sistema avanzado en Python para transcribir audio en vivo desde el micrófono usando **Vosk** y cancelar ruido en tiempo real usando **RNNoise**. Además, el sistema procesa el habla mediante expresiones regulares (Regex) para identificar intenciones de diseño paramétricas y ejecutar comandos.
>>>>>>> Stashed changes

Este repositorio contiene la implementación funcional de la escucha latente, gestión de hilos y procesamiento de comandos de voz.

<<<<<<< Updated upstream
### 1. Escucha Latente (VoskModel)
- **Ubicación:** `src/modelo/VoskModel.py`
- El sistema utiliza el modelo pequeño de Vosk para reconocer audio en tiempo real.
- Incluye un sistema de *callbacks* global (`set_callback_texto`) que permite actualizar la interfaz gráfica sin importar el modo de escucha activo.

### 2. Gestión Multihilo (GestorDeHilos)
- **Ubicación:** `src/hilos/GestorDeHilos.py`
- Al iniciar, se levantan **3 hilos paralelos** reales, cada uno con su propia ventana de Tkinter:
  1. **Mostrar texto dictado:** Actualiza su contenido dinámicamente con lo captado por el micrófono.
  2. **Traducir en instrucciones:** (Esqueleto funcional).
  3. **Ejecutar instrucciones:** (Esqueleto funcional).
- **Cierre Secuencial:** Al detectar el comando de cierre, el Gestor destruye las ventanas de forma ordenada con **1 segundo de diferencia**.

### 3. Lógica de Comandos (Command)
- **Ubicación:** `src/comando/Comando.py`
- **ExclusiveListening:** Implementa la lógica de filtrado por vectores. 
  - Soporta conversión de números hablados a dígitos (ej: "uno" -> "1").
  - Maneja comandos especiales: `Enter` (acumular), `Cancelar` (abortar) y `Enviar` (finalizar).
  - Incluye filtro de duplicados consecutivos.
- **PrintTest:** Método de prueba que ejecuta la escucha exclusiva y muestra el resultado final por consola.

---
=======
## Novedades del Sistema

- **Parseo Dinámico Robusto**: Reconoce comandos complejos como crear círculos, arcos, elipses, polilíneas, y otras acciones de la aplicación con sus respectivos números dictados (ej: *"crear punto en cuatro cinco"* o *"arco de elipse centro cero cero radio mayor cinco..."*).
- **Traducción de Números a Dígitos**: Traduce automáticamente "uno", "dos", "tres" a `1`, `2`, `3` y tiene tolerancia contra errores acústicos y tartamudeos propios del modelo (ej: traduce "cuatroro" o "cincoco").
- **Cancelación de Ruido (RNNoise)**: Procesa el audio al vuelo filtrando ruidos de fondo.
- **Registro Inmediato en Disco**: Escribe la conversación en `transcripcion.txt` al instante.
- **Bitácora Estructurada (JSONL)**: Guarda los comandos detectados con sus variables listas para ejecución en un formato legible por máquina (`comandos_reconocidos.jsonl`).

## Requisitos y Dependencias

Asegúrate de contar con Python 3.x y las siguientes dependencias:

```bash
pip install vosk sounddevice numpy pyrnnoise
```
>>>>>>> Stashed changes

## ¿Cómo ejecutar el proyecto?

<<<<<<< Updated upstream
1. Instalar dependencias:
   ```bash
   pip install vosk sounddevice
   ```
2. Modelo de voz: Colocar el modelo en `MODELO/vosk-model-small-es-0.42`.
3. Ejecutar:
   ```bash
   python main.py
   ```
   *Nota: Por defecto, al ejecutar main.py se iniciará el modo de prueba de Comandos (Vector 0).*
=======
Descargá y descomprimí los modelos en la carpeta raíz del proyecto.
El script los detectará automáticamente buscando los siguientes patrones:
- Chico: `model-small-es` o `vosk-model-small-es-*`
- Grande: `model-es` o `vosk-model-es-*`

*Nota: Disponibles en la página web de Vosk (versión 0.42).*

## Uso

Ejecutá el siguiente comando desde tu terminal:

```bash
python captura_voz.py
```

Luego:
1. Elegí el modelo que prefieras usar marcando 1 o 2.
2. Hablá al micrófono de manera natural. Prueba comandos como *"crear línea de 5 5 a 10 10"* o *"deshacer lógica"*.
3. Presioná `Ctrl+C` para terminar y salir del programa de forma segura.

### Archivos de Salida

Durante y al finalizar la sesión, se guardarán dos archivos críticos:
- **`transcripcion.txt`**: Mantiene todo el historial textual de tu dictado en bruto en vivo.
- **`comandos_reconocidos.jsonl`**: Guarda en formato JSON todo comando detectado junto con sus respectivos argumentos numéricos o strings (listo para conectarlo a herramientas como FreeCAD).

---


>>>>>>> Stashed changes
