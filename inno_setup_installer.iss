; ---------------------------------------
; Inno Setup Script for PyInstaller .exe
; Fully standalone installer (includes VC++ redistributable)
; ---------------------------------------

[Setup]
AppName=Mcc Tests
AppVersion=1.0
AppPublisher=MyCompany
DefaultDirName={pf}\MccTests
DefaultGroupName=MccTests
OutputBaseFilename=MccTestsInstaller
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=no
UninstallDisplayIcon={app}\MccTests.exe
AllowNoIcons=yes
OutputDir=.

[Files]
; Main PyInstaller executable
Source: "dist\mcc_tests\MccTests.exe"; DestDir: "{app}"; Flags: ignoreversion

; Optional data files
Source: "dist\mcc_tests\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

; Embedded VC++ Redistributable installer (offline)
Source: "vc_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
; Start Menu shortcut
Name: "{group}\MccTests"; Filename: "{app}\MccTests.exe"
; Desktop shortcut (optional)
Name: "{userdesktop}\MccTests"; Filename: "{app}\MccTests.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
; Run the app after installation
Filename: "{app}\MccTests.exe"; Description: "Launch MccTests"; Flags: nowait postinstall skipifsilent

[Code]
; Check and install VC++ Redistributable if missing
function IsVCRedistInstalled(): Boolean;
var
  Success: Boolean;
begin
  Success := RegValueExists(HKLM, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Installed');
  if not Success then
    Success := RegValueExists(HKLM, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x86', 'Installed');
  Result := Success;
end;

procedure InitializeWizard();
var
  ResultCode: Integer;
begin
  if not IsVCRedistInstalled() then
  begin
    MsgBox('Visual C++ 2015-2019 Redistributable is required. It will now be installed.', mbInformation, MB_OK);
    Exec(ExpandConstant('{tmp}\vc_redist.x64.exe'), '/install /quiet /norestart', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
  end;
end;
