import sys
from src.modelo.VoskModel import VoskModel
from src.hilos.GestorDeHilos import GestorDeHilos
from src.comando.Comando import Command

if __name__ == "__main__":
    ruta_modelo = r"MODELO\vosk-model-small-es-0.42" 
    gestor = GestorDeHilos()
    
    try:
        # 1. Levantamos las ventanas
        gestor.iniciar_ventanas()
        
        # 2. Levantamos el modelo y lo conectamos a la ventana 1
        modelo = VoskModel(ruta_modelo)
        modelo.set_callback_texto(gestor.actualizar_texto_ventana1)
        
        # 3. Levantamos el sistema de comandos
        comando = Command(modelo)
        
        # 4. En lugar de la escucha latente infinita, probamos la Lógica del Grupo 1
        # Esto iniciará la "Escucha Exclusiva" limitando el vocabulario al vector 0 (números)
        print("\n=== PRUEBA DE COMANDOS GRUPO 1 ===")
        print("Intentá decir: 'uno', luego 'enter', luego 'dos', luego 'enviar'")
        comando.PrintTest(0)
        
        # 5. Cerramos ordenadamente
        gestor.cerrar_todos(intervalo_segundos=1.0)
        
    except KeyboardInterrupt:
        print("\nPrograma terminado a la fuerza.")
        gestor.cerrar_todos(intervalo_segundos=0)
