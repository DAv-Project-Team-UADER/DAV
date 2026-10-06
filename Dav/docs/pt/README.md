# Documentação do DAV (Português)

**DAV — Design Assistido por Voz** (*Diseño Asistido por Voz*) é uma camada de controle por voz sobre o [FreeCAD](https://www.freecad.org/) que usa o [Vosk](https://alphacephei.com/vosk/) como reconhecedor. Esta pasta reúne a documentação de **desenvolvimento** do projeto, para quem quiser entender como ele é feito, instalá-lo a partir do código ou contribuir.

> Se você só quer usar o DAV, o material para usuários está no [README principal](../../../README.pt.md) (manual do usuário e videotutoriais).

Esta documentação também existe em [Español](../es/README.md) e [English](../en/README.md).

---

## Por onde começar

| Se você quer... | Leia |
|---|---|
| Entender o projeto e como se trabalha nele | [Guia de desenvolvimento](guia-desenvolvimento-dav.md) |
| Saber o que há em cada pasta do repositório | [Estrutura do repositório](desenvolvimento/estrutura.md) |
| Rodar o DAV a partir do código | [Configuração (setup)](desenvolvimento/setup.md) |
| Instalar o DAV | [Windows](guia-instalacao-Windows.md) · [Linux](guia-instalacao-Linux.md) |
| Ver as classes e como se relacionam | [Diagramas de classes](diagramas/README.md) |

## Desenvolvimento

- [Convenções de código](desenvolvimento/convencoes.md): nomes, cabeçalho de licença, docstrings e princípios de design.
- [Adicionar um comando de voz](desenvolvimento/adicionar-comando.md)
- [Adicionar um submenu](desenvolvimento/adicionar-submenu.md)
- [Adicionar um diálogo de voz](desenvolvimento/adicionar-prompt.md)
- [Como testar e validar](desenvolvimento/testando.md)
- [Portar o DAV para um novo idioma](portar-para-novo-idioma.md)
- [Regenerar o manual do usuário em PDF](regenerar-manual-pdf.md)
- [GitFlow: o histórico real do repositório](gitflow-gitgraph.md)

## Como funciona o reconhecimento de voz

- [Dicionário de números e sua gramática](numeros-dicionario-gramatica.md)
- [Números por voz: limites e proposta](numeros-por-voz-limites-e-proposta.md)
- [Encurtador de gramática do Vosk](encurtador-gramatica-vosk.md)

## Manuais e guias de uso por voz

- [Manual do Explorer](manual-explorer-voz.md)
- [Manual de seleção por voz](manual-selecao-voz.md)
- [Manual de esboço e gravação por voz](manual-esboco-e-gravacao-voz.md)
- [Guia da tesoura](guia-tesoura-voz.md)

## Testes e relatórios

- [Testes de PartDesign por voz](guia-testes-partdesign-voz.md)
- [Testes 3D por voz](guia-testes-3d-voz.md)
- [Teste de números com alunos](guia-teste-numeros-alunos.md)
- [Relatório de testes da bancada Draft](relatorio_testes_draftwork.md)

## Estado e planejamento

- [Concluídos](concluidos-dav.md): problemas já resolvidos e sua causa real.
- [Plano de unificação das GUIs](plano-unificacao-guis.md)
- [Plano de migração do thread de voz para QThread](plano-migracao-threads-qthread.md)
- [Plano da árvore de objetos navegável](plano_arvore_de_objetos_navegavel.md)

## Documentos institucionais e legais

Ainda não há tradução para o português; os originais estão em outras pastas:

- Normativas: [espanhol](../es/normativas/) · [inglês](../en/regulations/)
- Licença GPL v3: [espanhol](../es/licencias/) · [inglês](../en/licenses/)
- [Protótipos de integração](prototipos/) (arquivado).

## Outros recursos desta pasta

- [`../assets/`](../assets/): gráfico do GitFlow e apresentação de exemplos.
- [`../ejemplo-tijeras/`](../ejemplo-tijeras/): arquivos do exemplo da tesoura.
- [`../manual/`](../manual/): scripts que geram os manuais em PDF.
