# Documentación del Script de Arranque (`inicio_dav.sh`)

## Descripción General
Este script de Bash automatiza la preparación del entorno y el lanzamiento de FreeCAD para el banco de trabajo (Workbench) personalizado **DAV**. Su función principal es vincular tu código de desarrollo directamente con los archivos locales de FreeCAD mediante un enlace simbólico y ejecutar la aplicación de forma automática, adaptándose al directorio personal de cualquier usuario.

---

## Requisitos Previos
* **Sistema Operativo:** Ubuntu / Linux.
* **Ubicación de FreeCAD:** El script asume que el ejecutable de FreeCAD está guardado en la carpeta de descargas predeterminada en español del usuario que lo ejecuta (`$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage`).
* **Contexto de ejecución:** El script **debe** ejecutarse desde el directorio raíz de tu proyecto (el directorio que contiene la carpeta `Dav`), ya que utiliza `$(pwd)` (Print Working Directory) para armar la ruta.
* **Permisos:** El script necesita permisos de ejecución en el sistema.

---

## Modo de Uso

1. Abre una terminal.
2. Navega hasta el directorio raíz donde se encuentra tu proyecto y este script:
   ```bash
   cd /ruta/a/tu/proyecto
   ```
3. Otorga permisos de ejecución al script (solo es necesario hacerlo la primera vez):
   ```bash
   chmod +x inicio_dav.sh
   ```
4. Ejecuta el script:
   ```bash
   ./inicio_dav.sh
   ```

---

## Explicación Paso a Paso del Código

### 1. Variables de Entorno (Colores)
```bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
```
Define variables para imprimir mensajes con colores en la terminal (verde para éxitos, amarillo para advertencias, NC para resetear al color por defecto).

### 2. Directorio de Módulos (Mod) de FreeCAD
```bash
MOD_DIR="$HOME/.local/share/FreeCAD/v1-1/Mod"
mkdir -p "$MOD_DIR"
```
Establece la ruta a la carpeta de complementos (Mods) específicos para la versión 1.1 de FreeCAD en Linux. El comando `mkdir -p` crea el directorio si este aún no existe, evitando errores.

### 3. Resolución de Rutas y Validación
```bash
WORKBENCH_PATH="$(pwd)/Dav/scr/ComponentesDAV/Dav"

if [ -f "$WORKBENCH_PATH/InitGui.py" ]; then
    echo "¡InitGui.py encontrado correctamente!"
else
    echo -e "${YELLOW}Advertencia: No se ve el InitGui.py en la ruta esperada.${NC}"
fi
```
Toma la ruta actual donde estás ejecutando el script (`$(pwd)`) y le anexa el path hacia la subcarpeta final de tu Workbench.
Luego comprueba (`[ -f ... ]`) si el archivo crítico `InitGui.py` existe ahí. Esto es una barrera de seguridad para avisarte si estás ejecutando el script desde una carpeta equivocada.

### 4. Creación del Enlace Simbólico
```bash
ln -sfn "$WORKBENCH_PATH" "$MOD_DIR/DAV"
```
Crea un "acceso directo" (enlace simbólico) de tu código fuente hacia la carpeta `Mod` de FreeCAD. 
* `-s`: Crea un enlace simbólico (no físico).
* `-f`: Fuerza la creación (sobreescribe si ya existía).
* `-n`: Trata el destino como un archivo normal (evita que anide enlaces si se ejecuta múltiples veces).
* **Beneficio:** Cualquier cambio que guardes en tu código de Python se reflejará en FreeCAD la próxima vez que inicies, sin tener que copiar o mover archivos manualmente.

### 5. Lanzamiento Universal de FreeCAD
```bash
"$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"
```
Llama y ejecuta directamente el archivo AppImage. Al usar la variable de entorno `$HOME` en lugar de una ruta rígida, el script se vuelve universal: funcionará para cualquier usuario siempre y cuando tengan el archivo en su carpeta de "Descargas".

---

## Posibles Problemas y Soluciones (Troubleshooting)

| Problema | Causa probable | Solución |
| :--- | :--- | :--- |
| **"Advertencia: No se ve el InitGui.py..."** | Estás ejecutando el script desde una carpeta incorrecta. | Usa `cd` para ir a la carpeta raíz de tu proyecto antes de correr `./inicio_dav.sh`. |
| **"Permiso denegado" (Permission denied)** | El script o la AppImage no son ejecutables. | Corre `chmod +x inicio_dav.sh` y `chmod +x "$HOME/Descargas/FreeCAD_1.1.3-Linux-x86_64-py311.AppImage"`. |
| **"No existe el archivo o el directorio" al lanzar FreeCAD** | El usuario tiene el sistema en inglés (`Downloads` en vez de `Descargas`) o el archivo tiene otro nombre/versión. | Renombra la carpeta de descargas en el script o verifica que el archivo de FreeCAD 1.1.3 esté exactamente ahí. |