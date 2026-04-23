[Setup]
AppName=GitBack
AppVersion={#AppVersion}
AppPublisher=American Sound & Engineering Inc.
DefaultDirName={autopf}\GitBack
DefaultGroupName=GitBack
OutputBaseFilename=GitBack_Setup_{#AppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
DisableProgramGroupPage=yes
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
UninstallDisplayName=GitBack

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GitBack"; Filename: "{app}\gitback.exe"
Name: "{commondesktop}\GitBack"; Filename: "{app}\gitback.exe"; Tasks: desktopicon

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}'))

[Code]

function GitIsInstalled(): boolean;
var
  GitPath: string;
  CommonPaths: array of string;
  i: Integer;
begin
  Result := False;

  if RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\GitForWindows', 'InstallPath', GitPath) then begin
    Result := FileExists(GitPath + '\bin\git.exe');
    if Result then exit;
  end;
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\WOW6432Node\GitForWindows', 'InstallPath', GitPath) then begin
    Result := FileExists(GitPath + '\bin\git.exe');
    if Result then exit;
  end;
  if RegQueryStringValue(HKEY_CURRENT_USER,
    'SOFTWARE\GitForWindows', 'InstallPath', GitPath) then begin
    Result := FileExists(GitPath + '\bin\git.exe');
    if Result then exit;
  end;

  SetArrayLength(CommonPaths, 3);
  CommonPaths[0] := 'C:\Program Files\Git\bin\git.exe';
  CommonPaths[1] := 'C:\Program Files (x86)\Git\bin\git.exe';
  CommonPaths[2] := ExpandConstant('{localappdata}') + '\Programs\Git\bin\git.exe';
  for i := 0 to GetArrayLength(CommonPaths) - 1 do begin
    if FileExists(CommonPaths[i]) then begin
      Result := True;
      exit;
    end;
  end;
end;

function InitializeSetup(): boolean;
begin
  if not GitIsInstalled() then
  begin
    MsgBox(
      'Git for Windows is required to run GitBack but was not found on this system.' + #13#10 + #13#10 +
      'Please install Git for Windows from https://git-scm.com and then re-run this installer.',
      mbCriticalError,
      MB_OK
    );
    Result := False;
  end
  else
    Result := True;
end;

function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;
