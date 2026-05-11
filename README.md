# DAVCore - Grupo 1

## Estado Actual del Proyecto

Este repositorio contiene la implementación funcional de la escucha latente, gestión de hilos y procesamiento de comandos de voz.

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

## ¿Cómo ejecutar el proyecto?

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
