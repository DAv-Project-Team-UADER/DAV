# Numbers by voice — what can be dictated today and how to remove the ceiling

State of numeric recognition in the parameter pop-ups
(`SpokenNumberParser`), what limit it really has, and what it would take to
remove it.

---

## What can be dictated today

Contrary to what was noted in the first test guides, **there is no hard ceiling
of 99**. The parser concatenates digits, so any number can be dictated by
spelling it out:

| You say | You get |
|---|---|
| `veinticinco` | 25 |
| `treinta y cinco` | 35 |
| `cinco cero` | 50 |
| `nueve nueve` | 99 |
| **`uno cero cero`** | **100** |
| **`uno dos tres`** | **123** |
| `menos veinte` | −20 |
| `doce coma cinco` | 12.5 |

Verified by running `SpokenNumberParser.ParseInteger` on each phrase.

What **does** cut off at 99 is the *natural* pronunciation of a number as a
compound word: "ciento veinticinco" is not understood, because `cien` and the
hundreds are not in the dictionary.

### The practical consequence

For values from 0 to 99 you speak normally. For 100 or more you have to **spell
digit by digit**, which works but is unnatural — especially in cases like a
360° circular pattern, where `tres seis cero` is awkward compared to
"trescientos sesenta".

---

## Why it happens

`SpokenNumberParser.DigitWords` is a flat word → digit map, with 93 entries
that cover 0–30 and the tens (40, 50, 60, 70, 80, 90) in the three languages.

`_MergeTensAndUnits` builds the two-word compounds ("treinta y cinco" → 35),
but **there is no notion of hundreds or of a multiplier**: the parser joins
digits into a text string instead of adding positional values.

```
"uno cero cero"  →  "1" + "0" + "0"  →  "100"   (concatenation, not a sum)
```

That is why spelling works and pronouncing does not.

---

## The three possible ways out

### 1. External library

`text2num` or `number_parser` solve this with es/en/pt support.

**Not advisable.** The code runs in **FreeCAD's embedded Python**, not in the
development venv. The project currently has no external dependencies beyond
Vosk and PyAudio, and adding another one to the embedded interpreter is fragile
to install and to maintain on the team's machines.

### 2. Positional composition algorithm — recommended

Spanish, like English and Portuguese, builds numbers in a **regular** way:
units, tens, hundreds, and multipliers. There is no need to enumerate a
thousand words, just about 30 more plus the combination rules.

```
value = sum of groups, with multipliers closing each group

"doscientos treinta y cinco"  →  200 + 30 + 5            =   235
"tres mil cuatrocientos"      →  (3 × 1000) + 400        =  3400
```

Base words needed:

| Group | Words |
|---|---|
| Units and 11–15 | `uno`…`quince` — **already there** |
| Tens | `veinte`…`noventa` — **already there** |
| Hundreds | `cien`, `ciento`, `doscientos`…`novecientos` — **missing** |
| Multipliers | `mil`, `millón` — **missing** |

That is: the dictionary already has most of it. What is missing is adding the
hundreds and multipliers, and replacing `_MergeTensAndUnits` with an
accumulator that adds by position instead of concatenating text.

It is about 60 lines, with no new dependencies, and the same structure serves
all three languages.

### 3. Expand the hardcoding

Add `cien`, `doscientos`, etc. as flat entries of the map.

Quick, but it does not scale: reaching 1,000,000 would take thousands of
entries, and each one inflates the Vosk grammar.

---

## The detail that conditions everything: the Vosk grammar

**The parser is not enough on its own.** The Vosk grammar is narrowed to the
active context (see [vosk-grammar-shortener.md](vosk-grammar-shortener.md)),
and during a numeric pop-up it is switched to the list returned by
`get_numeric_grammar_phrases()` in `Dav/dic/Numbers/Numbers.py`, via
`NumericGrammarSwitcher.ActivateNumericGrammar()`.

That list comes **from the same dictionary** that feeds the parser. That is:

> If "doscientos" is not in the numeric dictionary, Vosk will **never
> transcribe that word**, no matter that the parser knows how to interpret it.

It is good news from a design standpoint: parser and grammar share a source, so
adding the new words to the dictionary enables them on both sides at once. But
it implies that the change **is not only the parser's** — it must be verified
that `get_numeric_grammar_phrases()` includes the new hundreds and multipliers.

---

## Recommendation

Go with **option 2**, in this order:

1. Add hundreds and multipliers to the `Numbers` dictionary, in the three
   languages.
2. Confirm that `get_numeric_grammar_phrases()` returns them (if it builds the
   list from the full map, it comes for free).
3. Replace `_MergeTensAndUnits` with a positional accumulator.
4. **Keep the digit-by-digit mode**, which works today and may have people
   using it: the accumulator should recognize both forms.

Point 4 is the one that demands the most care. Today `uno cero cero` gives 100
by concatenation; a naive positional accumulator would interpret it as
1 + 0 + 0 = 1. It must be decided explicitly how each mode coexists before
touching the parser.

---

## Current impact

No command is blocked — every value can be spelled out — but there are cases
where it shows:

| Case | Today | With the proposal |
|---|---|---|
| 360° circular pattern | `tres seis cero` | `trescientos sesenta` |
| 150 mm dimension | `uno cinco cero` | `ciento cincuenta` |
| Measurements 0–99 | already natural | same |

In the meantime, the test guides use values below 100 so that the example
phrases sound natural.
