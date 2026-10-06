# Regenerar o manual do usuário (PDF)

`Manual_Usuario.pdf` (espanhol), `User_Manual.pdf` (inglês) e `Manual_do_Usuario.pdf` (português)
estão na **raiz do repositório** e **não são editados à mão**: são montados por
[`build_manual.py`](../manual/build_manual.py) lendo os dicionários reais de `Dav/dic/`
(grupos, comandos, frases em cada idioma e ícones). Por isso o manual não fica desatualizado ao
adicionar uma função: basta gerá-lo novamente.

## Requisitos

- Python 3 com **PyMuPDF** e **PySide6** (o Qt é usado para rasterizar os ícones SVG):

  ```
  pip install pymupdf PySide6
  ```

- Não é preciso ter o FreeCAD instalado: `arbol.py` simula o FreeCAD e o Qt ao carregar a árvore.

## Gerar os PDF

A partir da raiz do repositório (também funciona de qualquer pasta):

```
python Dav/docs/manual/build_manual.py              # os três idiomas
python Dav/docs/manual/build_manual.py es           # somente um (es | en | pt)
python Dav/docs/manual/build_manual.py --salida C:/tmp   # outra pasta de saída
```

Por padrão escreve os três PDF na raiz do repositório, sobrescrevendo os existentes. Ao terminar
avisa quais comandos ficaram **sem descrição** nos `desc_*.py`.

## O que há em `Dav/docs/manual/`

| Arquivo | O que contém |
|---|---|
| `arbol.py` | Carrega a árvore de dicionários: grupos, comandos, frases e ícones SVG (mesmo critério do `IconLocator`) |
| `desc_*.py` | **O que faz** cada comando, em espanhol, inglês e português, e seu requisito |
| `textos.py` | Textos fixos (introdução, navegação, exemplos, agradecimentos) e os requisitos reutilizáveis |
| `build_manual.py` | Monta o HTML e faz a diagramação em PDF (índice, marcadores e cabeçalhos de tabela) |
| `img/` | Logo e capturas dos exemplos guiados |

## Adicionar uma função ao manual

1. Adicioná-la ao dicionário como sempre (com seu `TraduceTo*.py` e seu `<clave>.svg`).
2. No `desc_*.py` do banco correspondente, adicionar a entrada
   `"ruta/clave": ("español", "inglés", "portugués"[, "código de requisito"])`.
   O caminho é o das chaves do dicionário (`workbench/partdesign/additive/pad`).
3. Rodar novamente `build_manual.py` e revisar o aviso de comandos sem descrição.
4. Fazer commit dos três PDF regenerados junto com a mudança.

Os **grupos** (submenus como «agregar» do PartDesign) saem sozinhos como uma linha com seu ícone e
as frases para entrar; só é necessária sua descrição. Um grupo sem SVG próprio usa o ícone do seu
primeiro comando; um comando sem SVG pode tomar o de sua variante em `ICONO_PARIENTE`
(`build_manual.py`). Os códigos de requisito (`doc`, `sel`, `bodysk`…) estão em `textos.py`.

## Problemas frequentes

- **`ModuleNotFoundError: pymupdf` / `PySide6`**: instalar os pacotes acima no mesmo
  Python com que se roda o script.
- **Um comando aparece sem descrição ou sem ícone**: falta sua entrada em `desc_*.py` ou seu
  `<clave>.svg` no dicionário.
- **O PDF não muda**: confirmar que foi escrito na pasta esperada (opção `--salida`) e
  que o visualizador não está com o arquivo aberto (no Windows bloqueia a escrita).
