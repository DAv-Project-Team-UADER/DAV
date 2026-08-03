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
from __future__ import annotations

from typing import Optional, List, Dict, Any

from PruebaIntegracion.core.Command import Command
from PruebaIntegracion.core.Language import Language
from PruebaIntegracion.core.Navigator import Navigator
from PruebaIntegracion.core.ContextNode import ContextNode


class VoiceExplorer:
    """Orchestrates the voice loop: navigation, parameter collection, and execution."""

    def __init__(self, voice_model, navigator: Navigator, command: Optional[Command] = None, debug: bool = False):
        self.voice_model = voice_model
        self.navigator = navigator
        self.debug = debug
        self.command = command or Command(voice_model, debug=debug)
        self.parameter_mode = False
        self.pending_function = None
        self.collected_parameters: List[Any] = []

    def _log(self, message: str) -> None:
        if self.debug:
            print(f"[VoiceExplorer] {message}")

    def _get_real_name_ascending(self, word: str) -> str:
        self._log(f"resolving ascending translation for '{word}'")
        node = self.navigator.current_context
        w = word
        while node is not None:
            real = node.get_real_name(w)
            if real:
                self._log(f"translation found in {node.name}: {w} -> {real}")
                return real
            node = node.parent
        self._log(f"no translation found for '{word}'")
        return word

    def _navigation_vocabulary(self) -> List[str]:
        # Combines real names (keys) and spoken translations from the current context
        vocab = set()
        language = self._get_active_language()
        node = self.navigator.current_context
        while node is not None:
            for spoken in node.translations.keys():
                vocab.add(spoken)
            for key in node.elements.keys():
                vocab.add(key)
            node = node.parent
        vocab.update(language.commands)
        vocabulary = list(vocab)
        self._log(f"active vocabulary ({len(vocabulary)}): {sorted(vocabulary)}")
        return vocabulary

    def _get_active_language(self) -> Language:
        language = getattr(self.command, "language", None)
        if isinstance(language, Language):
            return language
        return Language()

    def _parse_number(self, phrase: str) -> Optional[float]:
        """Attempts to convert a spoken phrase to a number (supports 'one', 'two', 'comma', 'point')."""
        if not phrase:
            return None
        language = self._get_active_language()
        text = phrase.lower()
        number_map = language.number_map
        number_map.update({'one': '1', 'a': '1', 'ten': '10'})  # adapted for English; original: un, una, diez
        parts = []
        for w in text.replace(',', ' ').split():
            if w in number_map:
                parts.append(number_map[w])
            elif w in ('point', 'comma'):
                parts.append('.')
            else:
                # try direct numeric
                try:
                    float(w)
                    parts.append(w)
                except Exception:
                    # unknown word -> ignore
                    pass
        if not parts:
            return None
        s = ''.join(parts)
        try:
            return float(s)
        except Exception:
            return None

    def start_parameters(self, wrapper):
        self._log(f"entering parameter mode for '{getattr(wrapper, 'name', wrapper)}'")
        self.parameter_mode = True
        self.pending_function = wrapper
        self.collected_parameters = []

    def process_parameters(self, max_iterations: int = 5) -> bool:
        """Collects parameters according to the pending function's ParamSpec.
        Returns True if collection and execution were successful.
        """
        if not self.pending_function:
            self._log("process_parameters called without a pending function")
            return False
        specs = getattr(self.pending_function, 'param_specs', ())
        self._log(f"expecting {len(specs)} parameters")
        for spec in specs:
            # Request parameter via voice using Command for filtering
            prompt = f"Say the value for {spec.name} (or 'cancel' to abort)"
            print(prompt)
            self._log(f"listening for parameter '{spec.name}'")
            
            # Vocabulary for parameters: numbers, cancel, send, point, comma
            language = self._get_active_language()
            param_vocab = language.digits + language.commands + ["point", "comma"]
            
            # Use Command.exclusive_listen to filter against vocabulary
            phrase = self.command.exclusive_listen(param_vocab)
            
            # Handle cancellation
            if phrase is False:
                print("Cancellation received during parameter collection.")
                self._log("cancellation during parameter collection")
                return False
            
            self._log(f"phrase received for '{spec.name}': {phrase!r}")
            val = None
            if spec.param_type in (int, float):
                num = self._parse_number(phrase)
                if num is None:
                    print(f"Could not interpret a valid number for {spec.name}.")
                    self._log(f"numeric parsing failed for '{spec.name}' with phrase {phrase!r}")
                    return False
                if spec.param_type is int:
                    val = int(num)
                else:
                    val = float(num)
            else:
                # For strings or complex types, take the phrase as is
                val = phrase
            try:
                spec.validate(val, spec.name)
            except Exception as e:
                print(f"Validation failed for {spec.name}: {e}")
                self._log(f"validation failed for '{spec.name}': {e}")
                return False
            self.collected_parameters.append(val)
            self._log(f"parameter '{spec.name}' collected as {val!r}")

        # If we reach here, attempt execution
        try:
            self._log(f"executing '{self.pending_function.name}' with parameters {self.collected_parameters}")
            result = self.navigator.call(self.pending_function.name, *self.collected_parameters, context_keys=[self.navigator.current_context.name])
            print(f"Successful execution: {result}")
            self._log(f"successful execution: {result!r}")
            return True
        except Exception as e:
            print(f"Error executing function: {e}")
            self._log(f"error executing function: {e}")
            return False
        finally:
            self.parameter_mode = False
            self.pending_function = None
            self.collected_parameters = []
            self._log("exiting parameter mode")

    def command_loop(self, max_iterations: Optional[int] = None) -> None:
        """Main loop. For tests, `max_iterations` limits iterations.
        """
        it = 0
        self._log(f"starting command_loop max_iterations={max_iterations}")
        while True:
            if max_iterations is not None and it >= max_iterations:
                self._log("iteration limit reached")
                break
            it += 1
            self._log(f"iteration {it} in context {self.navigator.current_context.name}")
            vocab = self._navigation_vocabulary()
            self._log("invoking Command.exclusive_listen")
            token = self.command.exclusive_listen(vocab)
            self._log(f"Command.exclusive_listen returned {token!r}")
            if token is False:
                self._log("cancellation received; exiting loop")
                print("Cancelled by user.")
                break
            if token is None:
                # silence
                self._log("null token; continuing")
                continue
            print(f"Heard token: {token}")
            real_name = self._get_real_name_ascending(token)
            # try to find function
            found = self.navigator.find_function_ascending(real_name)
            if found:
                node, wrapper = found
                print(f"Function detected: {real_name} in node {node.name}")
                self._log(f"function found in {node.name}; starting parameter capture")
                self.start_parameters(wrapper)
                self.process_parameters()
                continue
            # if not a function, try navigating to subcontext
            child = self.navigator.current_context.elements.get(real_name)
            if isinstance(child, ContextNode):
                self.navigator.set_context(child)
                print(f"Context changed to: {child.name}")
                self._log(f"context changed to {child.name}")
                continue
            print(f"Command '{token}' not recognized in this context.")
            self._log(f"unrecognized command: {token!r}")
