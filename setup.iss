[Setup]
AppName=Media Yantra
AppVersion=1.0.0
AppPublisher=Kartik Kothalkar (Open Source Warrior)
AppCopyright=Kartik Kothalkar
InfoBeforeFile=README.md
DefaultDirName={autopf}\Media Yantra
DefaultGroupName=Media Yantra
UninstallDisplayIcon={app}\Media Yantra.exe
Compression=lzma2/ultra64
SolidCompression=yes
OutputDir=Release
OutputBaseFilename=Media_Yantra_Setup_v1.0
SetupIconFile=assets\icon.ico
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
DisableWelcomePage=no

[Files]
Source: "dist\Media Yantra\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Media Yantra"; Filename: "{app}\Media Yantra.exe"; IconFilename: "{app}\assets\icon.ico"
Name: "{autodesktop}\Media Yantra"; Filename: "{app}\Media Yantra.exe"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\Media Yantra.exe"; Description: "Launch Media Yantra"; Flags: nowait postinstall skipifsilent
