echo ROOT
echo %1
echo CUE
echo %2
set myEnvFolder=%~dp0
set ROOT=%1
set CUE=%2

set SVN_EDITOR=vim
set VimPerlTools=\usr\cmdare\vim\PerlTools
set RPK_DIR=%USERPROFILE%\dpk
set TMP=%USERPROFILE%\tmp
@REM
mkdir %USERPROFILE%\tmp
echo read global cue.
cd %USERPROFILE%\tmp
del /S /Q cue.global.script.cmd
python %myEnvFolder%\cue2shell.py %myEnvFolder%\cue.pri %USERPROFILE%\tmp\cue.global.script.cmd
call %USERPROFILE%\tmp\cue.global.script.cmd
@REM
echo read project type cue
cd %USERPROFILE%\tmp
del /S /Q cue.local.script.cmd
python %myEnvFolder%\cue2shell.py %CUE%\cue.pri %USERPROFILE%\tmp\cue.local.script.cmd
call %USERPROFILE%\tmp\cue.local.script.cmd

@REM
call %CUE%\cue.cmd
python %myEnvFolder%\cue.py

