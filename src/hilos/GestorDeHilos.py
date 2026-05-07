import threading
import time
import tkinter as tk

class VentanaHilo(threading.Thread):
    """
    Representa un hilo independiente que abre una ventana de Tkinter.
    """
    def __init__(self, titulo: str, posicion: str):
        super().__init__()
        self.titulo = titulo
        self.posicion = posicion
        self.debe_cerrar = False
        self.root = None
        self.texto_actual = ""
        self.lbl = None

    def run(self):
        # Cada hilo crea su propia instancia de Tkinter, asegurando que sean procesos paralelos reales
        self.root = tk.Tk()
        self.root.title(self.titulo)
        self.root.geometry(f"350x120+{self.posicion}")
        
        self.lbl = tk.Label(self.root, text=f"Hilo Activo:\n{self.titulo}\n\n", font=("Arial", 11), wraplength=320)
        self.lbl.pack(expand=True)
        
        # Bucle que chequea constantemente eventos
        self._chequear_eventos()
        self.root.mainloop()

    def _chequear_eventos(self):
        if self.debe_cerrar and self.root:
            self.root.quit() # Salir limpiamente del mainloop
            self.root.destroy()
        elif self.root:
            # Si es la primera ventana, actualizamos su texto en pantalla
            if self.titulo.startswith("1") and self.lbl:
                self.lbl.config(text=f"Hilo Activo:\n{self.titulo}\n\nTexto Dictado:\n'{self.texto_actual}'")
            # Vuelve a chequear en 200 milisegundos
            self.root.after(200, self._chequear_eventos)

    def cerrar(self):
        """Activa la bandera para que la ventana se destruya a sí misma."""
        self.debe_cerrar = True
        
    def actualizar_texto(self, texto: str):
        """Guarda el texto más reciente dictado."""
        self.texto_actual = texto


class GestorDeHilos:
    """
    Gestiona la creación y cierre ordenado de hilos para DAVCore.
    """

    def __init__(self):
        self._hilos: list[VentanaHilo] = []

    def iniciar_ventanas(self) -> None:
        """Crea los tres hilos con sus respectivas ventanas."""
        nombres = [
            "1 - Mostrar texto dictado", 
            "2 - Traducir en instrucciones", 
            "3 - Ejecutar instrucciones"
        ]
        # Posiciones en pantalla (x+y) para que las ventanas no se tapen entre sí
        posiciones = ["100+100", "100+250", "100+400"]
        
        for i in range(3):
            hilo = VentanaHilo(nombres[i], posiciones[i])
            self._hilos.append(hilo)
            # Al hacer .start(), el hilo empieza a correr en paralelo
            hilo.start()

    def actualizar_texto_ventana1(self, texto: str):
        """Busca el primer hilo y le manda el texto para que lo muestre."""
        if len(self._hilos) > 0:
            self._hilos[0].actualizar_texto(texto)

    def cerrar_todos(self, intervalo_segundos: float = 1.0) -> None:
        """Cierra los hilos uno a uno con el intervalo dado."""
        print("\n[Gestor] Iniciando cierre secuencial de hilos...")
        for hilo in self._hilos:
            print(f"[Gestor] Cerrando: {hilo.titulo}")
            hilo.cerrar()
            time.sleep(intervalo_segundos)
            
        # Esperamos a que los hilos terminen bien para evitar el error Tcl_AsyncDelete al apretar Ctrl+C
        for hilo in self._hilos:
            if hilo.is_alive():
                hilo.join(timeout=1.0)
                
        print("[Gestor] Todos los hilos se han cerrado correctamente.")
