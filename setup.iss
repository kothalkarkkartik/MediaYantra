[Setup]
AppName=Media Yantra
AppVersion=1.0.0
AppPublisher=Kartik Kothalkar (Open Source Warrior)
AppCopyright=Kartik Kothalkar
InfoBeforeFile=notes.txt
DefaultDirName={autopf}\Media Yantra
DefaultGroupName=Media Yantra
UninstallDisplayIcon={app}\Media_Yantra_Final.exe
Compression=lzma2/ultra
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=Media_Yantra_Setup_v1.0
SetupIconFile=assets\icon.ico
DisableProgramGroupPage=yes
PrivilegesRequired=lowest

[Files]
Source: "dist\Media_Yantra_Final.exe"; DestDir: "{app}"; Flags: ignoreversion
; We also deploy any external FFmpeg instances if needed, though they're usually handled
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Media Yantra"; Filename: "{app}\Media_Yantra_Final.exe"; IconFilename: "{app}\assets\icon.ico"
Name: "{autodesktop}\Media Yantra"; Filename: "{app}\Media_Yantra_Final.exe"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\Media_Yantra_Final.exe"; Description: "Launch Media Yantra"; Flags: nowait postinstall skipifsilent
