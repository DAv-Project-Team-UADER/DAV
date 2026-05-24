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


"""
Keychain.py
Class that retrieves top-level keys, icon file names, or raw literal values
from a dictionary defined inside a .py file, WITHOUT constructing the dict in memory.

Supports both:
- Literal dictionaries: {'key1': value1, 'key2': value2}
- dict() constructor: dict(key1=value1, key2=value2)

All parsing is done by scanning the source text (no AST, no execution).
"""

import os

class Keychain:
    """
    Extracts keys and values from a dictionary definition in a .py file
    using only text scanning. Works for both literal {} and dict() syntax.
    """

    def __init__(self, FilePath: str):
        """
        Initialize with the path to a .py file containing a dictionary.

        Args:
            FilePath: Path to the .py file.
        """
        self.FilePath = FilePath
        with open(self.FilePath, 'r', encoding='utf-8') as f:
            self._Content = f.read()

    # =====================================================================
    # Public methods
    # =====================================================================

    def GetKeys(self):
        """
        Extract top-level dictionary keys by scanning the file content.
        Automatically detects whether the dictionary uses literal {} or dict().

        Returns:
            list[str]: List of key names.

        Raises:
            ValueError: If no dictionary definition is found.
        """
        # Try literal dictionary first
        start = self._Content.find('{')
        if start != -1:
            return self._extract_keys_from_literal(start)

        # Then try dict() constructor
        start = self._Content.find('dict(')
        if start != -1:
            return self._extract_keys_from_dict_call(start)

        raise ValueError("No dictionary definition found (neither {...} nor dict(...))")

    def GetValues(self):
        """
        Extract raw literal values for each top-level key.
        Returns values exactly as they appear in the file.

        Returns:
            list[str]: List of raw value substrings.
        """
        start = self._Content.find('{')
        if start != -1:
            return self._extract_values_from_literal(start)

        start = self._Content.find('dict(')
        if start != -1:
            return self._extract_values_from_dict_call(start)

        raise ValueError("No dictionary definition found (neither {...} nor dict(...))")

    def GetIcons(self, base_dir=None):
        """
        Append '.svg' to each key and optionally filter existing files.

        Args:
            base_dir (str, optional): Directory to check for file existence.

        Returns:
            list[str]: Icon filenames (e.g., ['home.svg', 'user.svg']).
        """
        all_icons = [f"{key}.svg" for key in self.GetKeys()]
        if base_dir is None:
            return all_icons

        existing = []
        for icon in all_icons:
            full_path = os.path.join(base_dir, icon)
            if os.path.isfile(full_path):
                existing.append(icon)
        return existing

    def GetAllKeys(self):
        """
        Smart method: just returns GetKeys() (which now handles both formats).
        Kept for backward compatibility.

        Returns:
            list[str]: Top-level key names.
        """
        return self.GetKeys()

    # =====================================================================
    # Internal helpers for literal dictionary {...}
    # =====================================================================

    def _extract_keys_from_literal(self, start_idx):
        """Extract keys from a literal {...} dictionary."""
        content = self._Content
        keys = []
        depth = 0
        i = start_idx
        length = len(content)

        while i < length:
            ch = content[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
            elif depth == 1:
                if ch in ' \t\r\n,':
                    i += 1
                    continue
                if ch == '"' or ch == "'":
                    quote = ch
                    key_start = i + 1
                    i += 1
                    while i < length:
                        if content[i] == '\\':
                            i += 2
                            continue
                        if content[i] == quote:
                            break
                        i += 1
                    key_name = content[key_start:i]
                    # Look for colon
                    j = i + 1
                    while j < length and content[j] in ' \t\r\n':
                        j += 1
                    if j < length and content[j] == ':':
                        keys.append(key_name)
            i += 1
        return keys

    def _extract_values_from_literal(self, start_idx):
        """Extract raw values from a literal {...} dictionary."""
        content = self._Content
        values = []
        depth = 0
        i = start_idx
        length = len(content)

        while i < length:
            ch = content[i]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
            elif depth == 1:
                if ch in ' \t\r\n,':
                    i += 1
                    continue
                if ch == '"' or ch == "'":
                    quote = ch
                    key_start = i + 1
                    i += 1
                    while i < length:
                        if content[i] == '\\':
                            i += 2
                            continue
                        if content[i] == quote:
                            break
                        i += 1
                    # Find colon
                    j = i + 1
                    while j < length and content[j] in ' \t\r\n':
                        j += 1
                    if j < length and content[j] == ':':
                        # Skip colon and spaces
                        k = j + 1
                        while k < length and content[k] in ' \t\r\n':
                            k += 1
                        value_start = k
                        value_depth = 1
                        in_string = False
                        string_char = ''
                        while k < length:
                            c = content[k]
                            if in_string:
                                if c == '\\':
                                    k += 2
                                    continue
                                if c == string_char:
                                    in_string = False
                                k += 1
                                continue
                            if c == '"' or c == "'":
                                in_string = True
                                string_char = c
                                k += 1
                                continue
                            if c == '{' or c == '[':
                                value_depth += 1
                            elif c == '}' or c == ']':
                                value_depth -= 1
                                if value_depth == 1 and c == '}':
                                    break
                            elif c == ',' and value_depth == 1:
                                break
                            k += 1
                        raw_value = content[value_start:k].rstrip()
                        values.append(raw_value)
                        i = k
                        continue
            i += 1
        return values

    # =====================================================================
    # Internal helpers for dict(key=value, ...) constructor
    # =====================================================================

    def _extract_keys_from_dict_call(self, start_idx):
        """Extract keyword argument names from dict(key1=val1, key2=val2)."""
        content = self._Content
        keys = []
        i = start_idx + 5  # after 'dict('
        length = len(content)
        paren_depth = 1

        while i < length and paren_depth > 0:
            ch = content[i]
            if ch == '(':
                paren_depth += 1
            elif ch == ')':
                paren_depth -= 1
                if paren_depth == 0:
                    break
            elif ch == ',' and paren_depth == 1:
                pass  # separator, ignore
            elif paren_depth == 1:
                # Skip whitespace
                if ch in ' \t\r\n':
                    i += 1
                    continue
                # Look for an identifier (key) before '='
                if ch.isalpha() or ch == '_':
                    key_start = i
                    while i < length and (content[i].isalnum() or content[i] == '_'):
                        i += 1
                    key_candidate = content[key_start:i]
                    # Skip spaces until '='
                    j = i
                    while j < length and content[j] in ' \t\r\n':
                        j += 1
                    if j < length and content[j] == '=':
                        keys.append(key_candidate)
                        # Skip the value entirely (go to next comma or closing paren)
                        # We'll reuse the value-skipping logic
                        k = j + 1
                        # parse value (could be nested, strings, etc.)
                        value_depth = 0
                        in_string = False
                        string_char = ''
                        while k < length:
                            c = content[k]
                            if in_string:
                                if c == '\\':
                                    k += 2
                                    continue
                                if c == string_char:
                                    in_string = False
                                k += 1
                                continue
                            if c == '"' or c == "'":
                                in_string = True
                                string_char = c
                                k += 1
                                continue
                            if c in '([{':
                                value_depth += 1
                            elif c in ')]}':
                                value_depth -= 1
                            elif c == ',' and value_depth == 0 and paren_depth == 1:
                                break
                            elif c == ')' and value_depth == 0:
                                break
                            k += 1
                        i = k  # continue after the value
                        continue
                    else:
                        # not a key=value, just move on
                        pass
            i += 1
        return keys

    def _extract_values_from_dict_call(self, start_idx):
        """Extract raw values from dict(key1=val1, key2=val2)."""
        content = self._Content
        values = []
        i = start_idx + 5
        length = len(content)
        paren_depth = 1

        while i < length and paren_depth > 0:
            ch = content[i]
            if ch == '(':
                paren_depth += 1
            elif ch == ')':
                paren_depth -= 1
                if paren_depth == 0:
                    break
            elif ch == ',' and paren_depth == 1:
                pass
            elif paren_depth == 1:
                if ch in ' \t\r\n':
                    i += 1
                    continue
                # Find a key identifier
                if ch.isalpha() or ch == '_':
                    key_start = i
                    while i < length and (content[i].isalnum() or content[i] == '_'):
                        i += 1
                    # skip to '='
                    j = i
                    while j < length and content[j] in ' \t\r\n':
                        j += 1
                    if j < length and content[j] == '=':
                        # extract value after '='
                        k = j + 1
                        while k < length and content[k] in ' \t\r\n':
                            k += 1
                        value_start = k
                        value_depth = 0
                        in_string = False
                        string_char = ''
                        while k < length:
                            c = content[k]
                            if in_string:
                                if c == '\\':
                                    k += 2
                                    continue
                                if c == string_char:
                                    in_string = False
                                k += 1
                                continue
                            if c == '"' or c == "'":
                                in_string = True
                                string_char = c
                                k += 1
                                continue
                            if c in '([{':
                                value_depth += 1
                            elif c in ')]}':
                                value_depth -= 1
                            elif c == ',' and value_depth == 0 and paren_depth == 1:
                                break
                            elif c == ')' and value_depth == 0:
                                break
                            k += 1
                        raw_value = content[value_start:k].rstrip()
                        values.append(raw_value)
                        i = k
                        continue
                    else:
                        # not a key=value pair, skip
                        pass
            i += 1
        return values