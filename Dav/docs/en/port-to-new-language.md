# Workflow for porting DAV to a new language (hypothetical)

> This document is a **proposal**: it describes how it would be done, with the current architecture,
> to add a fourth language (for example French, `fr`) to the three DAV supports today
> (Spanish, English and Portuguese). It is not an end-to-end tested procedure.

A language in DAV has four pieces: the **recognition model** (Vosk), the **phrases and
names** of each command (`TraduceTo*.py`), the **interface and dialog texts**
and the **documentation** (including the PDF manual).

## 0. Decide the scope

- ISO 639-1 code of the language (`fr`) and whether there is a regional variant (`pt` vs `pt-br`).
- Confirm that a usable Vosk model exists (step 1). Without a model there is no voice: the rest
  only serves the written interface.

## 1. Choose the voice model

1. Go to the Vosk models page: **<https://alphacephei.com/vosk/models>**.
2. Look for the language. A pair of models is advisable, as for the other languages:
   - a **small** one (tens of MB, `vosk-model-small-<language>-…`), which ships with the project;
   - a **large** one (hundreds of MB to GB), which is downloaded on demand.
3. Check the license of each model (almost all are Apache 2.0, but there are exceptions) and note
   the exact version.
4. Try it without DAV using the Vosk example (`vosk-transcriber` or a `KaldiRecognizer` script) and
   confirm that it recognizes numbers and CAD terms well in that language. Accuracy with
   short phrases and numbers decides whether the language is viable.

## 2. Register the language in the code

| Where | What to change |
|---|---|
| [`core/language_code.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/language_code.py) | Add the member (`Fr = "fr"`) and its `TraduceToFr` suffix in `TranslateModuleSuffix` / `AlternateTranslateSuffixes` |
| [`core/model_manager.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/model_manager.py) | Add `"fr": (small, large)` to `MODEL_CATALOG` |
| [`core/settings.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/settings.py) | Accept `"fr"` in the language preference validation |
| [`InputPrompts/InputPromptI18n.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/InputPromptI18n.py) | Recognize `fr` when normalizing the code and return it |
| `InputPrompts/SpokenNumberParser.py`, `PlaneGrammarSwitcher.py` | Spoken numbers and plane grammar of the new language |
| Language selector in Preferences | Add the option (see [`Preferences`](diagrams/Preferences.md)) |

Search with `grep -rn "\"pt\"" Dav/scr` (and `'pt'`) to find the places that enumerate the
languages and were not listed above. The existing tests that go through the three languages will fail
until the new one is complete: they work as a to-do list.

## 3. Translate the command dictionaries

Each folder in `Dav/dic/` has a `TraduceToEs.py`, `TraduceToEn.py` and `TraduceToPt.py`.

1. Create `TraduceToFr.py` in **each** folder (today there are ~130), starting from a copy of the
   English or Spanish one. A script that walks the tree and copies the base file speeds this step up.
2. Translate the **spoken phrases** and the command names. Criteria:
   - short, natural phrases that differ from each other (the model confuses similar ones);
   - no ambiguity with numbers or other commands in the same context;
   - validate them against the vocabulary of the chosen model: a word outside the vocabulary
     will never be recognized (see [`vosk-grammar-shortener`](vosk-grammar-shortener.md)).
3. Respect phrase normalization (`DictionaryLoader.NormalizeSpoken`: lowercase, no accents).
4. Run the real-dictionary tests to detect missing keys or repeated phrases
   (see [`testing`](development/testing.md)).

The keys and the structure of the dictionaries do not change; only files are added.

## 4. Translate interface and dialog texts

- The dialogs with parameters (numbers, planes, yes/no, guided examples) have per-language texts
  in their `InputPrompts/` classes and in the examples under `dic/Explorer/Examples/`.
- Add the translation to each tuple or dictionary that today has `es`/`en`/`pt`.
- Review the panel titles and the status messages.

## 5. Documentation and PDF manual

1. Create `Dav/docs/fr/` with the same files and names as `es/` and `en/` (the file
   list is obtained with `find Dav/docs/es -type f`). You can start from machine
   translation and review it; the phrases that are spoken to the model are left in the model's language.
2. Add the language to `Dav/docs/manual/`: one more column in the tuples of the `desc_*.py`
   and in `textos.py`, and the language in `IDIOMAS`/`IDX` of `build_manual.py` (see
   [regenerating the PDF manual](regenerate-user-manual-pdf.md)).
3. Add a `README.fr.md` at the root, like `README.es.md` and `README.pt.md`.
4. Update the index [`Dav/docs/README.md`](../README.md).

## 6. Verification and delivery

- [ ] The small model is in `Dav/models/` and the large one is downloaded from Preferences.
- [ ] Changing the language in Preferences loads the correct grammar and model.
- [ ] All commands have a phrase in the new language (the dictionary tests pass).
- [ ] A native speaker goes through the test guides (`guia-pruebas-*.md`) and notes the phrases
      that are not recognized.
- [ ] The language's PDF manual is generated with no warnings about commands without description.
- [ ] The model version and its license were documented.

## Suggested branches and PRs

Follow the [project's GitFlow](gitflow-gitgraph.md) with a `feature/idioma-fr` branch and small
PRs: (1) language and model registration, (2) dictionaries, (3) interface and dialogs,
(4) documentation and manual.
