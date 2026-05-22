# test_interactivo.py
from VoskModel import VoskModel

def callback_de_pantalla(texto):
    print(f"[UI Callback] -> Mostrando en pantalla: {texto}")

def main():
    # Asegúrate de que la ruta apunte a la carpeta donde descomprimiste el modelo de Vosk
    ruta_modelo = "vosk-model-small-es-0.42" 
    
    print("Cargando modelo... por favor espera.")   
    # Activamos el modo debug para ver qué pasa internamente
    reconocedor = VoskModel(model_path=ruta_modelo, debug=True)
    
    # Probando el callback
    reconocedor.set_callback_texto(callback_de_pantalla)

    print("\n" + "="*50)
    print("PRUEBA 1: Escuchar una sola palabra/frase")
    print("Di algo por el micrófono...")
    resultado_una_palabra = reconocedor.escuchar_una_palabra()
    print(f"Resultado Prueba 1: '{resultado_una_palabra}'")
    print("="*50)

    print("\n" + "="*50)
    print("PRUEBA 2: Escucha latente continua")
    print("Di varias cosas. Para terminar la prueba di la palabra: 'apagar'")
    reconocedor.escuchar_latente(frase_despertar="apagar")
    print("Resultado Prueba 2: Finalizada correctamente.")
    print("="*50)

if __name__ == "__main__":
    main()