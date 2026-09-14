"""Spoken-word aliases: Spanish/Portuguese -> dictionary keys (English)."""

from __future__ import annotations

from typing import Any

ALIASES_ES: dict[str, dict[str, str]] = {
    "DAVCore": {
        "archivo": "file",
        "fichero": "file",
        "editar": "edit",
        "edicion": "edit",
        "documento": "doc",
        "imprimir": "print",
        "impresion": "print",
        "actualizar": "refresh",
        "captura": "screenshot",
        "preferencias": "preferences",
        "configuracion": "preferences",
        "ajustes": "preferences",
        "opciones": "preferences",
    },
    "file": {
        "nuevo": "new",
        "nueva": "new",
        "abrir": "open",
        "guardar": "save",
        "cerrar": "close",
        "guardar como": "saveas",
    },
    "edit": {
        "deshacer": "undo",
        "rehacer": "redo",
        "copiar": "copy",
        "cortar": "cut",
        "pegar": "paste",
        "eliminar": "delete",
        "borrar": "delete",
        "seleccionar todo": "selectall",
    },
    "doc": {
        "deshacer": "undo",
        "rehacer": "redo",
    },
}

ALIASES_PT: dict[str, dict[str, str]] = {
    "DAVCore": {
        "arquivo": "file",
        "editar": "edit",
        "documento": "doc",
        "imprimir": "print",
        "atualizar": "refresh",
        "captura": "screenshot",
        "preferencias": "preferences",
        "configuracoes": "preferences",
        "ajustes": "preferences",
    },
    "file": {
        "novo": "new",
        "nova": "new",
        "abrir": "open",
        "salvar": "save",
        "fechar": "close",
        "salvar como": "saveas",
    },
    "edit": {
        "desfazer": "undo",
        "refazer": "redo",
        "copiar": "copy",
        "cortar": "cut",
        "colar": "paste",
        "excluir": "delete",
        "selecionar tudo": "selectall",
    },
    "doc": {
        "desfazer": "undo",
        "refazer": "redo",
    },
}


def _apply_to_node(node: Any, table: dict[str, dict[str, str]]) -> None:
    from PruebaIntegracion.core.ContextNode import NodoContexto

    for spoken, real in table.get(node.nombre, {}).items():
        node.agregar_traduccion(spoken, real)
    for child in node.elementos.values():
        if isinstance(child, NodoContexto):
            _apply_to_node(child, table)


def apply_voice_aliases(raiz: Any, language: str) -> None:
    if language == "pt":
        _apply_to_node(raiz, ALIASES_PT)
    elif language in ("es",):
        _apply_to_node(raiz, ALIASES_ES)
