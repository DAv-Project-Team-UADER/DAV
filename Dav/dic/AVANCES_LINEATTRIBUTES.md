# Avances — Módulo LineAttributes

> Revisado: 2026-06-03 · Reconfirmado contra código 2026-06-25
>
> Verificado 2026-06-25: `LineAttributes.py` usa `.update(attributes)` + `'help': ayuda`.
> La doc coincide con el código; sin cambios.

---

## Estructura de archivos

```
LineAttributes/
├── LineAttributes.py       ← raíz
├── ayuda.py
└── attributes/
    ├── attributes.py
    └── ayuda.py
```

---

## Cobertura de tickets (2 tickets LineAttributes)

### ✅ Cubiertos correctamente

| Ticket                                 | Clave      | Archivo                     |
|----------------------------------------|------------|-----------------------------|
| `Ticket_ExtensionSelectLineAttributes` | `'select'` | `attributes/attributes.py`  |
| `Ticket_ExtensionChangeLineAttributes` | `'change'` | `attributes/attributes.py`  |

Comando ejecutado: `Gui.runCommand('TechDraw_Extension[Select|Change]LineAttributes', 0)`

Cobertura: **2/2 tickets** ✅

---

## Bugs corregidos (2026-06-03)

| # | Archivo             | Problema                                                                       | Corrección aplicada                                              |
|---|---------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------|
| 1 | `LineAttributes.py` | Anidaba `attributes` como valor — usuario debía decir `'attributes'` primero   | Reemplazado por `.update(attributes)` — claves aplanadas         |
| 2 | `ayuda.py` (raíz)   | Listaba `'attributes'` como comando (clave ya inexistente tras el fix)         | Actualizado para listar `'select'` y `'change'` directamente     |

---

## Notas

Los dos comandos corresponden al **TechDraw Workbench** (`TechDraw_Extension*`). Son herramientas de atributos de línea accesibles desde cualquier workbench, por eso tienen su propio módulo separado.

El módulo está **completo en cobertura y sin bugs estructurales**. Los comandos `'select'` y `'change'` son accesibles directamente desde el diccionario raíz.
