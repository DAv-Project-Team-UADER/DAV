# Protótipos aposentados

Código que **não é executado**. É conservado como referência de design, não como
parte do programa. Nada daqui está no caminho de inicialização do DAV.

> Se você procura o motor vivo: `Dav/scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/`
> — `navigation/browser.py` (`Browser`) + `integration/voice_bootstrap.py`.

## `PruebaIntegracion/`

DAVCore completo e autônomo (40 arquivos, ~2.700 linhas): `core/VoiceExplorer.py`,
`core/Navigator.py`, `core/Command.py`, `core/FunctionWrapper.py`,
`modelo/VoskModel.py`, `hilos/GestorDeHilos.py`, GUI e testes próprios.

É a implementação literal do UML de `CLAUDE.md` (`DAVAgent` + `VoskModel`),
e por isso vale como referência: mostra o design conceitual original do
projeto antes de a implementação convergir para o `Browser`.

Usava seu próprio dicionário (`diccionario/`), não a árvore oficial `Dav/dic/`.

## `cad_session.py`, `cad_voice_adapter.py`

As duas pontes que teriam conectado `PruebaIntegracion` ao FreeCAD. Nunca foram
chamadas por ninguém: `voice_bootstrap.py` monta o motor com `Browser` +
`BrowserVoiceAdapter`, não com `ExploradorVoz` + `CadVoiceAdapter`.

## `voice_aliases.py`

Tabela de sinônimos es/pt que operava sobre `NodoContexto` de `PruebaIntegracion`.
Só era alcançada por `cad_session.py`, então é aposentada junto com ele.

> O equivalente vivo são os arquivos `TraduceTo*.py` de cada pasta de
> `Dav/dic/`, que cumprem a mesma função sobre a árvore oficial.

## Por que foram aposentados (2026-08-10)

Resumo: chegaram a existir três motores de
voz em paralelo por desenvolvimento simultâneo, não por design. Ficou um.

## Nota para quem o mover de novo

`PruebaIntegracion/` era usada como **marcador de filesystem** para localizar a
raiz `Dav/scr/` em `integration/dav_paths.py` e em `tests/test_browser.py`. Isso
já foi mudado para `validation/` + `selection/`. Se esta pasta for realocada outra vez,
não é preciso mexer em nada: ninguém mais a procura.
