# Guia de testes — Entrada numérica por voz

> Para alunos: testar as funções que recebem valores numéricos por voz e detectar erros.

---

## Preparação

1. Abrir o FreeCAD com o projeto DAV
2. Iniciar o motor de voz: menu DAV → "Iniciar voz DAV" (ou pelo console: `from integration.voice_bootstrap import start_voice_engine; start_voice_engine()`)
3. Garantir que o microfone funcione
4. Ter um documento aberto no FreeCAD

---

## Funções com parâmetros numéricos

| # | Função | Caminho do dicionário | Parâmetros numéricos requeridos | Idiomas |
|---|---------|---------------------|--------------------------------|---------|
| 1 | `create_by_points` | `Workbench/Sketcher/Geometry/line` | `x1: float`, `y1: float`, `x2: float`, `y2: float` (4 floats) | ES, PT |
| 2 | `pointatcoords` | `Workbench/DraftWork/pointplacement` | `x: float`, `y: float`, `z: float` (3 floats) | ES, EN, PT |
| 3 | `_create_line` | `Workbench/Part/line` | `x1: float`, `y1: float`, `z1: float`, `x2: float`, `y2: float`, `z2: float` (6 floats) | ES, EN, PT |
| 4 | `pad_sketch` | `Workbench/PartDesign/additive` | `length: float = 10.0` (tem valor padrão, não requer entrada) | ES, EN, PT |

**Total: 13 parâmetros float requeridos em 3 funções navegáveis por voz.**

---

## Teste 1 — Sketcher Line (create by points)

### Navegação por voz

Dizer nesta ordem:

```
"workbench"
"sketcher"
"geometry"
"linea"
"linea por puntos"
```

### Valores a inserir

Quando o primeiro prompt abrir, dizer o número e depois confirmar:

| Prompt | Dizer | Confirmar com | Valor esperado |
|--------|-------|---------------|----------------|
| #1 (x1) | **"uno"** (um) | **"enviar"** (enviar) | 1.0 |
| #2 (y1) | **"dos"** (dois) | **"enviar"** | 2.0 |
| #3 (x2) | **"cinco"** (cinco) | **"enviar"** | 5.0 |
| #4 (y2) | **"tres"** (três) | **"enviar"** | 3.0 |

### Verificação

- Deveria ser criada uma linha de **(1, 2)** a **(5, 3)** no plano XY
- Verificar no FreeCAD: `App.ActiveDocument.Objects` deveria mostrar um objeto novo

---

## Teste 2 — Draft Point (pointatcoords)

### Navegação por voz

```
"workbench"
"draft"
"pointplacement"
"punto en coordenadas"
```

### Valores a inserir

| Prompt | Dizer | Confirmar com | Valor esperado |
|--------|-------|---------------|----------------|
| #1 (x) | **"tres"** (três) | **"ok"** | 3.0 |
| #2 (y) | **"cuatro"** (quatro) | **"ok"** | 4.0 |
| #3 (z) | **"cero"** (zero) | **"ok"** | 0.0 |

### Verificação

- Deveria ser criado um ponto nas coordenadas **(3, 4, 0)**

---

## Teste 3 — Part Line (_create_line)

### Navegação por voz

```
"workbench"
"part"
"linea"
"linea"
```

### Valores a inserir

| Prompt | Dizer | Confirmar com | Valor esperado |
|--------|-------|---------------|----------------|
| #1 (x1) | **"cero"** (zero) | **"enviar"** | 0.0 |
| #2 (y1) | **"cero"** | **"enviar"** | 0.0 |
| #3 (z1) | **"cero"** | **"enviar"** | 0.0 |
| #4 (x2) | **"diez"** (dez) | **"enviar"** | 10.0 |
| #5 (y2) | **"cinco"** (cinco) | **"enviar"** | 5.0 |
| #6 (z2) | **"cero"** | **"enviar"** | 0.0 |

### Verificação

- Deveria ser criada uma linha de **(0, 0, 0)** a **(10, 5, 0)**

---

## Casos especiais a testar

Testar estes casos em qualquer uma das funções anteriores:

| # | Caso | O que fazer | Resultado esperado |
|---|------|-----------|--------------------|
| 1 | **Decimal com ponto** | Dizer "tres punto cinco" → "enviar" | Aceita 3.5 |
| 2 | **Decimal com vírgula** | Dizer "dos coma ocho" → "enviar" | Aceita 2.8 |
| 3 | **Confirmar com "ok"** | Dizer "ocho" → "ok" | Aceita 8.0 |
| 4 | **Cancelar** | Dizer "cancelar" | Fecha o prompt sem aceitar valor |
| 5 | **Só "ok"** | Dizer "ok" sem dizer número antes | Mostra "No value to confirm" |
| 6 | **Número composto (11-19)** | Dizer "trece" → "enviar" | Aceita 13.0 |
| 6b | **Dezena sozinha (20-90)** | Dizer "cuarenta" → "enviar" | Aceita 40.0 |
| 6c | **Dezena + unidade** | Dizer "treinta y dos" → "enviar" | Aceita 32.0 (testar também sem o "y": "treinta dos") |
| 6d | **Contração espanhola (21-29)** | Dizer "veintidós" → "enviar" | Aceita 22.0 |
| 6e | **Dígito a dígito (reserva)** | Dizer "uno" "uno" → "enviar" | Aceita 11.0 (continua funcionando como alternativa) |
| 6f | **Fora de faixa (100+)** | Dizer "seiscientos cincuenta" → "enviar" | NÃO suportado (faixa atual: 0-99). "seiscientos" não está no dicionário e é ignorado em silêncio: dá **50**, não um erro. Reportar se isto surpreender no teste |
| 7 | **Duas utterances** | Dizer "cinco" → "ok" | Aceita 5.0 (acumula + confirma) |

---

## O que observar

Para cada teste, observar e anotar:

1. **O prompt abriu?** — Aparece a janela pop-up pedindo valor
2. **O número foi reconhecido?** — O campo de texto mostra o que você disse
3. **A confirmação funcionou?** — Ao dizer "enviar" ou "ok" o valor é aceito
4. **Passou ao próximo parâmetro?** — Abre-se o prompt para o próximo float
5. **A função foi executada?** — O objeto é criado no FreeCAD
6. **O objeto está correto?** — Coordenadas e forma corretas

---

## Formato de relatório

Preencher uma linha para cada função testada:

```
Função: _______________________
Comando de voz: _______________________

O prompt abriu?               SIM / NÃO
Números reconhecidos:         _______________
Números NÃO reconhecidos:     _______________
A função foi executada?       SIM / NÃO
O objeto foi criado corretamente? SIM / NÃO

Erros observados:
_________________________________________________
_________________________________________________
```

---

## Erros conhecidos — o que procurar

| Mensagem de erro | Causa provável | Severidade |
|-----------------|----------------|-----------|
| `"Command not executed: Collected parameters failed validation"` | O wrapper não repassa parâmetros à função | Alta |
| `"No se pudo convertir 'x1' al tipo un número decimal"` | A gramática numérica não foi carregada; o Vosk não escuta números | Alta |
| O número é substituído por outra palavra (ex: "ocho" → "opciones") | A gramática não mudou para modo numérico | Alta |
| `"ok" no confirma el número** | O prompt substitui o texto em vez de acumulá-lo | Média |
| O prompt não aparece | O comando não é navegável por voz | Alta |
| O Vosk não reconhece o número em nenhum idioma | A palavra não está na gramática numérica | Média |
| `"Value cannot be empty"` | Confirmou-se sem inserir número | Baixa |
| A função executa mas não cria objeto | Erro na implementação da função | Alta |

---

## Dicas

- **Falar claro e pausado** — O Vosk funciona melhor com dicção clara
- **Esperar o prompt aparecer** — Não falar antes de a janela estar visível
- **Dizer número e confirmação separadamente** — Primeiro "cinco", esperar, depois "enviar"
- **Se um número não for reconhecido, repeti-lo** — Às vezes o Vosk falha por ruído
- **Testar com os 3 idiomas** se possível — Mudar o idioma pelas preferências do DAV
