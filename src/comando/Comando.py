import threading
from typing import Optional
import unicodedata

class Command:
    """
    Clase base para el manejo de comandos de voz en DAVCore.
    """
    def __init__(self, voice_model):
        self._voice_model = voice_model
        
        # Vectores definidos
        self._vector0 = ["cancelar", "enter", "enviar", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self._vector1 = ["cancelar", "enviar", "linea fina", "linea punteada", "linea normal", "linea gruesa"]
        self._tuple1 = (self._vector0, self._vector1)

    def _normalizar_texto(self, texto: str) -> str:
        """
        Quita tildes y convierte números hablados a dígitos numéricos.
        """
        # Quitar tildes (ej: 'línea' -> 'linea')
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        
        # Mapa de números hablados a dígitos
        numeros = {
            "cero": "0", "uno": "1", "dos": "2", "tres": "3", "cuatro": "4",
            "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9"
        }
        
        palabras = texto.split()
        for i in range(len(palabras)):
            if palabras[i] in numeros:
                palabras[i] = numeros[palabras[i]]
                
        return " ".join(palabras)

    def ExclusiveListening(self, word_vector: list[str]) -> Optional[str]:
        print(f"\n[ExclusiveListening] Opciones permitidas: {word_vector}")
        
        accumulated_content = []
        pending_word = ""
        last_word = ""
        
        # Todas las palabras que el sistema puede entender en este modo
        valid_tokens = ["cancelar", "enter", "enviar"] + word_vector

        while True:
            phrase = self._voice_model.escuchar_una_palabra()
            if not phrase:
                continue
            
            # Limpiamos la frase (tildes y números a dígitos)
            phrase = self._normalizar_texto(phrase)
            words = phrase.split()
            
            # Procesamos las palabras extrayendo comandos válidos
            i = 0
            while i < len(words):
                token_procesar = None
                
                # Chequeamos si las próximas dos palabras forman un comando (ej: "linea fina")
                if i < len(words) - 1:
                    bi_word = words[i] + " " + words[i+1]
                    if bi_word in valid_tokens:
                        token_procesar = bi_word
                        i += 2
                
                # Si no formaron un comando de 2 palabras, probamos con 1 sola
                if not token_procesar:
                    uni_word = words[i]
                    if uni_word in valid_tokens:
                        token_procesar = uni_word
                    else:
                        print(f"[ExclusiveListening] Palabra '{uni_word}' fuera de vector. Ignorada.")
                    i += 1
                
                # Si encontramos un token válido, le aplicamos la lógica
                if token_procesar:
                    print(f"-> Procesando válido: '{token_procesar}'")
                    
                    if token_procesar == "cancelar":
                        print("[ExclusiveListening] Comando cancelado.")
                        return None
                    
                    if token_procesar == "enviar":
                        if pending_word:
                            accumulated_content.append(pending_word)
                        result = "".join(accumulated_content)
                        print(f"[ExclusiveListening] Enviando resultado final: '{result}'")
                        return result

                    if token_procesar == "enter":
                        if pending_word:
                            accumulated_content.append(pending_word)
                            pending_word = ""
                        print(f"[ExclusiveListening] Acumulado hasta ahora: '{''.join(accumulated_content)}'")
                        continue

                    # Si es una palabra del vector
                    if token_procesar in word_vector:
                        if token_procesar != last_word:
                            pending_word = token_procesar
                            last_word = token_procesar
                            print(f"[ExclusiveListening] '{token_procesar}' validada. (Diga Enter para confirmar)")
                        else:
                            print(f"[ExclusiveListening] Duplicado '{token_procesar}' ignorado.")

    def SystematicFill(self):
        pass

    def PrintTest(self, vector_index: int) -> None:
        if vector_index >= len(self._tuple1):
            return

        selected_vector = self._tuple1[vector_index]
        print(f"\n--- INICIANDO PRINT TEST (Vector {vector_index}) ---")
        
        # w=Commando().EscuchaExclusiva(0)
        w = self.ExclusiveListening(selected_vector)
        
        # El contenido de w se imprime
        if w is not None:
            print(f"\n>>> RESULTADO FINAL: '{w}'")
        else:
            print("\n>>> RESULTADO: null (Cancelado)")
