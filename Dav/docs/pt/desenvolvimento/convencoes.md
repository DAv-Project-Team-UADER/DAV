# Convenções de código

Estas são as convenções do projeto DAV. Aplicam-se a **todo o código próprio**
(o que vive em `Dav/`). Os arquivos preexistentes do FreeCAD conservam suas
próprias regras (e seu cabeçalho original).

> Fonte principal: `CLAUDE.md` do repositório.

## Nomenclatura

| Tipo | Convenção | Exemplo |
|---|---|---|
| Classes | `PascalCase` | `DavAgent`, `VoskModel` |
| Atributos / Propriedades | `PascalCase` | `LineColor`, `ShapeColor` |
| Funções / Métodos | `camelCase` (inicial minúscula) | `addObject()`, `recompute()` |
| Uso interno | `_sublinhado` | `_internalMethod` |

## Organização de arquivos

- **Uma classe = um arquivo**
- **Um dicionário = um arquivo**
- O nome do arquivo é igual ao nome da classe (`DavAgent.py`)

## Cabeçalho obrigatório (todos os arquivos próprios)

Cada arquivo próprio do DAV deve começar com este cabeçalho de licença
(mantido em espanhol, textualmente):

```python
# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
```

> Os arquivos do FreeCAD preexistentes **conservam seu cabeçalho original**
> (LGPL-2.1-or-later). Não os substitua.

## Docstrings

- Toda **classe e método público** deve ter um docstring em **inglês**.
- Formato: primeira linha curta (resumo), linha em branco, depois seções
  `Args:`, `Returns:`, `Example::` conforme couber.
- O docstring é o que as IDEs (VS Code, PyCharm) mostram como tooltip ao
  invocar a classe ou o método.
- Os **comentários** de desenvolvedor (`# ...`) vão em **espanhol**.

## Documentação

- Documentar com **Mermaid** (diagramas de classes, arquitetura, fluxos).
- Padrão **UML** para o que é próprio e para o que é consumido do FreeCAD.

## Princípios de design

- **KISS** — Keep It Simple. Menos é mais.
- **SOLID** — Responsabilidade Única, Aberto/Fechado, Substituição de Liskov,
  Segregação de Interfaces, Inversão de Dependências.
- **Arquitetura Document-View** — a mesma que o FreeCAD usa internamente
  (Documento ↔ Vista ↔ Storage).

## Regra crítica: subcontextos aninhados, nunca achatados

Ao montar o dicionário mestre de uma pasta, cada submenu vai **como valor
sob sua própria chave**, nunca fundido com `.update(sub_dict)`:

```python
explorer.update({'file': file})   # CORRETO — 'file' continua navegável
explorer.update(file)             # INCORRETO — achata as folhas do filho
```

Achatar quebra duas coisas em silêncio: colide chaves repetidas entre folhas
(`create`, `help`, `center`) ficando só com a última, e deixa a pasta
fora da árvore navegável, de modo que seu `TraduceTo*.py` nunca é carregado.

## Git / commits

- **Não adicionar `Co-Authored-By` nem qualquer menção ao assistente** nas
  mensagens de commit.
- **Não fazer `commit` nem `push`** a menos que o usuário peça explicitamente.
- Mensagens de commit em espanhol, descritivas (ex.: `Sketcher: selección de
  plano por voz al crear nuevo boceto`).
- Não commitar artefatos gerados nem chaves/secrets. Os modelos de voz em
  `Dav/models/` estão excluídos do git.

---

Próximo: [Adicionar um comando por voz](adicionar-comando.md)
