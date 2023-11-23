. .\cue.ps1 d:\source_code\bj-media d:\source_code\bj-media\cue

$env:OBJPOSTFIX="-media-x64"

$env:DART_SDK_PATH = 'd:\opensource\flutter\bin\cache\dart-sdk'
# 'd:\opensource\flutter\bin\cache\artifacts\engine\windows-x64\'

$env:PATH = "C:\Users\admin\AppData\Local\Programs\Python\Python39\;C:\Users\admin\AppData\Local\Programs\Python\Python39\Scripts\;$env:PATH"

$env:PYTHON_DEV_INCLUDE_PATH = "C:\Users\admin\AppData\Local\Programs\Python\Python39\include"
$env:PYTHON_DEV_LIB = "C:\Users\admin\AppData\Local\Programs\Python\Python39\libs\python39.lib"


#$env:Python313 = "D:\opensource\cpython\PCbuild\amd64"
#$env:PYTHON_DEV_INCLUDE_PATH = "D:\opensource\cpython\Include"
#$env:PYTHON_DEV_LIB = "$env:Python313\python313.lib"


$env:PATH = "C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\;C:\Program Files\LLVM\bin;$env:PATH"


$env:FLUTTER_PATH = "d:\opensource\flutter"
$env:QT_PATH = "d:\opensource\qt5-build\qtbase"

$env:QT_LIB_POSTFIX = ".lib"
$env:QT_DLL_POSTFIX = ".dll"


$env:PATH = "$env:PATH;C:\Users\wuzij\AppData\Local\Pub\Cache\bin;$env:FLUTTER_PATH\bin\"
$env:PATH = "$env:PATH;d:\opensource\flutter\bin\cache\artifacts\engine\windows-x64\"

$env:PATH = "$env:PATH;C:\Users\Zj\Downloads\node-v18.15.0-win-x64\node-v18.15.0-win-x64"
$env:PATH="$env:PATH;C:\Program Files\GTK2-Runtime Win64\bin"
$env:PATH="$env:PATH;C:\Program Files\nodejs"
$env:PATH="$env:PATH;$HOME/.pub-cache/bin"


$env:PATH="$env:PATH;C:\Users\admin\AppData\Local\Pub\Cache\bin"

$env:NODE_SKIP_PLATFORM_CHECK = 1
set-location -path $env:myEnvFolder
set-alias -name vi -value vim

$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
[Console]::TreatControlCAsInput = $True

$env:PATH="$env:PATH;C:\Program Files\Git\bin"
$env:PATH="$env:PATH;C:\windows\System32\"

$env:PATH="$env:PATH;C:\Program Files\Android\Android Studio\jbr\bin"
$env:PATH="$env:PATH;C:\Program Files\PowerShell\7"

$env:PATH="$env:PATH;D:\gradle-7.4\bin"

$env:PATH="$env:PATH;C:\Users\admin\AppData\Local\Android\Sdk\platform-tools"
$env:PATH="$env:PATH;C:\apktool\"

$env:PATH="$env:PATH;C:\Program Files\LLVM\bin\"
$env:ASAN_OPTIONS="detect_stack_use_after_return=1"

$env:NDK_PATH="C:\Users\admin\Downloads\android-ndk-r26"
#$env:NDK_PATH="C:\Users\admin\Downloads\android-ndk-r17c"
$env:ANDROID_SDK_ROOT="C:\Users\admin\AppData\Local\Android\Sdk"
$env:JAVA_HOME_PATH="d:\java_home\"
