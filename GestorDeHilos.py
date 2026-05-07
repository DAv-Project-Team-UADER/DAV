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

import threading
import time


class GestorDeHilos:
    """Gestiona el ciclo de vida de hasta N hilos de trabajo."""

    def __init__(self, maxHilos: int = 10):
        self._maxHilos = maxHilos
        self._hilos: list[threading.Thread] = []
        self._eventos: list[threading.Event] = []

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
        """Cierra cada hilo uno por segundo; imprime 1..9 y luego 'listo'."""
        for i, evento in enumerate(self._eventos):
            if i < self._maxHilos - 1:
                print(i + 1)
            evento.set()
            time.sleep(1)
        print("listo")

        for hilo in self._hilos:
            hilo.join()

    def _tareaHilo(self, indice: int, evento: threading.Event) -> None:
        evento.wait()
        print(f"  Hilo {indice} cerrando")