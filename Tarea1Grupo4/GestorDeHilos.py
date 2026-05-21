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
    """Manages the lifecycle of up to N worker threads.

    Creates daemon threads identified as ``DAV-Hilo-N``. Each thread blocks on
    an :class:`threading.Event` and exits as soon as that event is set.

    Args:
        maxHilos: Maximum number of threads to spawn. Defaults to 10.

    Example::

        gestor = GestorDeHilos(maxHilos=5)
        gestor.iniciar()
        gestor.detener()
    """

    def __init__(self, maxHilos: int = 10):
        self._maxHilos = maxHilos
        self._hilos: list[threading.Thread] = []
        self._eventos: list[threading.Event] = []

    def iniciar(self) -> None:
        """Create and start each thread sequentially.

        Each thread is a daemon so it does not prevent the process from
        exiting. Prints a confirmation line per thread once it is running.
        """
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
            print(f"Thread {i + 1} active")

    def detener(self) -> None:
        """Stop all threads, signalling one per second.

        Prints the thread index (1 … N-1) before signalling each event, then
        prints ``'ready'`` once all threads have been joined.
        """
        for i, evento in enumerate(self._eventos):
            if i < self._maxHilos - 1:
                print(i + 1)
            evento.set()
            time.sleep(1)
        print("ready")

        for hilo in self._hilos:
            hilo.join()

    def _tareaHilo(self, indice: int, evento: threading.Event) -> None:
        # Bloquea hasta recibir la señal de detención
        evento.wait()
        print(f"  Thread {indice} closing")