# Guia de testes — PartDesign por voz

Cobre os comandos do PartDesign que aceitam **medidas ditadas**: criar sólidos,
extrudar perfis, cortá-los e dar-lhes acabamento, sem abrir os diálogos do FreeCAD.

Todas as frases foram tiradas dos dicionários reais (`Dav/dic/`).

Para o fluxo completo a partir do desenho 2D e para o Assembly, veja
[guia-testes-3d-voz.md](guia-testes-3d-voz.md).

---

## Antes de começar

- FreeCAD com o painel DAV, idioma **espanhol**, documento novo aberto.
- Se você se perder: **`donde estoy`** (onde estou). Para subir um nível: **`subir`**.
- **Confirmar um valor**: `enter` · `enviar` · `aceptar` · `confirmar` · `ok`
- **Abortar um pop-up**: `cancelar`

### Números: 0–99 dizem-se normalmente, de 100 em diante soletram-se

Pronunciam-se naturalmente até 99: 0–30 diretos, mais as dezenas (40, 50, 60, 70,
80, 90) e os compostos (`treinta y cinco`).

De 100 em diante é preciso **soletrar**: `uno cero cero` dá 100. Veja
[numeros-por-voz-limites-e-proposta.md](numeros-por-voz-limites-e-proposta.md).

| Para dizer | Diga |
|---|---|
| −20 | `menos veinte` |
| 12,5 | `doce coma cinco` |

### Como chegar

Todos os testes começam com:

```
banco de trabajo → diseño de pieza
```

E dali se entra em `aditivo`, `sustractivo` ou `modificar`.

---

## O que esperar de cada comando

| Categoria | Comando de voz | Prompts | O que faz |
|---|---|---|---|
| Aditivo | `caja por medidas` | 3 | caixa / cubo |
| Aditivo | `cilindro por medidas` | 2 | cilindro |
| Aditivo | `extruir por medida` | 1 | perfil → sólido |
| Aditivo | `revolucion por angulo` | 1 | perfil → revolução |
| Aditivo | `esfera por radio` | 1 | esfera |
| Aditivo | `cono por medidas` | 3 | cone / tronco |
| Aditivo | `toro por medidas` | 2 | toro |
| Aditivo | `prisma por medidas` | 3 | prisma regular |
| Subtrativo | `vaciado por medida` | 1 | vazado com a forma do perfil |
| Subtrativo | `agujero por medidas` | 2 | furo cilíndrico |
| Subtrativo | `ranura por angulo` | 1 | ranhura por revolução |
| Subtrativo | `cortar caja por medidas` | 3 | subtrai uma caixa |
| Subtrativo | `cortar cilindro por medidas` | 2 | subtrai um cilindro |
| Subtrativo | `cortar esfera por radio` | 1 | subtrai uma esfera |
| Modificar | `redondear por radio` | 1 | arredonda todas as arestas |
| Modificar | `chaflan por medida` | 1 | chanfra todas as arestas |
| Modificar | `chaflan con angulo` | 2 | chanfro com ângulo próprio |
| Modificar | `espesor por medida` | 1 | esvazia deixando parede |
| Transformar | `patron lineal por medida` | 2 | N cópias em linha |
| Transformar | `repetir cada` | 2 | N cópias com espaçamento |
| Transformar | `patron circular por medida` | 2 | N cópias em círculo |
| Transformar | `escalar por factor` | 2 | escala o sólido |

---

## Teste 1 — Cubo

| Diga | O que acontece |
|---|---|
| `banco de trabajo` → `diseño de pieza` → `aditivo` | |
| `caja por medidas` | abre o pop-up |
| `veinte enter` | comprimento |
| `veinte enter` | largura |
| `veinte enter` | altura |

**Esperado**: `[additive] Created box 20 x 20 x 20`

> Comece por aqui: se falhar, o problema é a navegação ou os números, não os
> comandos.

---

## Teste 2 — Cilindro

A partir de `aditivo`:

| Diga | O que acontece |
|---|---|
| `cilindro por medidas` | abre o pop-up |
| `diez enter` | raio |
| `cuarenta enter` | altura |

**Esperado**: `[additive] Created cylinder radius 10 height 40`

---

## Teste 3 — Arredondar o cubo

Com o cubo do teste 1 **selecionado** (clique na árvore ou na vista 3D):

| Diga | O que acontece |
|---|---|
| `subir` → `modificar` | entra nos acabamentos |
| `redondear por radio` | abre o pop-up |
| `tres enter` | raio |

**Esperado**: todas as arestas arredondadas e
`[modify] Rounded '...' with radius 3`

> O raio deve ser **menor que a metade do lado mais curto** do sólido. Com um
> cubo de 20, um raio de 3 funciona; um de 15 falha ao recalcular.

---

## Teste 4 — Chanfro

Com um sólido selecionado, a partir de `modificar`:

| Diga | Depois | Esperado |
|---|---|---|
| `chaflan por medida` | `dos enter` | chanfro de 2 mm a 45° |
| `chaflan con angulo` | `dos enter` / `treinta enter` | chanfro de 2 mm a 30° |

**Esperado**: `[modify] Chamfered '...' with size 2` (ou `... at 30 degrees`).

---

## Teste 5 — Esvaziar

Com um sólido selecionado, a partir de `modificar`:

| Diga | O que acontece |
|---|---|
| `espesor por medida` | abre o pop-up |
| `dos enter` | espessura da parede |

**Esperado**: `[modify] Hollowed '...' leaving 2 of wall`

---

## Teste 6 — Cortar (subtrativo)

Estes comandos precisam de um **perfil 2D selecionado**, igual a `extruir`.

Primeiro desenhe um quadrado pequeno:

```
subir → croquis → geometria → rectangulo → rectangulo por esquinas
cero / cero / diez / diez
```

Selecione-o e, a partir de `diseño de pieza` → `sustractivo`:

| Diga | Depois | Esperado |
|---|---|---|
| `vaciado por medida` | `diez enter` | `Pocketed '...' by 10` |
| `ranura por angulo` | `noventa enter` | `Grooved '...' by 90 degrees` |

Para o furo, desenhe um círculo e selecione-o:

| Diga | Depois | Esperado |
|---|---|---|
| `agujero por medidas` | `seis enter` / `veinticinco enter` | `Drilled a hole of diameter 6 and depth 25` |

---

## Teste 7 — Fluxo completo: quadrado → cubo → arredondado

Encadeia tudo. É o teste de maior valor.

| Passo | Diga |
|---|---|
| 1 | `banco de trabajo` → `croquis` → `geometria` → `rectangulo` |
| 2 | `rectangulo por esquinas` → `cero`/`cero`/`veinte`/`veinte` |
| 3 | *(clique no retângulo para selecioná-lo)* |
| 4 | `subir` até workbench → `diseño de pieza` → `aditivo` |
| 5 | `extruir por medida` → `treinta enter` |
| 6 | *(clique no sólido)* |
| 7 | `subir` → `modificar` → `redondear por radio` → `tres enter` |

**Esperado**: um prisma de 20×20×30 com as arestas arredondadas.

> Os passos 3 e 6 **ainda precisam de mouse**. A seleção por voz existe, mas é
> outro fluxo.

---

## Teste 8 — Mais primitivas

A partir de `aditivo`, cada uma abre seu pop-up:

| Diga | Valores | Resultado |
|---|---|---|
| `esfera por radio` | `quince` | esfera r=15 |
| `cono por medidas` | `diez` / `cero` / `veinticinco` | cone com ponta |
| `cono por medidas` | `diez` / `cinco` / `veinticinco` | tronco de cone |
| `toro por medidas` | `veinte` / `cinco` | toro (anel 20, tubo 5) |
| `prisma por medidas` | `seis` / `diez` / `treinta` | prisma hexagonal |

> No toro, o raio do tubo deve ser **menor** que o do anel, ou o comando avisa e
> não cria nada.

---

## Teste 9 — Subtrair primitivas

Com um sólido já criado, a partir de `sustractivo`:

| Diga | Valores | Resultado |
|---|---|---|
| `cortar caja por medidas` | `diez` / `diez` / `veinte` | subtrai uma caixa |
| `cortar cilindro por medidas` | `cinco` / `veinte` | subtrai um cilindro |
| `cortar esfera por radio` | `ocho` | subtrai uma esfera |

São subtraídas do **último corpo criado**.

---

## Teste 10 — Padrões e escala

Com uma operação selecionada (por exemplo o furo do teste 6), a partir de
`transformar`:

| Diga | Valores | Resultado |
|---|---|---|
| `patron lineal por medida` | `cinco` / `ochenta` | 5 cópias distribuídas em 80 mm |
| `repetir cada` | `cinco` / `veinte` | 5 cópias, uma a cada 20 mm |
| `patron circular por medida` | `seis` / `trescientos sesenta`* | 6 cópias em círculo completo |
| `escalar por factor` | `dos` / `dos` | duplica o tamanho |

\* **Atenção**: 360 não pode ser pronunciado como palavra; é preciso soletrá-lo:
`tres seis cero enter`. Funciona, mas é incômodo — está documentado em
[numeros-por-voz-limites-e-proposta.md](numeros-por-voz-limites-e-proposta.md).

> A diferença entre os dois padrões lineares: `patron lineal por medida`
> distribui as cópias ao longo do **total** ditado; `repetir cada` usa o valor
> como **espaçamento entre cópias**.

---

## Teste 11 — Que os erros avisem

Implementadas mas **não testadas dentro do FreeCAD**. Confirme que a mensagem
sai no Report View:

| Teste | Como | Mensagem esperada |
|---|---|---|
| Caixa com lado zero | `caja por medidas` → `veinte`/`cero`/`veinte` | `every dimension must be greater than zero` |
| Raio negativo | `redondear por radio` → `menos uno` | `radius must be greater than zero` |
| Chanfro zero | `chaflan por medida` → `cero` | `size must be greater than zero` |
| Ângulo impossível | `chaflan con angulo` → `dos` / `doscientos` | `angle must be between 0 and 180` |
| Sem seleção | `redondear por radio` sem selecionar nada | `select the solid to round first` |
| Cancelar | `cancelar` em qualquer pop-up | `Command cancelled by user` |

---

## Teste 12 — Os outros idiomas

O PartDesign tinha três pastas com dicionários que falhavam em silêncio: o
loader isola o módulo quebrado e segue com mapa vazio, então as frases
simplesmente não respondiam, sem erro visível.

| Idioma | Frase | Deveria |
|---|---|---|
| Inglês | `box by size` | abrir o pop-up da caixa |
| Inglês | `fillet by radius` | abrir o pop-up do arredondamento |
| Português | `caixa por medidas` | abrir o pop-up da caixa |
| Português | `chanfro por medida` | abrir o pop-up do chanfro |

---

## Como reportar

Para cada teste: **o que você disse**, **o que saiu no Report View** e **se o
objeto apareceu na árvore** do painel DAV.

---

## Onde é mais provável que falhe

Nada disto foi executado dentro do FreeCAD: foi validado com stubs, que confirmam o
roteamento das frases e que os valores ditados chegam às propriedades
corretas (`Pad.Length`, `Fillet.Radius`, `Chamfer.Angle`…), mas não a
interação com o FreeCAD vivo.

Os pontos de maior risco:

1. **Arredondamento e chanfro** — aplicam-se a **todas as arestas** do sólido
   (`UseAllEdges`), porque escolher arestas soltas por voz não é prático. Se o
   raio ou o tamanho for muito grande para a peça, o recompute falha: é
   comportamento do FreeCAD, não do comando, mas convém ver que mensagem
   aparece.
2. **Subtrativo** — o perfil é convertido de `Part::Feature` em esboço, igual
   a `extruir`. Com curvas reais pode se comportar diferente do que com o
   stub.
3. **`agujero por medidas`** — força-se `DepthType = 1` para que respeite a
   profundidade ditada; vale confirmar que o furo sai com a profundidade
   pedida e não passante.
