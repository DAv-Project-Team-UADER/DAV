@echo off
rem Lanza la InterfazDAV standalone usando rutas relativas al propio .bat.
rem %~dp0 = carpeta de este script (...\Dav\scr\ComponentesDAV\InterfazDAV\).
setlocal
set "HERE=%~dp0"
cd /d "%HERE%"

rem Python del venv de GUIFreeCad (hermano de InterfazDAV en IntegracionGUI).
set "VENV1=%HERE%..\IntegracionGUI\GUIFreeCad\.venv\Scripts\pythonw.exe"
if exist "%VENV1%" (
    set "PYW=%VENV1%"
) else (
    set "PYW=pythonw.exe"
)

start "" "%PYW%" "%HERE%main.py"
endlocal
