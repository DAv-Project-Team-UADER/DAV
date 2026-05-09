import os
import sys
from src.voskModel.VoskModel import VoskModel
from src.threads.GestorDeHilos import GestorDeHilos
from src.command.command import Command

def main():
    model_path = "vosk-model-small-es-0.42"

    if not os.path.exists(model_path):
        print(f"ERROR: No se encuentra la carpeta '{model_path}'")
        sys.exit(1)

    vosk_wrapper  = VoskModel(model_path)
    gestor        = GestorDeHilos()
    cmd_processor = Command(vosk_wrapper)

    gestor.iniciar_ventanas()
    vosk_wrapper.set_callback_texto(gestor.actualizar_texto_ventana1)

    try:
        cmd_processor.print_test(0)

        print("\n>>> ESCUCHA LATENTE ACTIVA")
        print(">>> Di 'cerrar' para finalizar.\n")

        vosk_wrapper.escuchar_latente(frase_despertar="cerrar")

    except KeyboardInterrupt:
        pass
    finally:
        gestor.cerrar_todos(intervalo_segundos=1.0)

if __name__ == "__main__":
    main()