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
from a dictionary defined inside a .py file, without constructing the dict in memory.
Supports both literal dictionaries and dictionaries with imports/variable references.
"""
import os
import ast


class Keychain:
    """
    Retrieves top-level keys, icon file names, or raw literal values from a
    dictionary defined inside a `.py` file, without constructing the dict in memory.

    Supports two parsing modes:
    1. Text scanning (GetKeys, GetValues) - For files with literal dictionaries
    2. AST parsing (GetKeysFromCode) - For files with imports and variable references
    """

    def __init__(self, FilePath: str):
        """
        Initializes the Keychain with the path to a .py file containing a dictionary.

        Args:
            FilePath: Path to the .py file containing the dictionary definition.
        """
        self.FilePath = FilePath
        # Read the whole file once to avoid repeated I/O operations
        with open(self.FilePath, 'r', encoding='utf-8') as file_handle:
            self._Content = file_handle.read()

    # =========================================================================
    # Method 1: Text scanning (for literal dictionaries with string/number values)
    # =========================================================================

    def GetKeys(self):
        """
        Extracts top-level keys from a literal dictionary by scanning the text.
        Does NOT execute code. Works only when dictionary values are literals
        (strings, numbers, booleans, nested dicts/lists).

        Returns:
            list[str]: List of top-level key names.

        Raises:
            ValueError: If no opening brace '{' is found in the file content.
        """
        start_idx = self._Content.find('{')
        if start_idx == -1:
            raise ValueError("No opening brace '{' found in file content.")

        keys = []
        depth = 0          # Brace nesting depth (0 = outside main dict)
        i = start_idx      # Current position in content

        while i < len(self._Content):
            char = self._Content[i]

            # Track brace depth
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:          # Outermost dict closed, stop parsing
                    break

            # Only look for keys when exactly one level deep
            elif depth == 1:
                # Skip whitespace and commas
                if char in ' \t\r\n,':
                    i += 1
                    continue

                # Detect string keys (single or double quotes)
                if char == '"' or char == "'":
                    quote_char = char
                    key_start = i + 1
                    i += 1

                    # Find the matching closing quote (handling escapes)
                    while i < len(self._Content):
                        if self._Content[i] == '\\':
                            i += 2          # Skip escaped character
                            continue
                        if self._Content[i] == quote_char:
                            break
                        i += 1

                    key_name = self._Content[key_start:i]

                    # Look ahead for a colon (key-value separator)
                    j = i + 1
                    while j < len(self._Content) and self._Content[j] in ' \t\r\n':
                        j += 1

                    if j < len(self._Content) and self._Content[j] == ':':
                        keys.append(key_name)

            i += 1

        return keys

    def GetIcons(self, base_dir=None):
        """
        Appends '.svg' extension to each top-level key and optionally filters
        out icons that do not exist on disk.

        Args:
            base_dir (str, optional): Directory to check for icon existence.
                                     If provided, only icons that exist as files
                                     in this directory are returned. If None,
                                     no existence check is performed.

        Returns:
            list[str]: Icon file names (e.g., ['house.svg', 'car.svg']), filtered
                      if base_dir is given.
        """
        all_icons = [f"{key}.svg" for key in self.GetKeys()]
        if base_dir is None:
            return all_icons

        # Filter only those icons that actually exist in base_dir
        existing = []
        for icon in all_icons:
            full_path = os.path.join(base_dir, icon)
            if os.path.isfile(full_path):
                existing.append(icon)
        return existing

    def GetValues(self):
        """
        Extracts raw literal value strings for each top-level key without
        executing Python code. Values are returned exactly as they appear
        in the file (strings, numbers, nested structures, etc.).

        Returns:
            list[str]: List of raw value substrings.
        """
        start_idx = self._Content.find('{')
        if start_idx == -1:
            raise ValueError("No opening brace '{' found in file content.")

        values = []
        depth = 0
        i = start_idx

        while i < len(self._Content):
            char = self._Content[i]

            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    break
            elif depth == 1:
                if char in ' \t\r\n,':
                    i += 1
                    continue

                # Identify a key string
                if char == '"' or char == "'":
                    quote_char = char
                    key_start = i + 1
                    i += 1

                    while i < len(self._Content):
                        if self._Content[i] == '\\':
                            i += 2
                            continue
                        if self._Content[i] == quote_char:
                            break
                        i += 1

                    # Verify colon after key
                    j = i + 1
                    while j < len(self._Content) and self._Content[j] in ' \t\r\n':
                        j += 1

                    if j < len(self._Content) and self._Content[j] == ':':
                        # Skip whitespace after colon
                        k = j + 1
                        while k < len(self._Content) and self._Content[k] in ' \t\r\n':
                            k += 1

                        value_start = k
                        value_depth = 1
                        in_string = False
                        string_char = ''

                        # Walk forward until value ends (comma or closing brace at depth 1)
                        while k < len(self._Content):
                            c = self._Content[k]

                            # Handle string escaping
                            if in_string:
                                if c == '\\':
                                    k += 2
                                    continue
                                if c == string_char:
                                    in_string = False
                                k += 1
                                continue

                            # Enter a string literal
                            if c == '"' or c == "'":
                                in_string = True
                                string_char = c
                                k += 1
                                continue

                            # Track nested braces and brackets
                            if c == '{' or c == '[':
                                value_depth += 1
                            elif c == '}' or c == ']':
                                value_depth -= 1
                                if value_depth == 1 and c == '}':
                                    break
                            elif c == ',' and value_depth == 1:
                                break

                            k += 1

                        literal_value = self._Content[value_start:k].rstrip()
                        values.append(literal_value)
                        i = k
                        continue

            i += 1

        return values

    # =========================================================================
    # Method 2: AST parsing (for files with imports and variable references)
    # =========================================================================

    def GetKeysFromCode(self):
        """
        Extracts top-level dictionary keys from a Python file that may contain
        import statements and variable references as dictionary values.

        Uses Python's AST (Abstract Syntax Tree) module to parse the file
        without executing any code. This is completely safe and lightweight:
        - No code execution (safe against malicious files)
        - Minimal RAM usage (only the AST structure, not real objects)
        - Works with any value type (variables, function calls, nested dicts, etc.)

        Returns:
            list[str]: List of key names found in the first dictionary definition.

        Raises:
            ValueError: If the file contains a syntax error.
        """
        try:
            # Parse file content into an Abstract Syntax Tree (no execution)
            tree = ast.parse(self._Content)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in file '{self.FilePath}': {e}")

        # Walk through all nodes in the AST looking for dictionary definitions
        for node in ast.walk(tree):
            # Found a dictionary literal in the code
            if isinstance(node, ast.Dict):
                keys = []
                for key_node in node.keys:
                    # Extract the key if it's a string constant
                    if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                        keys.append(key_node.value)
                return keys

        # No dictionary definition found in the file
        return []

    # =========================================================================
    # Smart method: tries both approaches automatically
    # =========================================================================

    def GetAllKeys(self):
        """
        Tries to extract keys using both methods automatically.
        First attempts text scanning (fast, for literal dictionaries).
        If no keys found, falls back to AST parsing (for files with imports).

        Returns:
            list[str]: List of top-level key names.
        """
        # Try text scanning first (fast path for literal dictionaries)
        keys = self.GetKeys()

        # If text scanning found nothing, try AST parsing
        if not keys:
            keys = self.GetKeysFromCode()

        return keys