# DAVCore - Grupo 1

## Estado Actual del Proyecto

Este repositorio contiene la implementación base y funcional de los requerimientos de escucha latente y gestión de hilos del sistema.

### 1. Escucha Latente (VoskModel)
- **Ubicación:** `src/modelo/VoskModel.py`
- El sistema utiliza el modelo pequeño de Vosk para escuchar continuamente desde el micrófono.
- El bucle de escucha se mantiene activo y procesando el audio hasta que se detecta la palabra clave (`"cerrar"`).
- Implementa un sistema de *callbacks* para enviar el texto dictado en tiempo real hacia otros componentes.

### 2. Gestión Multihilo (GestorDeHilos)
- **Ubicación:** `src/hilos/GestorDeHilos.py`
- La lógica concurrente está aislada usando Programación Orientada a Objetos.
- Al iniciar, se levantan **3 hilos paralelos** (heredando de `threading.Thread`), cada uno abriendo una ventana de interfaz independiente:
  1. **Mostrar texto dictado:** Conectada al callback de Vosk, actualiza su texto en pantalla en tiempo real.
  2. **Traducir en instrucciones:** Ventana a la espera de implementación lógica.
  3. **Ejecutar instrucciones:** Ventana a la espera de implementación lógica.
- **Cierre Secuencial:** Al decir la palabra de cierre, el Gestor destruye los hilos de manera ordenada y secuencial, con **1 segundo de diferencia** entre cada uno.

### 3. Lógica de Comandos (Command)
- **Ubicación:** `src/comando/Comando.py`
- Contiene el esqueleto y los *docstrings* en inglés para la clase `Command` (`ExclusiveListening`, `SystematicFill`). Su lógica interna será desarrollada en la siguiente etapa.

---

## ¿Cómo ejecutar el proyecto?

1. Instalar las dependencias necesarias:
   ```bash
   pip install vosk sounddevice
   ```
2. Asegurarse de tener el modelo de voz de Vosk descomprimido dentro de la ruta:
   `MODELO/vosk-model-small-es-0.42`
3. Ejecutar el script principal desde la raíz del proyecto:
   ```bash
   python main.py
   ```
