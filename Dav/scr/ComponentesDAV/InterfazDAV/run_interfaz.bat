@echo off
REM Lanza la interfaz DAV en modo visor pasivo de historial.
REM Las rutas se resuelven desde la ubicacion de este .bat (%~dp0),
REM asi funciona en cualquier maquina sin editar el archivo.

set DAV_PASSIVE_HISTORY_VIEWER=1

set "INTERFAZ_DIR=%~dp0"
set "COMPONENTES_DIR=%INTERFAZ_DIR%.."
set "PYTHONW=%COMPONENTES_DIR%\IntegracionGUI\GUIFreeCad\.venv\Scripts\pythonw.exe"

cd /d "%INTERFAZ_DIR%"

if not exist "%PYTHONW%" (
    echo [DAV] No se encontro el venv en:
    echo     %PYTHONW%
    echo [DAV] Crealo con: python -m venv .venv  dentro de IntegracionGUI\GUIFreeCad
    pause
    exit /b 1
)

start "" "%PYTHONW%" "%INTERFAZ_DIR%main.py"
