# Manual rápido — Explorer por voz

## Como funciona

O DAV navega por **níveis**, como um menu. Você diz uma palavra para **entrar** em
um submenu e outra para **executar** um comando. Você está sempre parado em um
contexto, e só são reconhecidas as palavras desse contexto.

```
Base  →  explorador  →  archivo  →  guardar
         (entrar)       (entrar)    (executar)
```

## Comandos de navegação (funcionam em qualquer contexto)

| Para | Diga |
| --- | --- |
| Subir um nível | **subir**, volver, atrás, salir, regresar, retroceder |
| Ver onde você está e o que pode dizer | **contexto**, dónde estoy, qué puedo decir, opciones disponibles, ubicación |

> Se você se perder, diga **«contexto»** — lista os submenus e comandos
> disponíveis no nível atual.

Estas palavras não estão fixas no código: vivem em `Dav/dic/NavCommands/`, então
podem-se adicionar sinônimos sem tocar em `browser.py`.

## Entrar no Explorer

A partir de Base, diga: **«explorador»** (explorador)

## Submenus do Explorer

| Submenu | Palavras para entrar |
| --- | --- |
| Arquivos | **archivo**, archivos, carpeta, carpetas, folios |
| Edição | **editar**, edición, modificar, alterar |
| Imprimir | **imprimir**, impresión, pdf, exportar pdf, generar pdf, impresora |
| Janelas | **ventanas**, ventana |
| Expressões | **expresiones**, expresión |
| Ferramentas | **herramientas**, utilidades |
| Estrutura | **estructura**, barra de estructura |
| Exemplos | **ejemplos**, quiero aprender, aprender, tutoriales |

## Comandos diretos (sem entrar em nenhum submenu)

Estando em `explorador`, executam-se direto:

- **refrescar** / recargar / actualizar (atualizar)
- **captura** / foto / sacar foto / captura de pantalla / guardar pantalla
- **documento** / texto / documento de texto
- **desvincular** / desenlazar / quitar enlace
- **congelar** / bloquear / inmovilizar
- **variables** / conjunto de variables / set de variables
- **todas las instancias** / seleccionar instancias

## Comandos dentro de cada submenu

**archivo** → nuevo · abrir · guardar · guardar como · guardar copia ·
revertir · combinar · importar · exportar · recientes · cargar imagen

**proyecto** → nuevo · abrir · guardar · exportar · impresión 3D (sem diálogos nativos; veja mais abaixo)

**editar** → deshacer · rehacer · cortar · copiar · pegar · duplicar ·
seleccionar todo · eliminar · posición · transformar · alinear · preferencias ·
propiedades · enviar a python · modo edición

**imprimir** → imprimir · impresora · pdf

**ventanas** → cerrar · cerrar todo · salir

**expresiones** → copiar documento · copiar todo · copiar selección ·
pegar expresión

**herramientas** → medir · medir distancia · limpiar selección · modo demo ·
personalizar · editar parámetros · utilidades de proyecto

**estructura** → pieza · grupo · enlace

Todos os submenus aceitam além disso **ayuda** / información / opciones (ajuda /
informação / opções).

## Projeto: abrir, salvar e exportar por voz

`archivo` usa os diálogos nativos do FreeCAD, que não se controlam por voz.
`proyecto` faz o mesmo com janelas de voz (`Dav/dic/Explorer/Proyecto/`):

- **abrir** → percorre as pastas: *siguiente* / *anterior* movem a seleção,
  *abrir* entra na pasta escolhida, *subir* vai para a pasta pai, *okey* escolhe
  o arquivo, *cancelar* sai. Começa na pasta do documento ativo ou na última
  usada.
- **guardar** → se o documento já tem arquivo, salva ali. Se é novo, pergunta a
  pasta (a sugerida ou outra, escolhida com o mesmo navegador, onde *okey* escolhe
  a pasta em que você está) e o nome (o sugerido ou um soletrado). Se o arquivo
  existe, pede *sobrescribir* (sobrescrever).
- **exportar** → escolhe o formato (STEP, IGES, STL, OBJ, DXF; com
  *arriba*/*abajo* e *okey*), depois pasta e nome como em guardar. Exporta a
  seleção ou, se não houver, tudo o que estiver visível.

- **nuevo** → cria um projeto vazio (equivale a «nuevo» de `archivo`).
- **impresión 3D** (também «impresión tres de», «preparar impresión») → como
  *exportar*, mas com os formatos que os programas de impressão 3D leem (3MF, STL,
  OBJ) e somente com peças **sólidas**: um esboço ou uma folha do TechDraw não se
  imprimem. Se o nome não é aceito como está, é soletrado. Ao terminar, informa as
  medidas do que foi exportado.

Os nomes de arquivo não podem ser ditados (não estão no vocabulário do Vosk): por
isso percorre-se a lista em vez de dizê-los.

## Exemplos: aprender fazendo

Dentro de **ejemplos** (a pasta não tem ícone) há duas opções:

| Opção | Palavras | O que faz |
| --- | --- | --- |
| Manual do usuário | **manual**, referencia | Abre o PDF no seu idioma: `Manual_Usuario.pdf` em espanhol; `User_Manual.pdf` em inglês; `Manual_do_Usuario.pdf` em português |
| Exemplos | **ejemplos**, demostraciones, tutorial | Abre um seletor com os exemplos guiados |

Exemplos guiados:

| Exemplo | O que se faz | Medidas |
| --- | --- | --- |
| **Esboço** | Um círculo com restrição de raio | Cota em 2D |
| **Draft** | Retângulo, círculo e polígono | Cota em 2D |
| **Casa** | Uma casa só com figuras 2D de medidas ditadas (corpo, telhado, porta, janelas, chaminé); aprende-se a recortar uma figura com outra | Linhas por pontos e «modificar → cortar» |
| **Rótulo** | Um rótulo simples com texto no Draft | — |
| **TechDraw** | Um círculo em uma folha com seu rótulo | — |
| **PartDesign** | Um parafuso: haste, ponta, cabeça, chanfro e rosca | Cota em 3D e vista «tres de» (3D) |
| **Dado** | Um dado de 20 mm: a face do 1 com um cilindro e as outras cinco com um esboço e um rebaixo cada uma | Cota em 3D, as seis vistas e «tres de» |
| **Arruela lisa M6** | Um esboço com o furo (Ø 6,4) e a borda (Ø 12), extrudado 1,6 mm no PartDesign e colocado em uma folha do TechDraw com vista isométrica, vista do esboço e o texto «M6 arandela» | Restrição de diâmetro e cota em 2D |
| **Parafuso-porca** | Um parafuso M6 de cabeça sextavada (simplificado da DIN 931) e sua porca, feitos no PartDesign, inseridos por voz em uma montagem, com o parafuso ancorado e uma junta cilíndrica que leva a porca ao eixo pelas faces que se escolhem | Montagem com junta cilíndrica e vista «tres de» |
| **Tesoura de 5 peças** | Duas lâminas (triângulo extrudado com lingueta e furos), dois cabos (anéis) e um pino escalonado, feitos no PartDesign e unidos em uma montagem com dobradiças e juntas fixas. A versão aberta a 50 % e o plano ANSI B estão em [guia-tesoura-voz.md](guia-tesoura-voz.md) | Montagem com dobradiça, juntas fixas e vista «tres de» |
| **Haste roscada M30 com porcas** | Um núcleo cilíndrico com uma rosca real: um filete triangular de 60° (esboço no plano XZ) enrolado em uma hélice de passo 3,5 mm e 27 voltas, e a cota do passo (3,5 mm) entre duas cristas. Uma porca sextavada M30 (DIN 934) é inserida duas vezes em uma montagem, com a haste ancorada, e cada uma é unida com uma junta de parafuso de passo 3,5 pelas faces das extremidades: ao arrastá-las, giram e avançam pela rosca | Hélice aditiva, cota 3D, junta de parafuso e vista «tres de» |

Os decimais ditam-se com «punto» nos três idiomas: «uno punto uno uno» é 1,11. Em
espanhol «coma» vale igual («uno coma uno uno»). Os números de 0 a 99 dizem-se
naturais («treinta y dos»); de 100 em diante, dígito por dígito («uno cero cero»).

O seletor é controlado com **retroceder**, **avanzar** e **enviar**. Depois de
escolhido o exemplo, aparece uma janela (não bloqueia o FreeCAD, então você vê
como a peça é montada) que mostra um **quadro** por vez com **o que você diria
para fazê-lo no DAV**: o caminho pelos menus e, depois, os valores que se ditam
nos diálogos. Quando você diz tudo, em ordem, a ação é executada e passa ao quadro
seguinte.

Por exemplo, para desenhar um círculo de raio 12 em um esboço:

```
banco → croquis → nuevo → enviar          (escolhe o plano XY)
geometría → círculo → círculo             (entra em Geometria e em Círculo, e o cria)
cero → enviar → cero → enviar → doce → enviar     (centro X, centro Y e raio)
```

Cada palavra ou frase do caminho é um comando; cada valor é confirmado com
**enviar**. O que se dita depende do documento: por exemplo, no Dado, quantas
vezes dizer **abajo** para chegar a uma face da lista sai das faces que o sólido
tem naquele momento (a janela agrupa as repetições: «abajo ×5»).

- **retroceder / avanzar**: revisar quadros já feitos.
- **saltar**: executa o quadro sem dizer suas palavras (útil se o microfone não o
  reconhece).
- **cancelar**: fecha o exemplo. Ao terminar, **enviar** o fecha.

Cada exemplo são as funções `steps()` de `Dav/dic/Explorer/Examples/_*.py`; para
adicionar um, criar um módulo com `TITLE` e `steps()` e somá-lo a `_EXAMPLES` em
`_demos.py`.

As palavras de cada quadro são verificadas contra a árvore real, nos três idiomas,
com `tests/verify_examples_paths.py` (veja [`testando.md`](desenvolvimento/testando.md)):
se o dicionário muda e um exemplo deixa de coincidir, esse teste o marca.

## Correções por voz (a partir de qualquer contexto)

Vivem no dicionário raiz (`Dav/dic/Correction/`), então são ditas sem entrar em
nenhum submenu:

| Para | Diga |
| --- | --- |
| Desfazer | **deshacer**, deshacer cambio, deshacer último |
| Refazer | **rehacer**, rehacer cambio |
| Apagar o último objeto criado | **borrar último**, eliminar último, quitar último |
| Apagar um objeto escolhido | **borrar objeto**, eliminar objeto, quitar objeto |
| Limpar objetos com erro | **borrar rotos**, limpiar rotos, limpiar errores |

Apagar sempre **pede confirmação por voz** e não pode ser desfeito daqui. Também se
dizem de qualquer lugar: **medir** / cota / acotar (cria uma cota), as vistas
padrão com o zoom (**frontal**, **arriba**, **acercar**, **ajustar todo**…),
**mover vista**, **minimizar** / **maximizar** (o painel do DAV) e **preferencias**.

## Exemplos completos

Salvar o arquivo:

```
"explorador" → "archivo" → "guardar"
```

Exportar para PDF:

```
"explorador" → "imprimir" → "pdf"
```

Desfazer uma alteração:

```
"explorador" → "editar" → "deshacer"
```

Tirar uma captura (comando direto, sem submenu):

```
"explorador" → "captura"
```

## Dicas

- **Não é preciso subir para mudar de menu principal**: de qualquer nível pode-se
  dizer «banco de trabajo», «vista estándar», etc. e salta direto.
- **Os acentos não importam**: «impresión» e «impresion» são reconhecidos igual (o
  motor normaliza acentos e eñes antes de comparar).
- **Evite as palavras em inglês** (`sketcher`, `draft`, `techdraw`): o modelo de
  voz é espanhol e as reconhece mal. Use sempre os sinônimos em castelhano.
- Se uma palavra não é entendida, tente um sinônimo da lista — quase todos os
  comandos têm dois ou três.

## De onde sai este vocabulário

Todas as palavras deste manual saem dos dicionários reais:

- `Dav/dic/Explorer/TraduceToEs.py` — submenus e comandos diretos
- `Dav/dic/Explorer/<Submenú>/TraduceToEs.py` — comandos de cada submenu
- `Dav/dic/NavCommands/TraduceToEs.py` — subir / contexto

Se forem adicionados sinônimos ali, este manual fica desatualizado: convém
regenerá-lo a partir desses arquivos.

O **manual do usuário em PDF** (`Manual_Usuario.pdf`, `User_Manual.pdf` e
`Manual_do_Usuario.pdf`, na raiz do repositório) sim se regenera sozinho: lê os
dicionários reais (grupos, comandos, frases em cada idioma e ícones) com `python
Dav/docs/manual/build_manual.py`. Para somar uma função basta escrever sua
descrição em `Dav/docs/manual/desc_*.py` e gerá-lo de novo; o script avisa quais
comandos ainda não têm descrição.
