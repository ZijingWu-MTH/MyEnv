. .\cue.ps1 e:\source_code\bj-media e:\source_code\bj-media\cue

set OBJPOSTFIX=-bj-media

$env:DART_SDK_PATH = 'E:\open_source\flutter\bin\cache\dart-sdk'
# 'e:\open_source\flutter\bin\cache\artifacts\engine\windows-x64\'

$env:PATH = "C:\Users\Zj\AppData\Local\Programs\Python\Python38\;C:\Users\Zj\AppData\Local\Programs\Python\Python38\Scripts\;$env:PATH"
$env:PYTHON_DEV_INCLUDE_PATH = "C:\Users\Zj\AppData\Local\Programs\Python\Python38\include"
$env:PYTHON_DEV_LIB = "C:\Users\Zj\AppData\Local\Programs\Python\Python38\libs\python38.lib"
$env:PATH = "C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\;C:\Program Files\LLVM\bin;$env:PATH"


$env:FLUTTER_PATH = "E:\open_source\flutter"
$env:QT_PATH = "E:\open_source\qt5\qtbase\"
$env:QT_LIB_POSTFIX = ".lib"
$env:PATH = "$env:PATH;C:\Users\wuzij\AppData\Local\Pub\Cache\bin;$env:FLUTTER_PATH\bin\"
$env:PATH = "$env:PATH;E:\open_source\flutter\bin\cache\artifacts\engine\windows-x64\"

$env:PATH = "$env:PATH;C:\Users\Zj\Downloads\node-v18.15.0-win-x64\node-v18.15.0-win-x64"
$env:PATH="$env:PATH;C:\Program Files\GTK2-Runtime Win64\bin"
$env:PATH="$env:PATH;C:\Program Files\nodejs"
$env:PATH="$env:PATH;$HOME/.pub-cache/bin"

$env:NODE_SKIP_PLATFORM_CHECK = 1
A
set-location -path $env:myEnvFolder
set-alias -name vi -value vim

$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
[Console]::TreatControlCAsInput = $True

$env:PATH="$env:PATH;C:\Program Files\Git\bin"
$env:PATH="$env:PATH;C:\windows\System32\"

