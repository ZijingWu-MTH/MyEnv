$env:PATH = "e:\opensource\vim\src;$env:PATH"
$env:PATH = "C:\Users\Administrator1\AppData\Local\Programs\Python\Python39\Scripts;$env:PATH"
$env:PATH = "C:\Users\Administrator1\AppData\Local\Programs\Python\Python39;$env:PATH"
. .\cue.ps1 e:\source_code\bj-media3 e:\source_code\bj-media\cue

$env:OBJPOSTFIX="-media3-x64"

$env:DART_SDK_PATH = 'e:\opensource\flutter\bin\cache\dart-sdk'
# 'e:\opensource\flutter\bin\cache\artifacts\engine\windows-x64\'

$env:PATH = "C:\Users\Administrator\AppData\Local\Programs\Python\Python39\;C:\Users\Administrator\AppData\Local\Programs\Python\Python39\Scripts\;$env:PATH"

$env:PYTHON_DEV_INCLUDE_PATH = "C:\Users\Administrator\AppData\Local\Programs\Python\Python39\include"
$env:PYTHON_DEV_LIB = "C:\Users\Administrator\AppData\Local\Programs\Python\Python39\libs\python39.lib"


#$env:Python313 = "e:\opensource\cpython\PCbuild\amd64"
#$env:PYTHON_DEV_INCLUDE_PATH = "e:\opensource\cpython\Include"
#$env:PYTHON_DEV_LIB = "$env:Python313\python313.lib"


$env:PATH = "C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\;C:\Program Files\LLVM\bin;$env:PATH"
$env:PATH = "C:\Program Files (x86)\NASM;$env:PATH"


$env:FLUTTER_PATH = "e:\opensource\flutter"
$env:QT_PATH = "e:\opensource\qt5-build-release\"

$env:PATH = "$env:PATH;C:\Users\wuzij\AppData\Local\Pub\Cache\bin;$env:FLUTTER_PATH\bin\"
$env:PATH = "$env:PATH;e:\opensource\flutter\bin\cache\artifacts\engine\windows-x64\"

$env:PATH = "$env:PATH;C:\Users\Zj\Downloads\node-v18.15.0-win-x64\node-v18.15.0-win-x64"
$env:PATH="$env:PATH;C:\Program Files\GTK2-Runtime Win64\bin"
$env:PATH="$env:PATH;C:\Program Files\nodejs"
$env:PATH="$env:PATH;~/.pub-cache/bin"

$env:PATH="$env:PATH;C:\Users\Administrator\AppData\Local\Pub\Cache\bin"

$env:NODE_SKIP_PLATFORM_CHECK = 1
set-location -path $env:myEnvFolder
set-alias -name vi -value vim

$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
[Console]::TreatControlCAsInput = $True

$env:PATH="$env:PATH;C:\Program Files\Git\bin"
$env:PATH="$env:PATH;C:\windows\System32\"
$env:PATH="$env:PATH;C:\gnutool\GetGnuWin32\bin"
$env:PATH="$env:PATH;C:\gnutool\bin"

$env:PATH="$env:PATH;C:\Program Files\Android\Android Studio\jbr\bin"
$env:PATH="$env:PATH;C:\Program Files\PowerShell\7"

$env:PATH="$env:PATH;e:\gradle-7.4\bin"

$env:PATH="$env:PATH;C:\Users\Administrator\AppData\Local\Android\Sdk\platform-tools"
$env:PATH="$env:PATH;e:\installation\apk\"


$env:PATH="$env:PATH;C:\Program Files\LLVM\bin\"
$env:ASAN_OPTIONS="detect_stack_use_after_return=1"

$env:NDK_PATH="e:\downloads\android-ndk-r26d-windows\android-ndk-r26d"
$env:ANDROID_SDK_ROOT="E:\android_studio\"
$env:JAVA_HOME="e:\jdk-17\"
$env:PATH="$env:JAVA_HOME\bin;$env:PATH"
$env:PATH="C:\Users\Administrator\Downloads\nssm-2.24\nssm-2.24\win64;$env:PATH"
$env:PATH="E:\installation\perl\bin;$env:PATH"
$env:JAVA_HOME_PATH=$env:JAVA_HOME
$env:PATH="E:\installation\nginx-1.26.1;$env:PATH"
