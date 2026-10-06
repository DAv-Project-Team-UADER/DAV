# Guia — uma tesoura de 5 peças, da voz ao desenho ANSI

Como desenhar por voz no DAV uma montagem de tesoura (2 lâminas, 2 cabos e 1 pino) e
colocá-la em um desenho técnico com legenda ANSI, com uma vista lateral (tesoura aberta a 50 %,
com eixo de simetria) e uma vista isométrica (tesoura fechada).

![Desenho terminado](../ejemplo-tijeras/tijeras_dav.png)

Arquivos para comparar com o seu resultado, em [ejemplo-tijeras/](../ejemplo-tijeras/):

| Arquivo | O que é |
|---|---|
| `tijeras_dav.FCStd` | o modelo completo (5 corpos, 2 montagens, desenho) |
| `tijeras_dav.pdf` / `.png` | o desenho exportado |
| `crear_tijeras.py` | monta tudo o que foi dito acima com a API do FreeCAD, com os mesmos valores deste guia |

> **O que está testado e o que não.** Os valores, as juntas e os números de «avanzar» (avançar) deste guia
> saem de executar as funções reais do DAV (`_InsertLink`, `_CreateJoint`, `listConnectors`) e
> o solver do FreeCAD 1.1: o modelo converge e não há interferências, exceto a braçadeira
> lâmina/cabo, que é intencional. **O reconhecimento de voz não foi testado.** As frases
> foram tiradas dos dicionários de `Dav/dic/`. A parte do TechDraw (fase 4) agora se
> faz por voz; só a legenda mantém passos com mouse (🖱).

> **Também como exemplo guiado dentro do DAV:** `explorador` → `ejemplos` → `ejemplos` → *Tijera de 5 piezas*. Cobre as 5 peças e a montagem fechada (fases 1 e 2); a tesoura aberta e o desenho estão só neste guia.

## Antes de começar

- FreeCAD com o painel DAV, idioma **espanhol**, documento novo e vazio.
- Se você se perder: **`contexto`**. Para subir um nível: **`subir`**. Para abortar um pop-up: **`cancelar`**.
- Cada valor é dito e confirmado com **`enter`** (`ochenta enter` — oitenta). Negativos: `menos diez` (menos dez).
  Decimais: `uno coma ocho` (um vírgula oito). Os números de 0 a 99 dizem-se normalmente (todos os deste guia).
- Nas listas (corpos, peças, desenhos) começa-se no primeiro elemento: **`avanzar`** passa
  ao seguinte e **`enviar`** escolhe. «Avanzar ×3» = dizê-lo três vezes e depois `enviar`.
- `subir ×N` significa dizer `subir` N vezes. `banco de trabajo` (banco de trabalho) só vale a partir do menu principal.

## O modelo

A tesoura fica deitada no plano XY; o pino é o eixo Z. Medidas em mm.

| # | Peça | Como é |
|---|---|---|
| 1 | Lâmina A | triângulo (80,0) (−10,−16) (−26,14) extrudado 2; lingueta Ø20 em (−32,18); furo de pino Ø4; furo Ø16 na lingueta |
| 2 | Lâmina B | espelho da A em Y: (80,0) (−10,16) (−26,−14); lingueta em (−32,−18); furo de pino **Ø3,6** |
| 3 | Cabo A | anel Ø28 × 4 em (−32,18), vazado Ø16 |
| 4 | Cabo B | igual, em (−32,−18) |
| 5 | Pino | cabeça Ø10 × 2, eixo Ø4 × 2 (lâmina A), eixo Ø3,6 × 2 (lâmina B) |

Por que assim: o **pino é escalonado** (Ø4 e Ø3,6) para que a montagem empilhe sozinha a lâmina B
2 mm sobre a A sem pedir nenhuma junta de posição. Os **vazados Ø16** de lâmina e cabo são
cilindros do mesmo eixo: sobre eles se faz a junta fixa lâmina↔cabo.

Abertura: máximo 60°, então 50 % = 30° (cada lâmina ±15° em relação ao eixo X). Consegue-se com uma
junta de distância entre os cabos: **23,3 mm** de folga (fechada são 8).

## Fase 1 — as 5 peças

Lâmina A:

| # | Diga | O que acontece |
|---|---|---|
| 1 | `banco de trabajo` → `croquis` (esboço) → `geometria` → `triangulo` → `triangulo por vertices` | pop-up de 6 valores |
| 2 | `ochenta enter` `cero enter` `menos diez enter` `menos dieciseis enter` `menos veintiseis enter` `catorce enter` | triângulo da lâmina A |
| 3 | `subir ×3` → `diseño de pieza` → `aditivo` → `extruir por medida` | lista de desenhos |
| 4 | `enviar` · `dos enter` | cria-se o corpo 1 (lâmina A) |
| 5 | `cilindro por medidas` · `diez` `dos` `menos treinta y dos` `dieciocho` `uno` (cada um com `enter`) · `no` · `enviar` | lingueta, somada ao corpo 1 |
| 6 | `subir` → `cortar` → `cortar cilindro por medidas` · `dos` `diez` `cero` `cero` `uno` · `enviar` | furo do pino |
| 7 | `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `dieciocho` `uno` · `enviar` | vazado da lingueta |

Lâmina B (corpo 2):

| # | Diga | O que acontece |
|---|---|---|
| 8 | `subir ×2` → `croquis` → `geometria` → `triangulo` → `triangulo por vertices` · `ochenta` `cero` `menos diez` `dieciseis` `menos veintiseis` `menos catorce` | triângulo da lâmina B |
| 9 | `subir ×3` → `diseño de pieza` → `aditivo` → `extruir por medida` · **`avanzar ×2`** (o último da lista) · `enviar` · `dos enter` | corpo 2 |
| 10 | `cilindro por medidas` · `diez` `dos` `menos treinta y dos` `menos dieciocho` `uno` · `no` · `avanzar` · `enviar` | lingueta |
| 11 | `subir` → `cortar` → `cortar cilindro por medidas` · `uno coma ocho` `diez` `cero` `cero` `uno` · `avanzar` · `enviar` | furo do pino (Ø3,6) |
| 12 | `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `menos dieciocho` `uno` · `avanzar` · `enviar` | vazado |

Cabos e pino (cada «corpo novo» é `si` — sim):

| # | Diga | O que acontece |
|---|---|---|
| 13 | `subir` → `aditivo` → `cilindro por medidas` · `catorce` `cuatro` `menos treinta y dos` `dieciocho` `uno` · `si` | corpo 3 (cabo A) |
| 14 | `subir` → `cortar` → `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `dieciocho` `uno` · **`avanzar ×2`** · `enviar` | vazado |
| 15 | `subir` → `aditivo` → `cilindro por medidas` · `catorce` `cuatro` `menos treinta y dos` `menos dieciocho` `uno` · `si` | corpo 4 (cabo B) |
| 16 | `subir` → `cortar` → `cortar cilindro por medidas` · `ocho` `diez` `menos treinta y dos` `menos dieciocho` `uno` · **`avanzar ×3`** · `enviar` | vazado |
| 17 | `subir` → `aditivo` → `cilindro por medidas` · `cinco` `dos` `cero` `cero` `menos uno` · `si` | corpo 5: cabeça do pino |
| 18 | `cilindro por medidas` · `dos` `dos` `cero` `cero` `uno` · `no` · **`avanzar ×4`** · `enviar` | eixo da lâmina A |
| 19 | `cilindro por medidas` · `uno coma ocho` `dos` `cero` `cero` `tres` · `no` · **`avanzar ×4`** · `enviar` | eixo da lâmina B |

Ordem dos corpos nas listas: 1 lâmina A, 2 lâmina B, 3 cabo A, 4 cabo B, 5 pino
(o painel os mostra como `Body`, `Body001`…).

## Fase 2 — montagem fechada

Uma montagem por estado da tesoura: assim cada vista do TechDraw usa um único objeto de origem.

| # | Diga | Lista que aparece |
|---|---|---|
| 20 | `subir ×2` → `ensamblaje` → `crear ensamblaje` | a montagem nova fica ativa |
| 21 | `insertar vinculo` | corpos: `enviar` (lâmina A) |
| 22 | `insertar vinculo` · `avanzar` · `enviar` | lâmina B |
| 23 | `insertar vinculo` · `avanzar ×2` · `enviar` | cabo A |
| 24 | `insertar vinculo` · `avanzar ×3` · `enviar` | cabo B |
| 25 | `insertar vinculo` · `avanzar ×4` · `enviar` | pino |
| 26 | `anclar pieza` · `avanzar ×9` · `enviar` | o vínculo do pino (5 corpos + 4 vínculos antes) |
| 27 | `bisagra` | 1.ª lista `avanzar ×9` `enviar` (pino); 2.ª `avanzar ×5` `enviar` (lâmina A). Faces: pino `abajo` `enviar` (cilindro Ø4); lâmina A `abajo ×2` `enviar` (cilindro Ø4) |
| 28 | `bisagra` | 1.ª `avanzar ×9` `enviar`; 2.ª `avanzar ×6` `enviar` (lâmina B). Faces: pino `abajo ×2` `enviar` (Ø3,6); lâmina B `abajo ×2` `enviar` |
| 29 | `ensamble fijo` | 1.ª `avanzar ×5` `enviar` (lâmina A); 2.ª `avanzar ×6` `enviar` (cabo A). Faces: `abajo` `enviar` em cada uma (vazado Ø16) |
| 30 | `ensamble fijo` | 1.ª `avanzar ×6` `enviar` (lâmina B); 2.ª `avanzar ×7` `enviar` (cabo B). Faces: `abajo` `enviar` em cada uma |
| 31 | `resolver ensamblaje` | a lâmina B sobe 2 mm; tudo se encaixa |

Nos passos 27–30 a lista de faces mostra primeiro os cilindros (de maior para menor área):
se o painel diz «Cilindro de radio 8» é o vazado, «radio 2» é o do pino.

## Fase 3 — montagem aberta a 50 %

Mesmos passos com **outra montagem**. As listas de peças agora incluem os 5 vínculos da
fechada, então os números sobem em 5:

| # | Diga | Resultado |
|---|---|---|
| 32 | `crear ensamblaje`, e 5 vezes `insertar vinculo` como em 21–25 | 5 vínculos novos |
| 33 | `anclar pieza` · `avanzar ×14` · `enviar` | pino ancorado |
| 34 | `bisagra` | 1.ª `avanzar ×14`; 2.ª `avanzar ×10` (lâmina A); faces como em 27 |
| 35 | `bisagra` | 1.ª `avanzar ×14`; 2.ª `avanzar ×11` (lâmina B); faces como em 28 |
| 36 | `ensamble fijo` | 1.ª `avanzar ×10`; 2.ª `avanzar ×11`; faces como em 29 |
| 37 | `ensamble fijo` | 1.ª `avanzar ×11`; 2.ª `avanzar ×12`; faces como em 30 |
| 38 | `junta por distancia` · `veintitres coma tres enter` | 1.ª lista `avanzar ×12` `enviar` (cabo A); 2.ª `avanzar ×12` `enviar` (cabo B); faces: `enviar` em ambas (cilindro externo Ø28) |
| 39 | `resolver ensamblaje` | a tesoura abre ±15° |

Se o DAV avisar de «2 assemblies in the document», faça duplo clique (🖱) na montagem que você quer
usar para ativá-la e repita o comando.

## Fase 4 — desenho ANSI B (ASME Y14.1, 17×11 in)

Projeção em terceiro diedro (norma ASME Y14.3, a usual nos EUA). Legenda ANSI B do
modelo `ASME/ANSIB_Landscape.svg`.

| # | Diga / faça | O que acontece |
|---|---|---|
| 40 | `subir` até o menu principal → `banco de trabajo` → `dibujo tecnico` → `pagina` → `plantilla` | abre o navegador de arquivos |
| 41 | `abrir` (entra em `ASME`) · `siguiente ×5` · `okey` | página com `ANSIB_Landscape.svg` |
| 42 | `subir` → `vistas` → `vista de objeto` · na lista de objetos: **`buscar por deletreo`** → soletre `te i jota e erre a` `espacio` `a be i e erre te a` (Tijera abierta) · `okey` · `okey` | o quadro salta para o objeto mais parecido; `okey` o escolhe |
| 43 | Seguem as perguntas do mesmo comando: direção `superior` · escala `uno coma veinticinco enter` · X `uno cero cinco enter` · Y `uno seis cero enter` (as centenas dizem-se dígito por dígito) | vista lateral |
| 44 | `vista de objeto` · `buscar por deletreo` → `Tijera cerrada` · `okey` · `isometrica` · `uno coma veinticinco enter` · `tres dos cinco enter` · `uno seis cero enter` | vista isométrica |
| 45 | `proyeccion de pagina` · `tercer angulo` | terceiro diedro |
| 46 | **Eixo de simetria:** `lineas` → `eje de simetria` · vista (`avanzar`/`okey`) · `horizontal` · `origen` | linha de centro pelo pino, sobre o eixo X |
| 47 | Cotas totais: `cotas` → `extension` → `cotas totales` · vista | comprimento 117,56 e altura 79,3 |
| 48 | Legenda: `elementos` → `campos` preenche o que sai das propriedades do documento; o resto (título, número DAV-TJ-001, escala 5:4) edita-se com duplo clique 🖱 | legenda preenchida |
| 49 | `pagina` → `pdf` · pasta e nome por voz | PDF |

### Buscar por soletração

Em qualquer lista de objetos (vistas, montagens, peças...), em vez de dizer `avanzar` cem vezes:

1. Diga **`buscar por deletreo`** (basta `deletrear` ou `buscar`).
2. Soletre o nome letra por letra, com `espacio` entre palavras e `borrar` para corrigir; `okey` encerra.
3. O quadro salta para o objeto que **mais se parece** (tolera-se que o reconhecedor confunda letras
   vizinhas como be/de/pe/te) e nomeia outros dois candidatos. `okey` o escolhe; se não era, repita a busca
   ou continue com `avanzar`.

Fora de uma lista, a mesma frase seleciona no documento o objeto mais parecido (pergunta
«¿Es …?» e você responde `si` ou `no`).

### O que ainda precisa de revisão do usuário

- **Propriedades fora destes comandos** (por exemplo mudar só a escala de uma vista já criada): `escala de vista`,
  `direccion de vista` e `posicion de vista` fazem isso sem passar pelo painel de propriedades.
- O eixo de simetria e as cotas precisam da folha à vista; o DAV a abre sozinho, mas se o FreeCAD avisar que não
  criou o eixo, abra a página (duplo clique 🖱 na árvore) e repita o comando.
- Estes comandos foram verificados criando vistas, mudando direção/escala/posição/projeção e cotas totais no FreeCAD 1.1
  (sem interface, com as respostas de voz simuladas). **O reconhecimento de voz e o traçado do eixo (que exige a interface)
  não foram testados.**

Se você quiser pular os passos 42–49 e ver o resultado, execute `ejemplo-tijeras/crear_tijeras.py` com
`freecad.exe`: gera o mesmo desenho.

## Problemas frequentes

| Sintoma | Causa e solução |
|---|---|
| «la figura no se pudo unir al cuerpo» (a figura não pôde ser unida ao corpo) | a lingueta ou os eixos não tocam o sólido: revise x, y, z |
| A lâmina B fica sobre a A no mesmo plano | falta a dobradiça com o eixo Ø3,6 (passo 28) |
| A tesoura aberta sai invertida ou inclinada | repita `resolver ensamblaje`; se persistir, apague a junta de distância e recrie-a |
| As listas mostram outros números | conte com o painel: `avanzar` até ver o nome correto |
