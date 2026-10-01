# Guia de desenvolvimento do DAV

> **DAV — Design Assistido por Voz**
> Prática Educativa Territorial — Faculdade de Ciência e Tecnologia (FCyT) — UADER

Este guia explica **como se desenvolve e se contribui para o projeto DAV**: como
colocá-lo em funcionamento, quais convenções seguir, como adicionar um comando por voz e
como testar as mudanças. Foi pensado para integrantes da equipe que se
juntam ao desenvolvimento, tanto para o código próprio do DAV quanto para o
dicionário de comandos por voz.

Está escrito a partir do que foi aprendido na prática. Se algo ficou desatualizado ou
você mudar uma convenção, **atualize este guia** no mesmo PR que altera
o código.

---

## Índice

| Seção | Conteúdo |
|---|---|
| [Estrutura do repositório](desenvolvimento/estrutura.md) | O que faz cada pasta do repositório e onde vive cada coisa |
| [Colocação em funcionamento (setup)](desenvolvimento/setup.md) | Como clonar, instalar dependências, modelos e rodar o DAV no FreeCAD |
| [Convenções de código](desenvolvimento/convencoes.md) | Nomes, cabeçalho obrigatório, docstrings, princípios de design |
| [Adicionar um comando por voz](desenvolvimento/adicionar-comando.md) | Passo a passo com exemplo real, do dicionário até o TraduceTo |
| [Adicionar um submenu](desenvolvimento/adicionar-submenu.md) | Uma pasta nova: aninhado sem achatar, os três `TraduceTo*`, ícones por nome de chave |
| [Adicionar um diálogo de voz](desenvolvimento/adicionar-prompt.md) | Prompts existentes e novos, e como restringir a gramática do Vosk |
| [Como testar e validar](desenvolvimento/testando.md) | Testes manuais, `freecadcmd` e Qt offscreen sem abrir a GUI, e links para as guias existentes |

---

## Resumo rápido

- **DAV** é uma camada de controle por **voz** sobre o **FreeCAD** usando o **Vosk**
  como reconhecedor.
- O código próprio vive em `Dav/`; a árvore de comandos por voz em `Dav/dic/`;
  o motor que percorre essa árvore é o `Browser`
  (`Dav/scr/.../navigation/browser.py`).
- As frases faladas são definidas nos `TraduceToEs.py` / `TraduceToEn.py` /
  `TraduceToPT.py` de cada pasta; o dicionário mestre de cada pasta
  vincula as chaves internas a callables do FreeCAD.
- Regra de ouro: **os subcontextos vão aninhados sob sua própria chave**, nunca
  achatados com `.update(sub_dict)`. Veja [pendientes-dav.md](pendientes-dav.md) §4.

---

## Material de referência

- **[CLAUDE.md](../../CLAUDE.md)** — documentação geral do projeto:
  arquitetura, GitFlow, modelo de voz, licenças. É a fonte da maioria
  das convenções citadas aqui.
- **[pendientes-dav.md](pendientes-dav.md)** — o que continua em aberto. **Ler
  antes de mexer em dicionários ou navegação.**
- **[concluidos-dav.md](concluidos-dav.md)** — problemas já resolvidos e sua
  causa real. Consultar antes de rediagnosticar algo conhecido.
- `README.md` / `README.es.md` / `README.pt.md` — apresentação do projeto.
