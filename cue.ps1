$Env:myEnvFolder=$PSScriptRoot
$Env:ROOT=$args[0]
$Env:CUE=$args[1]

set SVN_EDITOR=vim
set VimPerlTools=\usr\cmdare\vim\PerlTools
set RPK_DIR=$env:USERPROFILE\dpk
set TMP=$env:USERPROFILE\tmp

new-item -itemtype directory -path $env:USERPROFILE\tmp -force
echo "read global cue."
cd $env:USERPROFILE\tmp
remove-item -path cue.global.script.ps1 -erroraction silentlycontinue
python3 $env:myEnvFolder\cue2shell.py $env:myEnvFolder\cue.pri $env:USERPROFILE\tmp\cue.global.script.ps1
. $env:USERPROFILE\tmp\cue.global.script.ps1

echo "read project type cue"
cd $env:USERPROFILE\tmp
remove-item -path cue.local.script.ps1 -erroraction silentlycontinue
python3 $env:myEnvFolder\cue2shell.py $env:CUE\cue.pri $env:USERPROFILE\tmp\cue.local.script.ps1
. $env:USERPROFILE\tmp\cue.local.script.ps1

# source $env:CUE\cue.cmd
python3 $env:myEnvFolder\cue.py

