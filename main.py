import sys

from src.modelo.VoskModel import VoskModel
from src.hilos.GestorDeHilos import GestorDeHilos

if __name__ == "__main__":
    # Ruta relativa al modelo dentro del repositorio
    ruta_modelo = r"MODELO\vosk-model-small-es-0.42" 
    
    gestor = GestorDeHilos()
    
    try:
        # 1. Iniciamos los 3 hilos (ventanas) antes de ponernos a escuchar
        gestor.iniciar_ventanas()
        
        # 2. Iniciamos el motor de Vosk
        modelo = VoskModel(ruta_modelo)
        
        # Pasamos gestor.actualizar_texto_ventana1 para que Vosk le mande el texto en tiempo real
        modelo.escuchar_latente("cerrar", callback_texto=gestor.actualizar_texto_ventana1)
        
        # 3. Si llegamos a esta línea, es porque Vosk detectó la palabra y terminó de escuchar.
        gestor.cerrar_todos(intervalo_segundos=1.0)
        
    except KeyboardInterrupt:
        print("\nPrograma terminado a la fuerza.")
        gestor.cerrar_todos(intervalo_segundos=0)
