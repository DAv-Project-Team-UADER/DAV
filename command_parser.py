import os
import re
import unicodedata
from pathlib import Path

def fold_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))

def parse_phrase_pattern(pattern_str: str) -> list:
    """
    Convierte una expresión como '"Línea desde " + número + número' 
    en una lista de expresiones regulares.
    """
    variants = pattern_str.split('/')
    regexes = []
    for var in variants:
        var = var.strip()
        if not var:
            continue
        parts = var.split('+')
        regex_str = r"^"
        for p in parts:
            p = p.strip()
            # Eliminar posibles notas entre paréntesis al final (ej. "string255 (nombre de archivo)")
            p = re.sub(r'\(.*?\)', '', p).strip()
            
            if p.startswith('"') and p.endswith('"'):
                literal = p[1:-1].lower().strip()
                literal = fold_accents(literal)
                # Escapar y permitir espacios flexibles
                regex_str += r"\s*" + re.escape(literal) + r"\s*"
            else:
                p_lower = fold_accents(p.lower())
                if 'numero' in p_lower:
                    # Captura números (incluyendo decimales)
                    regex_str += r"\s*(\d+(?:[.,]\d+)?)\s*"
                elif 'objeto' in p_lower or 'string' in p_lower:
                    # Captura una o más palabras
                    regex_str += r"\s*(\S+)\s*"
                elif 'grupo de puntos' in p_lower:
                    regex_str += r"\s*(.+)\s*"
                else:
                    # Si no está entre comillas pero tampoco es un token conocido, lo tomamos literal
                    literal = fold_accents(p)
                    regex_str += r"\s*" + re.escape(literal) + r"\s*"
        regex_str += r"$"
        
        # Limpiar espacios redundantes en la regex generada
        regex_str = regex_str.replace(r"\s*\s*", r"\s*")
        regexes.append(regex_str)
    return regexes

def inject_args_to_script(script: str, args: list) -> str:
    """
    Intenta inyectar los argumentos capturados en el script.
    Heurística 1: Reemplazar variables simbólicas comunes (OBJ, number, vector[], etc.)
    Heurística 2: Si hay una invocación de ejemplo con números, reemplazar esos números.
    """
    if not args:
        return script
    
    lines = script.split('\n')
    args_to_inject = list(args) # Copia
    
    # Intentar Heurística 1: reemplazar placeholders textuales
    placeholders = [r'\bnumber\b', r'\bOBJ\b', r'vector\[\]', r'\bstring255\b', r'\bobjeto\b']
    
    script_modified = False
    for i, line in enumerate(lines):
        for ph in placeholders:
            while re.search(ph, lines[i]) and args_to_inject:
                arg = args_to_inject.pop(0)
                # Si es un número, inyectar como número. Si es string, inyectar con comillas
                if isinstance(arg, str) and not arg.replace('.', '', 1).isdigit():
                    arg_str = f'"{arg}"'
                else:
                    arg_str = str(arg)
                lines[i] = re.sub(ph, arg_str, lines[i], count=1)
                script_modified = True

    if script_modified:
        return '\n'.join(lines)
    
    # Intentar Heurística 2: reemplazar números en la última línea no vacía (invocación de ejemplo)
    args_to_inject = list(args)
    for i in range(len(lines)-1, -1, -1):
        line = lines[i]
        if line.strip() and not line.strip().startswith('#') and 'def ' not in line:
            # Usar una función de reemplazo para no reemplazar el mismo número múltiple veces
            def repl(m):
                if args_to_inject:
                    return str(args_to_inject.pop(0))
                return m.group(0)
            lines[i] = re.sub(r'\d+(?:[.,]\d+)?', repl, lines[i])
            break

    return '\n'.join(lines)


def parse_commands_from_directories(directories: list) -> list:
    """
    Lee todos los archivos .txt de los directorios y devuelve una lista de reglas dinámicas.
    Cada regla es un dict: {'name': str, 'script_template': str, 'regexes': list[re.Pattern]}
    """
    rules = []
    
    for d in directories:
        dir_path = Path(d)
        if not dir_path.is_dir():
            continue
            
        for file_path in dir_path.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Nombre
                name_match = re.search(r'<Nombre de la característica>\s*(.*?)\s*<', content, re.DOTALL | re.IGNORECASE)
                name = name_match.group(1).strip() if name_match else file_path.stem
                
                # Script
                script_match = re.search(r'<(?:Script|scipt nativo para invocarlo o script completo)>\s*(.*?)\s*<', content, re.DOTALL | re.IGNORECASE)
                script_template = script_match.group(1).strip() if script_match else ""
                
                # Palabras sugeridas
                phrases_match = re.search(r'<Palabras sugeridas para los comandos por voz>\s*(.*?)\s*(?:<|$)', content, re.DOTALL | re.IGNORECASE)
                phrases_raw = phrases_match.group(1).strip() if phrases_match else ""
                
                if not phrases_raw or not script_template:
                    continue
                
                regex_strings = parse_phrase_pattern(phrases_raw)
                compiled_regexes = [re.compile(r) for r in regex_strings]
                
                rules.append({
                    'name': name,
                    'script_template': script_template,
                    'regexes': compiled_regexes,
                    'source_file': file_path.name
                })
                
            except Exception as e:
                print(f"Error parseando {file_path}: {e}")
                
    return rules

