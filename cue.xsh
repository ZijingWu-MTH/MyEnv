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
$TMP="~/tmp"

#
mkdir -p ~/tmp
echo read global cue.
cd ~/tmp
rm -f cue.global.script.xsh
python3 $myEnvFolder/cue2shell.py $myEnvFolder/cue.pri  ~/tmp/cue.global.script.xsh
chmod +x ~/tmp/cue.global.script.xsh
source ~/tmp/cue.global.script.xsh
#
echo read project type cue
cd ~/tmp
rm -f cue.local.script.xsh
python3 $myEnvFolder/cue2shell.py $CUE/cue.pri  ~/tmp/cue.local.script.xsh
chmod +x ~/tmp/cue.local.script.xsh
source ~/tmp/cue.local.script.xsh
