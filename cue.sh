echo $1
export myEnvFolder="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export ROOT=$1
export CUE=$2
export SVN_EDITOR=vim
export VimPerlTools=/usr/share/vim/PerlTools
export RPK_DIR=~/dpk
export TMP=~/tmp
#
mkdir ~/tmp
echo read global cue.
cd ~/tmp
rm cue.global.script.sh
python "$myEnvFolder"/cue2shell.py $myEnvFolder/cue.pri  ~/tmp/cue.global.script.sh
chmod +x ~/tmp/cue.global.script.sh
. ~/tmp/cue.global.script.sh
#
echo read project type cue
cd ~/tmp
rm cue.local.script.sh
python "$myEnvFolder"/cue2shell.py "$CUE"/cue.pri  ~/tmp/cue.local.script.sh
chmod +x ~/tmp/cue.local.script.sh
. ~/tmp/cue.local.script.sh
#
. "$CUE"/cue.sh
python "$myEnvFolder"/cue.py

