;  DAV (UADER) - Instalador para FreeCAD
;  Compilar con Inno Setup (https://jrsoftware.org/isinfo.php)
; ============================================================
;
;  UBICACIÓN DE ESTE ARCHIVO EN EL REPO:
;  Este .iss está pensado para vivir dentro de una carpeta "installer\"
;  al mismo nivel que "Dav\", por ejemplo:
;
;    DavCore\
;      Dav\             <- Init.py, InitGui.py, scr\, etc.
;      installer\
;        DAV_Setup.iss  <- este archivo
;
;  La ruta a "Dav" se calcula SOLA, en relación a dónde está este .iss
;  (usando la variable {#SourcePath} de Inno Setup), así que cualquiera
;  que clone el repo puede compilarlo sin editar ninguna ruta absoluta.
;
;  Si en algún momento cambian la carpeta "installer" de lugar dentro
;  del repo, ajustá el "..\Dav" de la línea de abajo según corresponda.
;
;  Para compilar: abrí este .iss en Inno Setup y Build → Compile (Ctrl+F9).
;  Inno Setup solo LEE los archivos de Dav\ al compilar, para empaquetarlos
;  dentro del instalador — no los mueve, no los borra, no los toca.
;
;  QUÉ HACE:
;  - Instala todo dentro de %APPDATA%\FreeCAD\Mod\DAV
;    (esa ruta es una de las que InitGui.py ya busca por defecto,
;     así que FreeCAD va a encontrar el workbench sin configuración extra)
;  - Crea accesos directos (Escritorio + Menú Inicio) a iniciar_dav.bat,
;    que abre FreeCAD con el workbench cargado + la ventana IntegracionGUI
;  - Si no detecta una instalación de FreeCAD, avisa y sigue con la instalación
;    (los archivos quedan listos para cuando se instale FreeCAD)
; ============================================================

#define MyAppName "DAV (UADER)"
#define MyAppVersion "1.0"
#define MyAppPublisher "UADER"

; Ruta relativa: sube un nivel desde la carpeta "installer\" (donde vive
; este .iss) y entra a "Dav\". Funciona igual para todos, sin editar nada,
; siempre que se respete esa ubicación relativa dentro del repo.
#define SourceDir SourcePath + "..\Dav"

[Setup]
AppId={{8F1B2C4E-6A3D-4E7B-9C2A-DAV0FREECAD1}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={userappdata}\FreeCAD\Mod\DAV
DisableProgramGroupPage=yes
DisableDirPage=yes
PrivilegesRequired=lowest
OutputBaseFilename=DAV_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\iniciar_dav.bat"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\iniciar_dav.bat"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el Escritorio"; GroupDescription: "Accesos directos:"

[Code]
function FreeCADEncontrado(): Boolean;
var
  Paths: TArrayOfString;
  I: Integer;
  Candidatos: array[0..3] of String;
begin
  Result := False;

  // 1) Buscar en el registro (clave típica del instalador de FreeCAD)
  if RegKeyExists(HKLM, 'SOFTWARE\FreeCAD') or RegKeyExists(HKCU, 'SOFTWARE\FreeCAD') then
  begin
    Result := True;
    Exit;
  end;

  // 2) Buscar carpetas comunes de instalación
  Candidatos[0] := ExpandConstant('{pf}\FreeCAD 0.21\bin\FreeCAD.exe');
  Candidatos[1] := ExpandConstant('{pf}\FreeCAD 1.0\bin\FreeCAD.exe');
  Candidatos[2] := ExpandConstant('{pf64}\FreeCAD 0.21\bin\FreeCAD.exe');
  Candidatos[3] := ExpandConstant('{pf64}\FreeCAD 1.0\bin\FreeCAD.exe');

  for I := 0 to 3 do
  begin
    if FileExists(Candidatos[I]) then
    begin
      Result := True;
      Exit;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    if not FreeCADEncontrado() then
    begin
      MsgBox('No se detectó una instalación de FreeCAD en este equipo.' + #13#10 + #13#10 +
             'Los archivos de DAV ya quedaron instalados en:' + #13#10 +
             ExpandConstant('{app}') + #13#10 + #13#10 +
             'Instalá FreeCAD (freecad.org) y el workbench va a estar disponible ' +
             'automáticamente la próxima vez que lo abras.',
             mbInformation, MB_OK);
    end;
  end;
end;
