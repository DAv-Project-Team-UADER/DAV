# Guia de testes — de um quadrado a uma montagem, por voz

Este guia cobre o que foi adicionado nos PRs **#208**, **#209** e **#213**: criar
geometria ditando medidas, extrudá-la para 3D e unir peças com juntas — tudo sem
diálogos do FreeCAD.

Todas as frases deste guia foram tiradas dos dicionários reais
(`Dav/dic/`). Nenhuma é inventada.

---

## Antes de começar

- Abra o FreeCAD com o painel DAV, idioma **espanhol**.
- Tenha um documento novo aberto.
- Se você se perder: diga **`donde estoy`** (onde estou) — lista o contexto atual e as
  opções disponíveis.
- Para subir um nível: **`subir`** (também `volver`, `atras`).

**Confirmar um valor** (depois de cada número):
`enter` · `enviar` · `aceptar` · `confirmar` · `ok`

**Abortar um pop-up**: `cancelar`

### Números: 0–99 dizem-se normalmente, de 100 em diante soletram-se

Pronunciam-se naturalmente até 99: 0–30 diretos, mais as dezenas (40, 50, 60, 70,
80, 90) e os compostos (`treinta y cinco`).

De 100 em diante é preciso **soletrar dígito por dígito**: `uno cero cero` dá
100, `tres seis cero` dá 360. Funciona, mas é incômodo — veja
[numeros-por-voz-limites-e-proposta.md](numeros-por-voz-limites-e-proposta.md).

Os testes deste guia usam valores menores que 100 para que as frases soem
naturais.

Outros modificadores:

| Para dizer | Diga |
|---|---|
| −20 | `menos veinte` |
| 12,5 | `doce coma cinco` |

---

## Como reportar

Para cada teste anote:

1. **O que você disse** (a frase exata).
2. **O que saiu no Report View** — todos os comandos imprimem ali, tanto o
   sucesso quanto o erro.
3. **Se o objeto apareceu na árvore** do painel DAV.

---

## Teste 1 — Cubo direto

O mais rápido. Confirma que a navegação, o pop-up e os números funcionam.

| Diga | O que acontece |
|---|---|
| `banco de trabajo` (banco de trabalho) | entra nos workbenches |
| `diseño de pieza` (projeto de peça) | entra no PartDesign |
| `aditivo` | entra nas operações aditivas |
| `caja por medidas` (caixa por medidas) | **abre o pop-up** |
| `veinte enter` | comprimento |
| `veinte enter` | largura |
| `veinte enter` | altura |

**Esperado**: um cubo de 20×20×20 e, no Report View:
`[additive] Created box 20 x 20 x 20`

> Se este teste falhar, o problema é a navegação ou o reconhecimento de números.
> Não continue com os demais até resolvê-lo.

---

## Teste 2 — Cilindro

A partir de `aditivo`:

| Diga | O que acontece |
|---|---|
| `cilindro por medidas` | abre o pop-up |
| `diez enter` | raio |
| `cuarenta enter` | altura |

**Esperado**: cilindro r=10, h=40.

---

## Teste 3 — O fluxo completo: quadrado → cubo

**Este é o teste principal.** Fecha o caminho 2D → 3D sem mouse.

### Passo A — desenhar o quadrado

| Diga | O que acontece |
|---|---|
| `banco de trabajo` | |
| `croquis` (esboço) | entra no Sketcher |
| `geometria` | entra nas geometrias |
| `rectangulo` | entra no submenu retângulo |
| `rectangulo por esquinas` | **abre o pop-up** |
| `cero enter` | x1 |
| `cero enter` | y1 |
| `veinte enter` | x2 |
| `veinte enter` | y2 |

**Esperado**: quadrado de 20×20 e
`[geometry.rectangle] Created 'Rectangle' from (0,0) to (20,20)`

### Passo B — selecioná-lo

Clique no retângulo (na árvore de objetos ou na vista 3D).

> Este passo **ainda precisa de mouse**. A seleção por voz existe, mas é outro
> fluxo.

### Passo C — extrudá-lo

| Diga | O que acontece |
|---|---|
| `subir` (até o nível de workbench) | |
| `diseño de pieza` | |
| `aditivo` | |
| `extruir por medida` | **abre o pop-up** |
| `treinta enter` | altura |

**Esperado**: o quadrado se converte em um prisma de 20×20×30 e
`[additive] Padded '...' by 30`

> **O passo mais importante a testar.** Internamente o quadrado (um
> `Part::Feature`) é convertido em esboço para poder ser extrudado. Essa conversão
> só foi validada com stubs, nunca dentro do FreeCAD.

---

## Teste 4 — Revolução

Com um perfil 2D selecionado, a partir de `aditivo`:

| Diga | O que acontece |
|---|---|
| `revolucion por angulo` | abre o pop-up |
| `noventa enter` | ângulo em graus |

**Esperado**: sólido de revolução de 90°.

---

## Teste 5 — Outras geometrias 2D

A partir de `croquis` → `geometria`:

| Figura | Diga | Valores de exemplo |
|---|---|---|
| Círculo | `circulo` → `circulo por centro` | `cero` / `cero` / `veinticinco` |
| Arco | `arco` → `arco por centro` | `cero` / `cero` / `veinticinco` / `cero` / `noventa` |
| Elipse | `elipse` → `elipse por centro` | `cero` / `cero` / `cuarenta` / `veinte` |
| Polígono | `poligono` → `poligono por lados` | `seis` / `cero` / `cero` / `veinticinco` |
| Linha | `linea` → `linea por puntos` | `cero` / `cero` / `treinta` / `treinta` |

---

## Teste 6 — Montagem com juntas

| Diga | O que acontece |
|---|---|
| `banco de trabajo` | |
| `ensamblaje` (montagem) | entra no Assembly |
| `crear ensamblaje` | cria a montagem |
| `insertar vinculo` | abre uma lista com os corpos: `avanzar` para mudar, `enviar` para escolher. O vínculo fica à direita dos já inseridos (repetir para ter dois) |
| `insertar pieza` | insere uma peça nova e vazia |

Com **uma peça** (escolhe-se em uma lista: `avanzar` e `enviar`):

| Diga | Esperado |
|---|---|
| `anclar pieza` | `[assembly] Grounded '...'` |

Com **duas peças** (escolhem-se em duas listas seguidas) e depois **por onde se une cada uma**: uma lista de faces que se percorre com `abajo` e se escolhe com `enviar` (primeiro os cilindros, pelo seu eixo, e depois as faces planas de maior para menor):

| Diga | Depois | Esperado |
|---|---|---|
| `junta por distancia` | `veinticinco enter` | `Held '...' and '...' 25 apart` |
| `junta por angulo` | `noventa enter` | `Held '...' and '...' at 90 degrees` |
| `ensamble fijo` | — | `Fixed '...' to '...'` |
| `bisagra` | — | `Hinged '...' to '...'` |
| `junta deslizante` | — | `Slider between '...' and '...'` |

**Juntas sem medidas** (duas peças e por onde se une cada uma):

| Diga | O que faz |
|---|---|
| `rotula` | livre em qualquer rotação |
| `junta de cilindro` (ou `junta cilindrica`) | gira e desliza sobre um eixo |
| `junta paralela` | mantém as peças paralelas |
| `junta perpendicular` | mantém as peças em ângulo reto |

**Juntas de transmissão** (duas peças e por onde se une cada uma; pedem raios):

| Diga | Depois | O que faz |
|---|---|---|
| `junta de engranajes` | `veinte` / `diez` | engrena com essa relação |
| `junta de correa` | `treinta` / `quince` | polias unidas por correia |
| `junta de tornillo` | `cinco` | avanço da rosca |
| `junta de cremallera` | `diez` | cremalheira e pinhão |

Para verificar que o solver roda: `resolver ensamblaje`.

> As peças e o lugar por onde cada uma se une são escolhidos por voz. Só são oferecidos cilindros e faces planas: não é possível escolher arestas nem vértices soltos.

---

## Teste 7 — Que os erros avisem

Estas rotas estão implementadas mas **não foram testadas dentro do FreeCAD**.
Confirme que a mensagem sai no Report View:

| Teste | Como | Mensagem esperada |
|---|---|---|
| Raio zero | `circulo por centro` → `cero`/`cero`/`cero` | `radius must be greater than zero` |
| Polígono impossível | `poligono por lados` → `dos` | `a polygon needs at least 3 sides` |
| Caixa com lado zero | `caja por medidas` → `veinte`/`cero`/`veinte` | `every dimension must be greater than zero` |
| Junta sem seleção | `ensamble fijo` sem selecionar nada | `select two parts to join first` |
| Cancelar | em qualquer pop-up diga `cancelar` | `Command cancelled by user` |
| Negativos | `menos veinte enter` | aceita −20 |
| Decimais | `doce coma cinco enter` | aceita 12,5 |

---

## Teste 8 — O bug da árvore de objetos

Verifica uma correção pontual: antes, as elipses e polígonos criados por voz
**não apareciam na árvore** do painel DAV.

1. Crie uma **elipse** (teste 5).
2. Crie um **polígono**.
3. Olhe a árvore de objetos do painel DAV.

**Esperado**: ambos constam na árvore. Se não aparecerem, a correção não funcionou.

---

## Teste 9 — Os outros idiomas

Três módulos tinham dicionários que falhavam em silêncio: o loader isola o
módulo quebrado e segue com mapa vazio, então as frases simplesmente não
respondiam, sem nenhum erro visível.

Mude o idioma do painel e teste se respondem:

| Idioma | Frase | Deveria |
|---|---|---|
| Inglês | `box by size` | abrir o pop-up da caixa |
| Inglês | `line by points` | abrir o pop-up da linha |
| Português | `caixa por medidas` | abrir o pop-up da caixa |
| Português | `junta fixa` | criar uma junta fixa |

As do PartDesign em inglês e **todo o Assembly em português** estavam fora do ar
antes destas mudanças.

---

## Onde é mais provável que falhe

Nada disto foi executado dentro do FreeCAD: foi validado com stubs, que confirmam
o roteamento das frases, a matemática e que os valores ditados chegam às
propriedades corretas — mas não a interação com o FreeCAD vivo.

Os três pontos de maior risco:

1. **Passo C do teste 3** — a conversão de quadrado em esboço.
   `addGeometry` com curvas reais pode se comportar diferente do que com o stub.
2. **As juntas do teste 6** — usa-se `Vertex1` de cada peça como ponto de
   ancoragem padrão; com formas complexas pode não ser o ponto esperado.
3. **A cadeia de navegação completa** — que
   `banco de trabajo` → `diseño de pieza` → `aditivo` funcione em sequência com
   o reconhecimento de voz real, não só no dicionário.
