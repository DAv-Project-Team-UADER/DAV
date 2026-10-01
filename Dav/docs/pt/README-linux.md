# Documentação do Script de Inicialização (`inicio_dav.sh`)

## Descrição Geral
Este script Bash automatiza a preparação do ambiente e o lançamento do FreeCAD para o banco de trabalho (Workbench) personalizado **DAV**. Sua função principal é vincular o seu código de desenvolvimento diretamente aos arquivos locais do FreeCAD por meio de um link simbólico e executar a aplicação automaticamente, adaptando-se ao diretório pessoal de qualquer usuário.

---

## Pré-requisitos
* **Sistema Operacional:** Ubuntu / Linux.
* **Localização do FreeCAD:** O script assume que o executável do FreeCAD está salvo na pasta de downloads padrão em espanhol do usuário que o executa (`$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage`).
* **Contexto de execução:** O script **deve** ser executado a partir do diretório raiz do seu projeto (o diretório que contém a pasta `Dav`), pois utiliza `$(pwd)` (Print Working Directory) para montar o caminho.
* **Permissões:** O script precisa de permissões de execução no sistema.

---

## Modo de Uso

1. Abra um terminal.
2. Navegue até o diretório raiz onde se encontram o seu projeto e este script:
   ```bash
   cd /ruta/a/tu/proyecto
   ```
3. Conceda permissões de execução ao script (só é necessário fazer isso na primeira vez):
   ```bash
   chmod +x inicio_dav.sh
   ```
4. Execute o script:
   ```bash
   ./inicio_dav.sh
   ```

---

## Explicação Passo a Passo do Código

### 1. Variáveis de Ambiente (Cores)
```bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
```
Define variáveis para imprimir mensagens com cores no terminal (verde para sucessos, amarelo para avisos, NC para voltar à cor padrão).

### 2. Diretório de Módulos (Mod) do FreeCAD
```bash
MOD_DIR="$HOME/.local/share/FreeCAD/v1-1/Mod"
mkdir -p "$MOD_DIR"
```
Estabelece o caminho para a pasta de complementos (Mods) específicos da versão 1.1 do FreeCAD no Linux. O comando `mkdir -p` cria o diretório caso ele ainda não exista, evitando erros.

### 3. Resolução de Caminhos e Validação
```bash
WORKBENCH_PATH="$(pwd)/Dav/scr/ComponentesDAV/Dav"

if [ -f "$WORKBENCH_PATH/InitGui.py" ]; then
    echo "¡InitGui.py encontrado correctamente!"
else
    echo -e "${YELLOW}Advertencia: No se ve el InitGui.py en la ruta esperada.${NC}"
fi
```
Pega o caminho atual onde você está executando o script (`$(pwd)`) e acrescenta o path até a subpasta final do seu Workbench.
Em seguida verifica (`[ -f ... ]`) se o arquivo crítico `InitGui.py` existe ali. Isso é uma barreira de segurança para avisar caso você esteja executando o script a partir de uma pasta errada.

### 4. Criação do Link Simbólico
```bash
ln -sfn "$WORKBENCH_PATH" "$MOD_DIR/DAV"
```
Cria um "atalho" (link simbólico) do seu código-fonte para a pasta `Mod` do FreeCAD. 
* `-s`: Cria um link simbólico (não físico).
* `-f`: Força a criação (sobrescreve se já existia).
* `-n`: Trata o destino como um arquivo normal (evita aninhar links se for executado várias vezes).
* **Benefício:** Qualquer mudança que você salvar no seu código Python será refletida no FreeCAD na próxima vez que você iniciá-lo, sem ter que copiar ou mover arquivos manualmente.

### 5. Lançamento Universal do FreeCAD
```bash
"$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"
```
Chama e executa diretamente o arquivo AppImage. Ao usar a variável de ambiente `$HOME` em vez de um caminho rígido, o script se torna universal: funcionará para qualquer usuário, desde que ele tenha o arquivo em sua pasta "Descargas".

---

## Possíveis Problemas e Soluções (Troubleshooting)

| Problema | Causa provável | Solução |
| :--- | :--- | :--- |
| **"Advertencia: No se ve el InitGui.py..."** | Você está executando o script a partir de uma pasta incorreta. | Use `cd` para ir à pasta raiz do seu projeto antes de rodar `./inicio_dav.sh`. |
| **"Permissão negada" (Permission denied)** | O script ou a AppImage não são executáveis. | Rode `chmod +x inicio_dav.sh` e `chmod +x "$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"`. |
| **"Arquivo ou diretório inexistente" ao lançar o FreeCAD** | O usuário tem o sistema em inglês ou português (`Downloads` em vez de `Descargas`) ou o arquivo tem outro nome/versão. | Renomeie a pasta de downloads no script ou verifique que o arquivo do FreeCAD 1.1.3 esteja exatamente ali. |
