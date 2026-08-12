@echo off
setlocal
set DAV_PASSIVE_HISTORY_VIEWER=1
cd /d "%~dp0"
start "" "%~dp0..\IntegracionGUI\GUIFreeCad\.venv\Scripts\pythonw.exe" "%~dp0main.py"
