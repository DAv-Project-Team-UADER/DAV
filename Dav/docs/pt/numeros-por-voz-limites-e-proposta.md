# Números por voz — o que se pode ditar hoje e como remover o teto

Estado do reconhecimento numérico nos pop-ups de parâmetros
(`SpokenNumberParser`), qual limite ele realmente tem e o que seria necessário
para removê-lo.

---

## O que se pode ditar hoje

Ao contrário do que foi anotado nas primeiras guias de teste, **não há um teto
duro de 99**. O parser concatena dígitos, então qualquer número pode ser ditado
soletrando-o:

| Diz-se | Obtém-se |
|---|---|
| `veinticinco` | 25 |
| `treinta y cinco` | 35 |
| `cinco cero` | 50 |
| `nueve nueve` | 99 |
| **`uno cero cero`** | **100** |
| **`uno dos tres`** | **123** |
| `menos veinte` | −20 |
| `doce coma cinco` | 12,5 |

Verificado executando `SpokenNumberParser.ParseInteger` sobre cada frase.

O que **sim** corta em 99 é a pronúncia *natural* de um número como
palavra composta: «ciento veinticinco» não é entendido, porque `cien` e as
centenas não estão no dicionário.

### A consequência prática

Para valores de 0 a 99 fala-se normalmente. Para 100 ou mais é preciso
**soletrar dígito por dígito**, o que funciona, mas é pouco natural — sobretudo em casos
como um padrão circular de 360°, em que `tres seis cero` é incômodo comparado
com «trescientos sesenta».

---

## Por que acontece

`SpokenNumberParser.DigitWords` é um mapa plano de palavra → dígito, com 93
entradas que cobrem 0–30 e as dezenas (40, 50, 60, 70, 80, 90) nos três
idiomas.

`_MergeTensAndUnits` monta os compostos de duas palavras («treinta y cinco» →
35), mas **não há noção de centena nem de multiplicador**: o parser junta
dígitos em uma cadeia de texto em vez de somar valores posicionais.

```
"uno cero cero"  →  "1" + "0" + "0"  →  "100"   (concatenação, não soma)
```

Por isso soletrar funciona e pronunciar não.

---

## As três saídas possíveis

### 1. Biblioteca externa

`text2num` ou `number_parser` resolvem isso com suporte a es/en/pt.

**Não convém.** O código roda no **Python embutido do FreeCAD**, não no
venv de desenvolvimento. O projeto hoje não tem dependências externas além do
Vosk e do PyAudio, e adicionar mais uma ao interpretador embutido é frágil de instalar e
de manter nas máquinas da equipe.

### 2. Algoritmo de composição posicional — recomendada

O espanhol, como o inglês e o português, constrói números de forma
**regular**: unidades, dezenas, centenas e multiplicadores. Não é preciso
enumerar mil palavras, mas umas 30 mais as regras de combinação.

```
valor = soma de grupos, com multiplicadores que fecham cada grupo

"doscientos treinta y cinco"  →  200 + 30 + 5            =   235
"tres mil cuatrocientos"      →  (3 × 1000) + 400        =  3400
```

Palavras base necessárias:

| Grupo | Palavras |
|---|---|
| Unidades e 11–15 | `uno`…`quince` — **já estão** |
| Dezenas | `veinte`…`noventa` — **já estão** |
| Centenas | `cien`, `ciento`, `doscientos`…`novecientos` — **faltam** |
| Multiplicadores | `mil`, `millón` — **faltam** |

Ou seja: o dicionário já tem a maior parte. Falta adicionar centenas e
multiplicadores, e substituir `_MergeTensAndUnits` por um acumulador que some
por posição em vez de concatenar texto.

São umas 60 linhas, sem dependências novas, e a mesma estrutura serve para
os três idiomas.

### 3. Ampliar o hardcode

Adicionar `cien`, `doscientos`, etc. como entradas planas do mapa.

Rápido, mas não escala: para chegar a 1.000.000 seriam necessárias milhares de entradas,
e cada uma incha a gramática do Vosk.

---

## O detalhe que condiciona tudo: a gramática do Vosk

**O parser, sozinho, não basta.** A gramática do Vosk é restrita ao contexto
ativo (ver [encurtador-gramatica-vosk.md](encurtador-gramatica-vosk.md)), e
durante um pop-up numérico é trocada pela lista que `get_numeric_grammar_phrases()`
devolve em `Dav/dic/Numbers/Numbers.py`, via
`NumericGrammarSwitcher.ActivateNumericGrammar()`.

Essa lista sai **do mesmo dicionário** que alimenta o parser. Ou seja:

> Se «doscientos» não está no dicionário numérico, o Vosk **nunca vai
> transcrever essa palavra**, por mais que o parser saiba interpretá-la.

É uma boa notícia de design: parser e gramática compartilham a fonte, então
adicionar as palavras novas ao dicionário as habilita nos dois lados ao
mesmo tempo. Mas implica que a mudança **não é só do parser** — é preciso verificar
que `get_numeric_grammar_phrases()` inclua as centenas e os multiplicadores
novos.

---

## Recomendação

Encarar a **opção 2**, nesta ordem:

1. Adicionar centenas e multiplicadores ao dicionário `Numbers`, nos três
   idiomas.
2. Confirmar que `get_numeric_grammar_phrases()` os devolve (se monta a lista
   a partir do mapa completo, sai de graça).
3. Substituir `_MergeTensAndUnits` por um acumulador posicional.
4. **Manter o modo dígito a dígito**, que hoje funciona e pode haver gente
   usando: o acumulador deveria reconhecer ambas as formas.

O ponto 4 é o que mais cuidado exige. Hoje `uno cero cero` dá 100 por
concatenação; um acumulador posicional ingênuo o interpretaria como
1 + 0 + 0 = 1. É preciso decidir explicitamente como cada modo convive antes de
mexer no parser.

---

## Impacto atual

Nenhum comando está bloqueado —todo valor pode ser soletrado— mas há casos
em que isso se nota:

| Caso | Hoje | Com a proposta |
|---|---|---|
| Padrão circular 360° | `tres seis cero` | `trescientos sesenta` |
| Cota de 150 mm | `uno cinco cero` | `ciento cincuenta` |
| Medidas 0–99 | já é natural | igual |

Enquanto isso, as guias de teste usam valores menores que 100 para que as
frases de exemplo soem naturais.
