# xonsh behavior variables.
$UPDATE_OS_ENVIRON=True
$RAISE_SUBPROC_ERROR=True

import os
$myEnvFolder=os.getcwd()
$ROOT=$ARG0
$CUE=$ARG1
$SVN_EDITOR="vim"
$VimPerlTools="/usr/share/vim/PerlTools"
$RPK_DIR="~/dpk"

import os
TMP=os.path.normpath(os.path.expanduser("~/tmp"))

#
python3 $ROOT/build_system/mkdir.py f"{TMP}"

echo read global cue.
cd ~/tmp
python3 $ROOT/build_system/rm.py cue.global.script.xsh
python3 $myEnvFolder/cue2shell.py $myEnvFolder/cue.pri  ~/tmp/cue.global.script.xsh
source ~/tmp/cue.global.script.xsh
#
echo read project type cue
cd ~/tmp
python3 $ROOT/build_system/rm.py cue.local.script.xsh
python3 $myEnvFolder/cue2shell.py $CUE/cue.pri  ~/tmp/cue.local.script.xsh
source ~/tmp/cue.local.script.xsh
