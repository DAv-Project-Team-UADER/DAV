# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""
GestorDeHilos — Gestor de ciclo de vida de hilos para DAVCore.

Diagrama de clases (Mermaid):

```mermaid
classDiagram
    class GestorDeHilos {
        -int _maxHilos
        -list _hilos
        +__init__(maxHilos: int)
        +iniciar() void
        +detener() void
        -_tareaHilo(indice: int) void
    }
    class threading.Thread {
        +start()
        +join()
    }
    GestorDeHilos --> threading.Thread : crea y gestiona
```

Diagrama de flujo (Mermaid):

```mermaid
flowchart TD
    A[Inicio] --> B[GestorDeHilos.iniciar]
    B --> C{i < maxHilos?}
    C -- Sí --> D[Crear Thread i]
    D --> E[Thread i duerme hasta estar activo]
    E --> F[Thread i imprime 'Hilo i activo']
    F --> C
    C -- No --> G[Hilo principal imprime 1..9 y listo]
    G --> H[GestorDeHilos.detener]
    H --> I{hilos pendientes?}
    I -- Sí --> J[Thread i imprime 'Hilo i cerrando']
    J --> K[sleep 1s]
    K --> I
    I -- No --> L[Fin]
```

Autores: Bianca Micaela Tournour, Maitén Blanc, Julian Agustín Olivera
Grupo 4 — Práctica Educativa Territorial FCyT-UADER, 2026
"""

import threading
import time


class GestorDeHilos:
    """Gestiona el ciclo de vida de hasta N hilos de trabajo.

    Levanta todos los hilos de forma secuencial (uno tras otro),
    luego los cierra uno a uno con un segundo de separación mientras
    el hilo principal imprime la cuenta del 1 al 9 seguida de 'listo'.
    """

    def __init__(self, maxHilos: int = 10):
        self._maxHilos = maxHilos
        self._hilos: list[threading.Thread] = []
        self._eventos: list[threading.Event] = []

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def iniciar(self) -> None:
        """Crea y arranca cada hilo de forma secuencial."""
        for i in range(self._maxHilos):
            evento = threading.Event()
            self._eventos.append(evento)
            hilo = threading.Thread(
                target=self._tareaHilo,
                args=(i + 1, evento),
                name=f"DAV-Hilo-{i + 1}",
                daemon=True,
            )
            self._hilos.append(hilo)
            hilo.start()
            print(f"Hilo {i + 1} activo")

    def detener(self) -> None:
        """Señala el cierre de cada hilo uno por segundo; el hilo
        principal imprime 1..9 durante los primeros nueve cierres y
        'listo' al terminar todos."""
        for i, evento in enumerate(self._eventos):
            if i < self._maxHilos - 1:
                print(i + 1)
            evento.set()
            time.sleep(1)
        print("listo")

        for hilo in self._hilos:
            hilo.join()

    # ------------------------------------------------------------------
    # Implementación interna
    # ------------------------------------------------------------------

    def _tareaHilo(self, indice: int, evento: threading.Event) -> None:
        """Tarea ejecutada por cada hilo: espera la señal de cierre."""
        evento.wait()
        print(f"  Hilo {indice} cerrando")


# ------------------------------------------------------------------
# Punto de entrada para prueba directa
# ------------------------------------------------------------------

if __name__ == "__main__":
    gestor = GestorDeHilos(maxHilos=10)
    gestor.iniciar()
    gestor.detener()