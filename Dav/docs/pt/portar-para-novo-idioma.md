# Fluxo de trabalho para portar o DAV para um novo idioma (hipotético)

> Este documento é uma **proposta**: descreve como seria feito, com a arquitetura atual,
> para adicionar um quarto idioma (por exemplo francês, `fr`) aos três que hoje o DAV suporta
> (espanhol, inglês e português). Não é um procedimento testado de ponta a ponta.

Um idioma no DAV tem quatro peças: o **modelo de reconhecimento** (Vosk), as **frases e
nomes** de cada comando (`TraduceTo*.py`), os **textos da interface e dos diálogos**
e a **documentação** (incluindo o manual em PDF).

## 0. Decidir o escopo

- Código ISO 639-1 do idioma (`fr`) e se há variante regional (`pt` vs `pt-br`).
- Confirmar que existe um modelo Vosk utilizável (passo 1). Sem modelo não há voz: o resto
  serve apenas para a interface escrita.

## 1. Escolher o modelo de voz

1. Acessar a página de modelos do Vosk: **<https://alphacephei.com/vosk/models>**.
2. Procurar o idioma. Convém um par de modelos, como nos demais idiomas:
   - um **pequeno** (dezenas de MB, `vosk-model-small-<idioma>-…`), que viaja com o projeto;
   - um **grande** (centenas de MB a GB), que é baixado sob demanda.
3. Revisar a licença de cada modelo (quase todos são Apache 2.0, mas há exceções) e anotar
   a versão exata.
4. Testá-lo sem o DAV com o exemplo do Vosk (`vosk-transcriber` ou um script de `KaldiRecognizer`) e
   confirmar que reconhece bem os números e os termos de CAD nesse idioma. A precisão com
   frases curtas e números decide se o idioma é viável.

## 2. Registrar o idioma no código

| Onde | O que mudar |
|---|---|
| [`core/language_code.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/language_code.py) | Adicionar o membro (`Fr = "fr"`) e seu sufixo `TraduceToFr` em `TranslateModuleSuffix` / `AlternateTranslateSuffixes` |
| [`core/model_manager.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/model_manager.py) | Adicionar `"fr": (pequeno, grande)` a `MODEL_CATALOG` |
| [`core/settings.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/core/settings.py) | Aceitar `"fr"` na validação da preferência de idioma |
| [`InputPrompts/InputPromptI18n.py`](../../scr/ComponentesDAV/IntegracionGUI/GUIFreeCad/InputPrompts/InputPromptI18n.py) | Reconhecer `fr` ao normalizar o código e devolvê-lo |
| `InputPrompts/SpokenNumberParser.py`, `PlaneGrammarSwitcher.py` | Números falados e gramática de planos do novo idioma |
| Seletor de idioma em Preferências | Adicionar a opção (veja [`Preferences`](diagramas/Preferences.md)) |

Buscar com `grep -rn "\"pt\"" Dav/scr` (e `'pt'`) para encontrar os lugares que enumeram os
idiomas e que não tenham sido listados acima. Os testes existentes que percorrem os três idiomas falharão
até que o novo esteja completo: servem como lista de pendências.

## 3. Traduzir os dicionários de comandos

Cada pasta de `Dav/dic/` tem um `TraduceToEs.py`, `TraduceToEn.py` e `TraduceToPt.py`.

1. Criar `TraduceToFr.py` em **cada** pasta (hoje são ~130), partindo da cópia do
   inglês ou do espanhol. Um script que percorra a árvore e copie o arquivo base acelera o passo.
2. Traduzir as **frases faladas** e os nomes dos comandos. Critérios:
   - frases curtas, naturais e distintas entre si (o modelo confunde as parecidas);
   - sem ambiguidade com números ou outros comandos do mesmo contexto;
   - validá-las contra o vocabulário do modelo escolhido: uma palavra fora do vocabulário
     nunca será reconhecida (veja [`encurtador-gramatica-vosk`](encurtador-gramatica-vosk.md)).
3. Respeitar a normalização de frases (`DictionaryLoader.NormalizeSpoken`: minúsculas, sem acentos).
4. Rodar os testes de dicionários reais para detectar chaves faltantes ou frases repetidas
   (veja [`testando`](desenvolvimento/testando.md)).

As chaves e a estrutura dos dicionários não mudam; só são adicionados arquivos.

## 4. Traduzir textos de interface e diálogos

- Os diálogos com parâmetros (números, planos, sim/não, exemplos guiados) têm textos por idioma
  em suas classes de `InputPrompts/` e nos exemplos de `dic/Explorer/Examples/`.
- Adicionar a tradução em cada tupla ou dicionário que hoje tem `es`/`en`/`pt`.
- Revisar os títulos dos painéis e as mensagens de estado.

## 5. Documentação e manual em PDF

1. Criar `Dav/docs/fr/` com os mesmos arquivos e nomes que `es/` e `en/` (a lista de
   arquivos é obtida com `find Dav/docs/es -type f`). Pode-se partir da tradução
   automática e revisá-la; as frases que são ditas ao modelo são deixadas no idioma do modelo.
2. Adicionar o idioma a `Dav/docs/manual/`: uma coluna a mais nas tuplas dos `desc_*.py`
   e em `textos.py`, e o idioma em `IDIOMAS`/`IDX` de `build_manual.py` (veja
   [regenerar o manual em PDF](regenerar-manual-pdf.md)).
3. Adicionar um `README.fr.md` na raiz, como os `README.es.md` e `README.pt.md`.
4. Atualizar o índice [`Dav/docs/README.md`](../README.md).

## 6. Verificação e entrega

- [ ] O modelo pequeno está em `Dav/models/` e o grande é baixado pelas Preferências.
- [ ] Mudar o idioma nas Preferências carrega a gramática e o modelo corretos.
- [ ] Todos os comandos têm frase no novo idioma (os testes de dicionários passam).
- [ ] Um falante nativo percorre as guias de teste (`guia-pruebas-*.md`) e anota as frases
      que não são reconhecidas.
- [ ] O manual em PDF do idioma é gerado sem avisos de comandos sem descrição.
- [ ] Foram documentadas a versão do modelo e sua licença.

## Sugestão de branches e PR

Seguir o [GitFlow do projeto](gitflow-gitgraph.md) com uma branch `feature/idioma-fr` e PRs
pequenos: (1) registro do idioma e modelo, (2) dicionários, (3) interface e diálogos,
(4) documentação e manual.
