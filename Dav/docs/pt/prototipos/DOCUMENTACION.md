# Documentação de `PruebaIntegracion`

## 1. Propósito do módulo

`PruebaIntegracion` é uma implementação de integração para o projeto DAV focada na navegação por voz e na execução de ações a partir de uma estrutura hierárquica de contexto. Sua função é unir três partes que no repositório apareciam separadas ou incompletas:

1. Captura e filtragem de voz.
2. Busca de comandos dentro de uma árvore de contextos.
3. Execução segura de funções com validação de parâmetros.

A pasta foi pensada como um espaço de trabalho autocontido para levar a código a ideia descrita em `IDEAS/IDEA DE DAVCORE IMPLEMENTATION/EXPLICACION.txt`, sem interferir nas outras variantes do repositório.

## 2. Relação com o projeto

A utilidade concreta desta seção para o projeto é a seguinte:

- Permite definir ferramentas por contexto, não como uma lista plana de comandos.
- Torna possível traduzir palavras faladas para nomes reais de funções ou subcontextos.
- Centraliza a validação de parâmetros antes de executar uma ação.
- Separa a lógica de reconhecimento de voz da lógica de negócio.
- Deixa uma base clara para crescer de uma demo local até uma integração real com `VoskModel` e pastas dinâmicas em `dic/`.

Em termos funcionais, `PruebaIntegracion` representa o núcleo conceitual do futuro `DAVCore`.

## 3. Estrutura desenvolvida

Os módulos principais desenvolvidos dentro de `PruebaIntegracion` são:

- `core/ParamSpec.py`
- `core/EnvoltorioFuncion.py`
- `core/NodoContexto.py`
- `core/Navegador.py`
- `core/Comando.py`
- `core/ExploradorVoz.py`
- `core/CargadorConTraducciones.py`
- `main.py`

Além disso, o fluxo usa:

- `modelo/VoskModel.py` para o reconhecimento de voz real.
- `dic/` como pasta de módulos carregáveis dinamicamente.
- `idiomas/` como espaço preparado para traduções por idioma.

## 4. Mapa de responsabilidades

### 4.1 `ParamSpec`

Arquivo: [PruebaIntegracion/core/ParamSpec.py](../../prototipos/PruebaIntegracion/core/ParamSpec.py)

Sua tarefa é descrever como deve ser um parâmetro de uma função.

#### O que resolve

Sem esta classe, cada função teria sua própria validação manual. Com `ParamSpec`, a validação fica declarada de forma uniforme e reutilizável.

#### Atributos principais

- `nombre`: nome lógico do parâmetro.
- `tipo`: tipo esperado, por exemplo `int`, `float`, `str` ou uma tupla de tipos.
- `requerido`: indica se o argumento é obrigatório.
- `longitud_maxima`: limite para cadeias de texto.
- `valores_permitidos`: conjunto fechado de valores válidos.

#### Método-chave

- `validar(valor, nombre_argumento=None)`: verifica o valor recebido e lança um erro claro se não cumprir.

#### Utilidade no projeto

`ParamSpec` é a base da validação de entrada. Dá ao sistema uma forma declarativa de dizer: "esta função espera um float obrigatório" ou "este texto não pode superar certo comprimento".

### 4.2 `EnvoltorioFuncion`

Arquivo: [PruebaIntegracion/core/EnvoltorioFuncion.py](../../prototipos/PruebaIntegracion/core/EnvoltorioFuncion.py)

Envolve uma função real para inspecionar sua assinatura, validar argumentos e executá-la de forma controlada.

#### O que resolve

O projeto precisa de uma camada intermediária entre o comando falado e a função concreta. Essa camada precisa saber:

- quais parâmetros a função espera,
- em que ordem,
- se precisa de `context_keys`,
- e como validar antes de executar.

#### Como funciona

1. Guarda a função original.
2. Lê sua assinatura com `inspect.signature`.
3. Obtém a lista de `ParamSpec` a partir do atributo `_param_specs` ou de uma lista explícita.
4. Verifica que cada `ParamSpec` realmente exista na assinatura.
5. Em `ejecutar()` faz `bind_partial()` sobre a assinatura.
6. Se a função aceita `context_keys`, injeta-os automaticamente.
7. Valida os argumentos com cada `ParamSpec`.
8. Se tudo estiver correto, invoca a função real.

#### Método-chave

- `obtener_orden_parametros()`: devolve a ordem original da assinatura.
- `ejecutar(*args, context_keys=None, **kwargs)`: valida e invoca.

#### Utilidade no projeto

Este módulo converte uma função comum em uma ferramenta segura para o sistema de voz. É a peça que torna possível invocar ações sem confiar cegamente no que foi ouvido.

### 4.3 `NodoContexto`

Arquivo: [PruebaIntegracion/core/NodoContexto.py](../../prototipos/PruebaIntegracion/core/NodoContexto.py)

Representa um nível de navegação dentro do sistema. Pode conter funções, subcontextos e traduções.

#### O que resolve

A aplicação não trabalha com um menu plano, e sim com uma hierarquia. `NodoContexto` modela essa árvore.

#### Estrutura interna

- `elementos`: dicionário de nomes reais para `EnvoltorioFuncion` ou `NodoContexto`.
- `traducciones`: dicionário de palavra falada para nome real.
- `parent`: referência ao nó pai.

#### Métodos-chave

- `agregar_funcion(clave, envoltorio)`: registra uma função.
- `agregar_subcontexto(clave, nodo)`: registra um subcontexto e conecta o pai.
- `agregar_traduccion(palabra_hablada, nombre_real)`: adiciona um sinônimo local.
- `obtener_nombre_real(palabra_hablada)`: resolve a tradução no nó atual.
- `obtener_todas_las_llaves()`: percorre as chaves reais locais.
- `obtener_hijo(clave)`: devolve um subcontexto se existir.

#### Utilidade no projeto

`NodoContexto` permite separar o vocabulário falado da estrutura interna real. Isso é útil para suportar vários idiomas, aliases ou palavras mais naturais para o usuário.

### 4.4 `Navegador`

Arquivo: [PruebaIntegracion/core/Navegador.py](../../prototipos/PruebaIntegracion/core/Navegador.py)

É o orquestrador da árvore de contextos. Mantém o contexto atual e resolve buscas ascendentes.

#### O que resolve

Quando o usuário fala a partir de um contexto, a aplicação deve saber se a palavra corresponde a uma função local ou a algo definido em um pai. `Navegador` concentra essa lógica.

#### Método-chave

- `establecer_contexto(nodo)`: muda o contexto atual.
- `navegar(ruta)`: desce por um caminho como `Dibujo-Geometria-Circulos`.
- `buscar_funcion_ascendente(nombre_real)`: busca a partir do contexto atual em direção à raiz.
- `llamar(nombre_real, *args, context_keys=None, **kwargs)`: busca a função e a executa.

#### Fluxo real

Quando `llamar()` encontra a função, atualiza `contexto_actual` para o nó onde foi encontrada. Isso permite que a navegação e a execução trabalhem sobre a mesma árvore sem duplicar estado.

#### Utilidade no projeto

`Navegador` é o ponto central de decisão para resolver nomes reais, subir pela árvore e executar ações sem perder a posição do usuário.

### 4.5 `Command`

Arquivo: [PruebaIntegracion/core/Comando.py](../../prototipos/PruebaIntegracion/core/Comando.py)

É o adaptador de entrada por voz. Recebe frases do modelo de voz e filtra somente as palavras que são permitidas no vocabulário ativo.

#### O que resolve

A intenção do sistema não é transcrever qualquer coisa, e sim reconhecer somente tokens úteis para o estado atual.

#### Características

- Tem vetores predefinidos por meio de `VECTORS`.
- Normaliza o texto removendo acentos e passando para minúsculas.
- Converte dígitos falados como `uno`, `dos`, `tres` em números.
- Detecta comandos especiais como `cancelar`, `enter` e `enviar`.
- Suporta tanto uso por índice quanto por lista personalizada de tokens.

#### Método-chave

- `exclusive_listen(vector)`: escuta até obter uma seleção válida ou um cancelamento.

#### Utilidade no projeto

`Command` faz o papel de filtro inteligente entre o áudio e a lógica do sistema. Sem esta camada, o explorador teria que interpretar frases ruidosas ou irrelevantes.

### 4.6 `ExploradorVoz`

Arquivo: [PruebaIntegracion/core/ExploradorVoz.py](../../prototipos/PruebaIntegracion/core/ExploradorVoz.py)

É o coordenador principal do comportamento. Cuida da navegação, da seleção de funções e da coleta de parâmetros.

#### O que resolve

Conecta todo o resto em uma máquina de estados simples:

- modo navegação,
- modo parâmetros,
- execução.

#### Atributos internos

- `voice_model`: fonte de áudio ou modelo de teste.
- `navegador`: instância de `Navegador`.
- `command`: instância de `Command`.
- `modo_parametros`: indica se está lendo uma função selecionada.
- `funcion_pendiente`: função envolvida que falta executar.
- `parametros_recolectados`: lista de valores capturados.

#### Métodos-chave

- `_obtener_nombre_real_ascendente(palabra)`: resolve traduções subindo na hierarquia.
- `_vocabulario_navegacion()`: monta o vocabulário ativo para navegação.
- `_parse_number(phrase)`: interpreta números falados de forma simples.
- `iniciar_parametros(envoltorio)`: muda para o modo parâmetros.
- `procesar_parametros()`: coleta valores e chama a função.
- `bucle_comando(max_iterations=None)`: loop principal.

#### Fluxo de integração

1. Obtém o vocabulário permitido conforme o contexto atual.
2. Chama `Command.exclusive_listen(...)`.
3. Traduz a palavra detectada para nome real.
4. Busca se esse nome corresponde a função ou subcontexto.
5. Se é função, entra em modo parâmetros.
6. Se a captura termina, executa com `Navegador.llamar()`.

#### Utilidade no projeto

É o módulo que transforma a infraestrutura de dados em comportamento interativo real.

### 4.7 `CargadorConTraducciones`

Arquivo: [PruebaIntegracion/core/CargadorConTraducciones.py](../../prototipos/PruebaIntegracion/core/CargadorConTraducciones.py)

Carregamento dinâmico de módulos a partir de `dic/` e construção da árvore de contextos.

#### O que resolve

Evita que a árvore de ferramentas tenha que ser escrita à mão dentro do código principal. Em vez disso, a estrutura pode ser mantida como arquivos soltos dentro de uma pasta.

#### Convenção usada

- Cada pasta representa um `NodoContexto`.
- Cada arquivo `TraduceTo*.py` pode expor um dicionário `TRADUCCIONES`.
- Cada arquivo `.py` restante é inspecionado em busca de funções com `_param_specs`.

#### Fluxo interno

1. Percorre a pasta `dic/`.
2. Cria um nó para cada subdiretório.
3. Importa módulos com `importlib.util.spec_from_file_location`.
4. Se encontra `TRADUCCIONES`, registra-as no nó.
5. Se encontra funções válidas, envolve-as com `EnvoltorioFuncion`.
6. Devolve um dicionário de raízes pronto para ser pendurado no nó principal.

#### Utilidade no projeto

Torna possível escalar o sistema sem modificar o núcleo cada vez que uma ferramenta nova é adicionada.

### 4.8 Exemplo real de `dic/`

Para que o carregador tenha conteúdo funcional, `PruebaIntegracion/dic/` já pode usar uma estrutura mínima como esta:

```text
PruebaIntegracion/dic/
	Demo/
		crear_punto.py
		TraduceToEs.py
```

Nesse exemplo:

- `crear_punto.py` define uma função `crear_punto(valor, context_keys=None)`.
- A função expõe `_param_specs` com `ParamSpec("valor", float)`.
- `TraduceToEs.py` declara `TRADUCCIONES = {"demo": "Demo", "crear punto": "crear_punto"}`.

Isso permite que o carregador:

1. Crie um `NodoContexto` chamado `Demo`.
2. Registre a tradução falada `demo -> Demo`.
3. Registre a tradução falada `crear punto -> crear_punto`.
4. Vincule a função real com `EnvoltorioFuncion`.
5. Permita que `ExploradorVoz` navegue até o contexto e execute a função.

Este caso serve como modelo para adicionar novas ferramentas reais sem mexer no núcleo.

## 5. Integração entre módulos

A relação entre os componentes é a seguinte:

- `ExploradorVoz` contém um `Command` e um `Navegador`.
- `Command` usa um `voice_model` para escutar.
- `Navegador` administra `NodoContexto`.
- `NodoContexto` contém `EnvoltorioFuncion` e outros `NodoContexto`.
- `EnvoltorioFuncion` valida com `ParamSpec`.
- `CargadorConTraducciones` constrói a árvore inicial.

Em outras palavras: o carregador cria a estrutura, o navegador a percorre, o comando filtra a voz e o explorador decide o que executar.

## 6. Fluxo de inicialização atual

Arquivo: [PruebaIntegracion/main.py](../../prototipos/PruebaIntegracion/main.py)

O `main` atual substitui a inicialização rígida por um fluxo mais flexível.

### O que faz

- Lê argumentos pelo console.
- Tenta carregar a árvore a partir de `dic/`.
- Se não há conteúdo, cria uma demo mínima com uma função de exemplo.
- Cria o `Navegador`.
- Instancia o modelo de voz real ou um modelo simulado de demo.
- Lança `ExploradorVoz.bucle_comando()`.

### Modo demo

O modo demo serve para testar o fluxo sem microfone nem modelo Vosk instalado. É especialmente útil para validar integração, navegação e execução básica.

## 7. Exemplo de uso

### Modo demo

```bash
python -m PruebaIntegracion.main --demo --max-iter 2
```

Esse modo usa um modelo simulado que devolve uma sequência de frases e permite confirmar que a árvore, a tradução e a execução funcionam.

### Modo real

```bash
python -m PruebaIntegracion.main --modelo MODELO\vosk-model-small-es-0.42
```

Nesse caso usa-se `VoskModel` e a entrada depende do microfone e da instalação de dependências.

## 8. Código de exemplo conceitual

A ideia central do sistema é esta sequência:

```python
raiz = construir_estructura_desde_diccionario()
navegador = Navegador(raiz)
explorador = ExploradorVoz(modelo_voz, navegador)
explorador.bucle_comando()
```

E dentro do explorador:

```python
token = command.exclusive_listen(vocabulario)
nombre_real = _obtener_nombre_real_ascendente(token)
encontrado = navegador.buscar_funcion_ascendente(nombre_real)
```

Esse pequeno ciclo resume a arquitetura completa: escutar, traduzir, buscar e executar.

## 9. Estado atual e limitações

### Estado atual

- A arquitetura principal está implementada.
- A inicialização tem modo demo funcional.
- O carregador já pode percorrer `dic/` e preparar uma árvore.
- A busca ascendente e a execução básica estão testadas.

### Limitações atuais

- `dic/` ainda está vazio, por isso o sistema usa um fallback de demo se não encontra módulos reais.
- A interpretação numérica de `ExploradorVoz` é simples e pode ser ampliada.
- `Command` e `ExploradorVoz` estão preparados para crescer, mas a semântica final depende dos módulos reais que forem adicionados em `dic/`.

## 10. Conclusão

`PruebaIntegracion` concentra a implementação prática do mapa descrito nos documentos de ideia. Seu valor para o projeto é que já não se trata apenas de uma explicação conceitual: agora existe uma base executável que mostra como traduzir a navegação por voz em uma árvore de contextos, como validar parâmetros antes de executar ações e como estender o sistema sem reescrever o núcleo.
