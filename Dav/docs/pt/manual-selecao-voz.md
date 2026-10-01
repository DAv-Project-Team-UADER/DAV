# Rotas de voz — Selection e criação de objetos

Guia para testar por voz o módulo `Selection` e o circuito de `CreateObjects`.
Frases verificadas contra os dicionários de `Dav/dic/`.

---

## Rota A — Criar objetos (dispara CreateObjects)

Exercita o `CreateObjects` de `Dav/scr/selection/`, porque cada primitiva de
`creation.py` o invoca ao terminar.

| Passo | Dizer | Contexto |
|---|---|---|
| 1 | **"banco de trabajo"** (banco de trabalho) | `workbench` |
| 2 | **"borrador"** (rascunho) | `workbench > draft` |
| 3 | **"creacion"** (criação) | `draft > creation` |
| 4 | **"rectangulo"** (retângulo) | executa → `CreateObjects(...).Execute()` |

Outras primitivas do passo 4: **"punto"**, **"poligono"**, **"cuadrilatero"**,
**"dibujar rectangulo"**, **"marcar punto"**, **"dibujar poligono"**.

Cada uma chama `CreateObjects(ObjectName=..., Is3D=False).Execute()`
(`creation.py:31,38,45`), que é o caminho que passa pelo `Tagger`.

Sinônimos do passo 3: creacion · creación · crear · crear objeto · primitivas.

---

## Rota B — Navegar pela seleção

| Passo | Dizer | Executa |
|---|---|---|
| 1 | **"seleccion"** (seleção) | entra em `selection` |
| 2 | **"siguiente"** (seguinte) | `SelectNext()` |
| 3 | **"anterior"** | `SelectPrevious()` |
| 4 | **"todos"** | `SelectAll()` |
| 5 | **"nada"** | `DeselectAll()` |

Sinônimos do passo 1: seleccion · selección · seleccionar ·
seleccion de objetos · objetos.

Dentro de `selection` (já existiam em `Selection/TraduceToEs.py`):

- **next** — avanzar · otro · otra · pasar · siguiente · siguiente objeto ·
  objeto siguiente · siguiente elemento · seleccionar siguiente
- **previous** — retroceder · volver · anterior · anterior objeto ·
  objeto anterior · seleccionar anterior
- **selectall** — todos · todo · seleccionar todos · seleccionar todo ·
  seleccionar todos los objetos
- **deselectall** — nada · ninguno · ninguna · quitar · quitar todos ·
  desmarcar · desmarcar todo

Outras folhas do módulo: `current` (objeto atual) e `count` (quantos há).

---

## Rota C — Apagar, buscar, pintar e dar material

Além de percorrer a seleção, o módulo apaga, busca por nome e muda o aspecto do
que está selecionado, sem diálogos nativos (tudo se escolhe por voz):

| Para | Dizer | O que faz |
|---|---|---|
| Apagar o objeto escolhido | **"borrar"** · "borrar objeto" · "eliminar" · "suprimir" | Primeiro **"siguiente"/"anterior"** até o objeto e depois **"borrar"** |
| Buscar um objeto pelo nome | **"buscar por deletreo"** · "deletrear" · "buscar objeto" | Soletra-se o nome e seleciona-se o mais parecido |
| Pintar | **"pintar objeto"** · "colorear objeto" · "cambiar color" · "poner color" | Lista curta de cores (rojo, naranja, amarillo, verde, celeste, azul, violeta, rosa, marrón, negro, blanco, gris — vermelho, laranja, amarelo, verde, azul-claro, azul, violeta, rosa, marrom, preto, branco, cinza) |
| Dar material | **"material de objeto"** · "poner material" · "elegir material" | Materiais da biblioteca do FreeCAD (aluminio, acero, inoxidable, hierro, cobre, latón, bronce, titanio, oro, plata, PLA, ABS, plástico, acrílico, vidrio, madera — alumínio, aço, inoxidável, ferro, cobre, latão, bronze, titânio, ouro, prata, PLA, ABS, plástico, acrílico, vidro, madeira); só são oferecidos os que a instalação tiver |

- A cor e o material são aplicados ao que estiver **selecionado**; se não houver
  nada, escolhe-se antes com **"siguiente"** ou **"buscar por deletreo"**.
- Na caixa de cores e de materiais, **"arriba"** e **"abajo"** movem a seleção,
  **"okey"** a confirma e **"cancelar"** sai sem mudar nada.
- **"borrar"** remove o objeto sem pedir confirmação à parte; para apagar com
  confirmação por voz, usar os comandos globais de correção
  ("borrar objeto", "borrar último", "borrar rotos"; veja o manual PDF).

Código: `Dav/dic/Selection/selection.py` e `_aspecto.py`.

---

## Navegação geral

Definidos em `Dav/dic/NavCommands/TraduceToEs.py`, servem em qualquer nível:

| Para | Dizer |
|---|---|
| Subir um nível | **"subir"** · "atrás" · "salir" · "regresar" |
| Ver onde você está | **"contexto"** · "dónde estoy" · "qué puedo decir" |
| Confirmar | **"aceptar"** · "ok" · "confirmar" · "enviar" |
| Cancelar | **"cancelar"** |

Se você se perder, **"contexto"** lista o que pode ser dito nesse ponto.

---

## Teste direto pelo console Python

Sem passar por voz, para isolar se um problema é do motor ou do dicionário:

```python
import sys
sys.path.insert(0, r"C:\Users\Jose\Desktop\j\DAV\Dav\scr\selection")

from object_selection import ObjectSelection
sel = ObjectSelection()
sel.SelectAll()
sel.SelectNext()
print(sel.GetCurrentObject())
```

Circuito de criação + etiquetagem:

```python
import FreeCAD as App
from createobjects import CreateObjects

doc = App.ActiveDocument
CreateObjects(ObjectName=doc.ActiveObject.Name, Is3D=False).Execute()
```

---

## Traduções que foram adicionadas para isto

As funções já existiam; faltavam as frases de entrada, sem as quais o submenu é
inalcançável por voz mesmo que o dicionário funcione (o caso que descreve
`pendientes-dav.md` §4).

**`Dav/dic/TraduceToEs.py`** — `base.py` registrava `"selection": selection`, mas
a tradução raiz não o mencionava: o módulo inteiro não tinha porta de entrada.
Foram adicionados o import e seis frases.

**`Dav/dic/Workbench/DraftWork/TraduceToEs.py`** — dos 14 submenus de
`DraftWork.py` só 11 estavam traduzidos. Faltavam `creation`, `drafting` e
`modification`.

> Ao adicioná-las, cuidado para não sobrescrever chaves existentes: `'modificar'`
> já apontava para `draft['modify']`, então `modification` ficou como
> `'modificaciones'`. Uma chave repetida não dá erro — a última vence, em silêncio.

Ambas as correções já estão replicadas em `TraduceToEn.py` e `TraduceToPT.py`
(raiz e `Workbench/DraftWork/`).
