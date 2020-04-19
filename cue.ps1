function Get-ScriptDirectory {
    Split-Path -parent $PSCommandPath
}

Split-Path -Parent $MyInvocation.MyCommand.Path 

$env:myEnvFolder=Get-ScriptDirectory
$env:ROOT=$args[0]
$env:CUE=$args[1]
echo "cue: $env:CUE"
echo "root: $env:ROOT"

$env:TMP="$env:USERPROFILE\tmp"
$env:vs9path=$env:VS90COMNTOOLS + "vsvars32.bat"
$env:vs10path=$env:VS100COMNTOOLS + "vsvars32.bat"

# VS 2012
$env:vs11path=$env:VS110COMNTOOLS + "vsvars32.bat"
# VS 2013
$env:vs12path=$env:VS120COMNTOOLS + "vsvars32.bat"

$env:SVN_EDITOR="vim"
# set the java has 1.6.0, because XMLAPI generator code dependence on java version (the sequence of attribute of class changed).
$env:JAVA_HOME="C:\Program Files (x86)\Java\jdk1.6.0_41"
$env:PATH="C:\Program Files (x86)\Java\jdk1.6.0_41\bin;$env:PATH"
$env:VimPerlTools="c:\Program Files (x86)\Vim\PerlTools"
$env:RPK_DIR="d:\dpk\"

Set-Location -Path $env:ROOT
#$env:_NT_SYMBOL_PATH="ssymsrv*symsrv.dll*d:\symbols*http://msdl.microsoft.com/download/symbol;$env:ROOT\release"

If (Test-Path $env:vs12path) {
    $env:vs12path
} Else {
    If (Test-Path $env:vs11path) {
        $vs11path
    } Else {
        If (Test-Path $env:vs10path) {
            $vs10path
        } Else {
            $vs9path
        }
    }
}

echo "read global cue"
New-Item -Path $env:USERPROFILE\tmp -ErrorAction SilentlyContinue
Remove-Item -Path $env:USERPROFILE\tmp\cue.global.script.ps1 -ErrorAction SilentlyContinue
python "$env:myEnvFolder\cue2shell.py" "$env:myEnvFolder\cue.pri" "$env:USERPROFILE\tmp\cue.global.script.ps1"
. "$env:USERPROFILE\tmp\cue.global.script.ps1"

echo "read project type cue"
Remove-Item -Path "$env:USERPROFILE\tmp\cue.local.script.ps1" -ErrorAction SilentlyContinue
python "$env:myEnvFolder\cue2shell.py" "$env:CUE\cue.pri" "$env:USERPROFILE\tmp\cue.local.script.ps1"
. $env:USERPROFILE\tmp\cue.local.script.ps1

If (Test-Path "$env:CUE\cue.ps1") {
    . $env:CUE\cue.ps1
}

$env:PATH="$env:PATH;c:\Python27\;D:\my_project\patch_tool"
$env:PATH="$env:PATH;C:\Program Files\Microsoft Visual Studio 9.0\Team Tools\Performance Tools"
#$env:PATH="$env:PATH;$env:VimPerlTools\..\UnxTools;C:\Program Files\TortoiseSVN\bin"
$env:PATH="$env:PATH;C:\Program Files (x86)\Microsoft SDKs\Windows\v7.0A\Bin"

python $env:myEnvFolder\cue.py
