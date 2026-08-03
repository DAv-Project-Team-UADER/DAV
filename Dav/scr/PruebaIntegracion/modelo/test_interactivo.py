#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.
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
    reconocedor.set_text_callback(callback_de_pantalla)

    print("\n" + "="*50)
    print("PRUEBA 1: Escuchar una sola palabra/frase")
    print("Di algo por el micrófono...")
    resultado_una_palabra = reconocedor.listen_for_one_word()
    print(f"Resultado Prueba 1: '{resultado_una_palabra}'")
    print("="*50)

    print("\n" + "="*50)
    print("PRUEBA 2: Escucha latente continua")
    print("Di varias cosas. Para terminar la prueba di la palabra: 'apagar'")
    reconocedor.listen_continuously(wake_phrase="apagar")
    print("Resultado Prueba 2: Finalizada correctamente.")
    print("="*50)

if __name__ == "__main__":
    main()