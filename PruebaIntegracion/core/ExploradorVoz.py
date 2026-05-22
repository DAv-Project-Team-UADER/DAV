from __future__ import annotations

from typing import Optional, List, Dict, Any

from PruebaIntegracion.core.Comando import Command
from PruebaIntegracion.core.Idioma import Idioma
from PruebaIntegracion.core.Navegador import Navegador
from PruebaIntegracion.core.NodoContexto import NodoContexto
        

class ExploradorVoz:
    """Orquesta el bucle de voz: navegación, recolección de parámetros y ejecución."""

    def __init__(self, voice_model, navegador: Navegador, command: Optional[Command] = None, debug: bool = False):
        self.voice_model = voice_model
        self.navegador = navegador
        self.debug = debug
        self.command = command or Command(voice_model, debug=debug)
        self.modo_parametros = False
        self.funcion_pendiente = None
        self.parametros_recolectados: List[Any] = []

    def _log(self, mensaje: str) -> None:
        if self.debug:
            print(f"[ExploradorVoz] {mensaje}")

    def _obtener_nombre_real_ascendente(self, palabra: str) -> str:
        self._log(f"resolviendo traduccion ascendente para '{palabra}'")
        nodo = self.navegador.contexto_actual
        p = palabra
        while nodo is not None:
            real = nodo.obtener_nombre_real(p)
            if real:
                self._log(f"traduccion encontrada en {nodo.nombre}: {p} -> {real}")
                return real
            nodo = nodo.parent
        self._log(f"no se encontro traduccion para '{palabra}'")
        return palabra

    def _vocabulario_navegacion(self) -> List[str]:
        # Combina nombres reales (claves) y traducciones habladas del contexto actual
        vocab = set()
        idioma = self._obtener_idioma_activo()
        nodo = self.navegador.contexto_actual
        while nodo is not None:
            for spoken in nodo.traducciones.keys():
                vocab.add(spoken)
            for key in nodo.elementos.keys():
                vocab.add(key)
            nodo = nodo.parent
        vocab.update(idioma.lista_comandos)
        vocabulario = list(vocab)
        self._log(f"vocabulario activo ({len(vocabulario)}): {sorted(vocabulario)}")
        return vocabulario

    def _obtener_idioma_activo(self) -> Idioma:
        idioma = getattr(self.command, "idioma", None)
        if isinstance(idioma, Idioma):
            return idioma
        return Idioma()

    def _parse_number(self, phrase: str) -> Optional[float]:
        """Intenta convertir una frase hablada a número (soporta 'uno', 'dos', 'coma', 'punto')."""
        if not phrase:
            return None
        idioma = self._obtener_idioma_activo()
        text = phrase.lower()
        mapa = idioma.mapa_numeros
        mapa.update({'un': '1', 'una': '1', 'diez': '10'})
        parts = []
        for w in text.replace(',', ' ').split():
            if w in mapa:
                parts.append(mapa[w])
            elif w in ('punto', 'coma'):
                parts.append('.')
            else:
                # si es numérico directo
                try:
                    float(w)
                    parts.append(w)
                except Exception:
                    # palabra desconocida -> ignorar
                    pass
        if not parts:
            return None
        s = ''.join(parts)
        try:
            return float(s)
        except Exception:
            return None

    def iniciar_parametros(self, envoltorio):
        self._log(f"entrando a modo parametros para '{getattr(envoltorio, 'nombre', envoltorio)}'")
        self.modo_parametros = True
        self.funcion_pendiente = envoltorio
        self.parametros_recolectados = []

    def procesar_parametros(self, max_iterations: int = 5) -> bool:
        """Recolecta parámetros según ParamSpec de la función pendiente.
        Retorna True si la recolección y ejecución fue exitosa.
        """
        if not self.funcion_pendiente:
            self._log("procesar_parametros invocado sin funcion pendiente")
            return False
        specs = getattr(self.funcion_pendiente, 'param_specs', ())
        self._log(f"esperando {len(specs)} parametros")
        for spec in specs:
            # Pedimos el parámetro por voz usando Command para filtrar
            prompt = f"Decí el valor para {spec.nombre} (o 'cancelar' para abortar)"
            print(prompt)
            self._log(f"escuchando parametro '{spec.nombre}'")
            
            # Vocabulario para parámetros: números, cancelar, enviar, punto, coma
            idioma = self._obtener_idioma_activo()
            vocab_parametros = idioma.lista_digitos + idioma.lista_comandos + ["punto", "coma"]
            
            # Usamos Command.exclusive_listen para filtrar contra vocabulario
            phrase = self.command.exclusive_listen(vocab_parametros)
            
            # Manejar cancelación
            if phrase is False:
                print("Cancelación recibida durante recolección de parámetros.")
                self._log("cancelacion durante recoleccion de parametros")
                return False
            
            self._log(f"frase recibida para '{spec.nombre}': {phrase!r}")
            val = None
            if spec.tipo in (int, float):
                num = self._parse_number(phrase)
                if num is None:
                    print(f"No pude interpretar un número válido para {spec.nombre}.")
                    self._log(f"fallo parseo numerico para '{spec.nombre}' con frase {phrase!r}")
                    return False
                if spec.tipo is int:
                    val = int(num)
                else:
                    val = float(num)
            else:
                # Para strings o tipos complejos, tomamos la frase tal cual
                val = phrase
            try:
                spec.validar(val, spec.nombre)
            except Exception as e:
                print(f"Validación fallida para {spec.nombre}: {e}")
                self._log(f"validacion fallida para '{spec.nombre}': {e}")
                return False
            self.parametros_recolectados.append(val)
            self._log(f"parametro '{spec.nombre}' recolectado como {val!r}")

        # Si llegamos aquí, intentamos ejecutar
        try:
            self._log(f"ejecutando '{self.funcion_pendiente.nombre}' con parametros {self.parametros_recolectados}")
            resultado = self.navegador.llamar(self.funcion_pendiente.nombre, *self.parametros_recolectados, context_keys=[self.navegador.contexto_actual.nombre])
            print(f"Ejecución exitosa: {resultado}")
            self._log(f"ejecucion exitosa: {resultado!r}")
            return True
        except Exception as e:
            print(f"Error al ejecutar la función: {e}")
            self._log(f"error al ejecutar funcion: {e}")
            return False
        finally:
            self.modo_parametros = False
            self.funcion_pendiente = None
            self.parametros_recolectados = []
            self._log("salida de modo parametros")

    def bucle_comando(self, max_iterations: Optional[int] = None) -> None:
        """Bucle principal. Para pruebas, `max_iterations` limita iteraciones.
        """
        it = 0
        self._log(f"iniciando bucle_comando max_iterations={max_iterations}")
        while True:
            if max_iterations is not None and it >= max_iterations:
                self._log("se alcanzo el limite de iteraciones")
                break
            it += 1
            self._log(f"iteracion {it} en contexto {self.navegador.contexto_actual.nombre}")
            vocab = self._vocabulario_navegacion()
            self._log("invocando Command.exclusive_listen")
            token = self.command.exclusive_listen(vocab)
            self._log(f"Command.exclusive_listen devolvio {token!r}")
            if token is False:
                self._log("cancelacion recibida; saliendo del bucle")
                print("Cancelado por el usuario.")
                break
            if token is None:
                # silencio
                self._log("token nulo; continuando")
                continue
            print(f"Token escuchado: {token}")
            nombre_real = self._obtener_nombre_real_ascendente(token)
            # intentar encontrar funcion
            encontrado = self.navegador.buscar_funcion_ascendente(nombre_real)
            if encontrado:
                nodo, envoltorio = encontrado
                print(f"Funcion detectada: {nombre_real} en nodo {nodo.nombre}")
                self._log(f"funcion encontrada en {nodo.nombre}; iniciando captura de parametros")
                self.iniciar_parametros(envoltorio)
                self.procesar_parametros()
                continue
            # si no es funcion, intentar navegar a subcontexto
            hijo = self.navegador.contexto_actual.elementos.get(nombre_real)
            if isinstance(hijo, NodoContexto):
                self.navegador.establecer_contexto(hijo)
                print(f"Cambiado contexto a: {hijo.nombre}")
                self._log(f"cambio de contexto a {hijo.nombre}")
                continue
            print(f"Comando '{token}' no reconocido en este contexto.")
            self._log(f"comando no reconocido: {token!r}")
