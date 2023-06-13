cue = cd env{CUE} :: win32
cue = cd env{CUE} :: mac
cue = cd env{CUE} :: linux
myEnv = cd env{myEnvFolder}
tmp = cd ~{path_sep}tmp
nani = "env{myEnvFolder}{path_sep}nani $1 $2" > _search_tmp_.txt :: win32
ni = python3 "env{myEnvFolder}{path_sep}search_service.py" $1 $2 
qs = python3 "env{myEnvFolder}{path_sep}query_service.py" $1
updateindex = python3 "env{myEnvFolder}{path_sep}index_service.py"
updatefilelist = env{myEnvFolder}{path_sep}update_file_list.sh :: mac
updatefilelist = env{myEnvFolder}{path_sep}update_file_list.sh :: linux
updatefilelist = . env{myEnvFolder}{path_sep}update_file_list.cmd :: win32
updatetag = env{myEnvFolder}{path_sep}update_ctag_index.sh :: mac
updatetag = env{myEnvFolder}{path_sep}update_ctag_index.sh :: linux
updatetag = . env{myEnvFolder}{path_sep}update_ctag_index.cmd :: win32
updatecscope = env{myEnvFolder}{path_sep}update_cscope_index.sh :: mac
updatecscope = env{myEnvFolder}{path_sep}update_cscope_index.sh :: linux
updatecscope = . env{myEnvFolder}{path_sep}update_cscope_index.cmd :: win32
updateall = alias{updatefilelist} && alias{updateindex} && alias{updatetag} && alias{updatecscope}

root = cd env{ROOT} :: win32
root = cd env{ROOT} :: mac
root = cd env{ROOT} :: linux
govim = vimBinFolder=`which vim` {command_sep} cd $(dirname "$vimBinFolder")/../share/vim :: mac
govim = vimBinFolder=`which vim` {command_sep} cd $(dirname "$vimBinFolder")/../share/vim :: linux
q = exit
build = pushd . {command_sep} cd /d env{ROOT}{path_sep}scripts {command_sep} build_rpd.bat {command_sep} popd :: win32

svnfix = svn update --set-depth empty && svn update --set-depth infinity

svndiffcl = svn diff --diff-cmd "env{myEnvFolder}{path_sep}svnwindiff.{shell_ext}" --cl $1
svndifff = svn diff --diff-cmd "env{myEnvFolder}{path_sep}svnwindiff.{shell_ext}" $1

patch = pushd . {command_sep} cd /d env{ROOT} {command_sep} popd {command_sep} svn diff --cl $1 > d:{path_sep}dpk{path_sep}$1.patch

go = . env{CUE}{path_sep}cue{path_sep}goto_single_dir.cmd

copydir = cd | CLIP :: win32
copydir = pwd | pbcopy :: mac

copy = cp :: mac

vclog = perl env{myEnvFolder}{path_sep}convert_vcproj_log_to_errorlist.pl build.log > build.filter.log {command_sep} vim build.filter.log -c "cb"  :: win32
cslog = perl env{myEnvFolder}{path_sep}convert_cs_make_log_to_errorlist.pl build.log > build.filter.log {command_sep} vim build.filter.log -c "cb"  :: win32
mklog = python3 env{myEnvFolder}{path_sep}convert_nmake_cpp_error.py build.log  build.filter.log {command_sep} vim build.filter.log -c "cb"  :: win32
mklog = cat build.log | perl env{myEnvFolder}{path_sep}convert_make_log_to_errorlist.pl > build.filter.log {command_sep} vim build.filter.log -c "cb"  :: mac
mklog = cat build.log | perl env{myEnvFolder}{path_sep}convert_make_log_to_errorlist.pl > build.filter.log {command_sep} vim build.filter.log -c "cb"  :: linux

cscopeIndex = dir /A:-D /B  /S *.c *.cc *.cpp *.h *.hpp *.vcproj *.sln *.cs >cscope.files {command_sep} cscope -bkq -i cscope.files :: win32
reloadcue = pushd . {command_sep} cd env{myEnvFolder} {command_sep} . .{path_sep}cue.{shell_ext} env{ROOT} env{CUE} {command_sep} popd
ewindbg = "C:{path_sep}WinDDK{path_sep}7600.16385.1{path_sep}Debuggers{path_sep}windbg.exe" :: win32
test = obj{path_sep}app.exe obj{path_sep}test.cpp obj{path_sep}test.out :: win32

.. = cd ..
... = cd ..{path_sep}..
.... = cd ..{path_sep}..{path_sep}..
..... = cd ..{path_sep}..{path_sep}..{path_sep}..
...... = cd ..{path_sep}..{path_sep}..{path_sep}..{path_sep}..
mk = nmake /f $1 /x build.err :: win32
mk = rm build.log {command_sep} make -f $1 $2 $3 2>&1| tee -a build.log :: mac
mk = rm build.log {command_sep} make -f $1 $2 $3 2>&1| tee -a build.log :: linux
mkclean = make clean -f $1 :: mac
mkclean = make clean -f $1 :: linux

ls = dir $1 :: win32
dir = ls $1 :: mac
cr = python3 "env{myEnvFolder}{path_sep}querychange.py" $1
~ = cd ~ :: mac
~ = cd ~ :: linux
~ = cd $env:USERPROFILE :: win32
profile = cd ~ {command_sep} vim .profile :: mac
rename = mv :: mac
cls = clear :: mac
gp = python "env{myEnvFolder}/find.py" -r . -e "grep -H \"$1\" {path}":: mac
gp = python "env{myEnvFolder}/find.py" -r . -e "grep -H \"$1\" {path}":: linux
gp = python "env{myEnvFolder}/find.py" -r . -e "findstr /snip /C:""$1"" {path}" :: win32
#fullgp = find . -type f -exec grep -i -H "$1" {} \; :: mac
#fullgp = find . -type f -exec grep -i -H "$1" {} \; :: linux
#partialgp = echo "find $1 in file type extension $2" && find . \( -name "*.$2" \) -exec grep -i -H "$1" \; :: mac
restartnetwork = sudo ifconfig en0 down {command_sep} sudo ifconfig en0 up {command_sep} sudo ifconfig en1 down {command_sep} sudo ifconfig en1 up
undo = python3 env{myEnvFolder}/svn_revert.py $1 $2 
functions = declare -f :: mac
functions = declare -f :: linux
r = su -l root :: mac
r = su -l root :: linux
diffr = svn diff --diff-cmd diff -x "-U 1000" > $1

backup = mkdir ~/backup/ {command_sep} currentTime=`date +%m-%B-%d_%k_%M_%S` {command_sep} cp -R $1 ~/backup/$(basename "$1")-$currentTime :: mac
#for linux, we remove the "%k" else it will be space.
backup = mkdir ~/backup/ {command_sep} currentTime=`date +%m-%B-%d_%M_%S` {command_sep} cp -R $1 ~/backup/$(basename "$1")-$currentTime :: linux
backupdir = cd ~/backup/  :: mac
backupdir = cd ~/backup/  :: linux
sync = pushd . && cd $ROOT && svn update && popd .
D = cd ~/Downloads :: mac
Doc = cd ~/Documents :: mac
D = cd ~/Downloads :: linux
Doc = cd ~/Documents :: linux
dv = python3 "env{myEnvFolder}{path_sep}download_video.py" download $1
dvc = python3 "env{myEnvFolder}{path_sep}download_video.py" check
ucd = python3 env{myEnvFolder}/generate_goto_dir_script.py $1 up  env{TMP}/goto.{shell_ext} && . env{TMP}/goto.{shell_ext}
dcd = python3 env{myEnvFolder}/generate_goto_dir_script.py $1 down  env{TMP}/goto.{shell_ext} && . env{TMP}/goto.{shell_ext}
devicedebug = $myEnvFolder/launch_device_debug.sh $1 :: mac
gccd = g++ -g $1
decompress = tar -cvzf $1 $1_decompress:: mac
compress = tar -cvzf $1.tar.gz $1:: mac
decompress = tar -cvzf $1 $1_decompress:: linux
compress = tar -cvzf $1.tar.gz $1:: linux
whooshIndex = python3 $myEnvFolder/index_service.py
unlockkeychain = security unlock-keychain ~/Library/Keychains/login.keychain :: mac
demo = cd ~/demo/ :: mac
hidepath = export HIDESTATUSBAR=1
showpath = export HIDESTATUSBAR=
findchange = python $myEnvFolder/svn_changes.py $1 "$2"

# ':' is a python operator in xonsh
#. = {source}
#> = cp $ROOT/last_edit_file.txt $ROOT/last_edit_file.{shell_ext} && {source} $ROOT/last_edit_file.{shell_ext}
: = cp $ROOT/last_edit_file.txt $ROOT/last_edit_file.{shell_ext} && {source} $ROOT/last_edit_file.{shell_ext} :: mac
: = cp $ROOT/last_edit_file.txt $ROOT/last_edit_file.{shell_ext} && {source} $ROOT/last_edit_file.{shell_ext} :: linux
: = Copy-Item $env:ROOT/last_edit_file.txt $env:ROOT/last_edit_file.ps1 && . $env:ROOT/last_edit_file.ps1::win32

checkin = python $myEnvFolder/partial_check_in.py
symbolicate = export DEVELOPER_DIR="/Applications/XCode.app/Contents/Developer" {command_sep} /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/PrivateFrameworks/DTDeviceKit.framework/Versions/A/Resources/symbolicatecrash -v -E  $1 $2
openurl = open::mac
openurl = xdg-open::linux
openurl = start .::win32
sf = python3 $myEnvFolder/stackoverflow_filter.py "SO" $1 $2 $3 > ~/tmp/stackoverflow_questions.html {command_sep} alias{openurl} ~/tmp/stackoverflow_questions.html
lsf = python3 $myEnvFolder/stackoverflow_filter.py "SO" 6 20 2000 > ~/tmp/stackoverflow_questions.html {command_sep} alias{openurl} ~/tmp/stackoverflow_questions.html
uxsf = python3 $myEnvFolder/stackoverflow_filter.py "UX" $1 $2 $3 > ~/tmp/stackoverflow_questions.html {command_sep} alias{openurl} ~/tmp/stackoverflow_questions.html
luxsf = python3 $myEnvFolder/stackoverflow_filter.py "UX" 6 20 2000 > ~/tmp/stackoverflow_questions.html {command_sep} alias{openurl} ~/tmp/stackoverflow_questions.html

fixgcclib = export DYLD_LIBRARY_PATH=$ROOT/x86_64-apple-darwin12.4.0/libsanitizer/ubsan/.libs:$ROOT/x86_64-apple-darwin12.4.0/libgcc:$ROOT/x86_64-apple-darwin12.4.0/libstdc++-v3:$ROOT/x86_64-apple-darwin12.4.0/libstdc++-v3/src/.libs:$DYLD_LIBRARY_PATH
myxgcc = pushd . {command_sep} cd $ROOT/host-x86_64-apple-darwin12.4.0/gcc {command_sep} xgcc -fsanitize=undefined $1  -o $1.a.out -L$ROOT/x86_64-apple-darwin12.4.0/libsanitizer/ubsan/.libs  -L$ROOT/x86_64-apple-darwin12.4.0/libgcc -L$ROOT/x86_64-apple-darwin12.4.0/libstdc++-v3/src/.libs {command_sep} popd 
symbolicate = export DEVELOPER_DIR="/Applications/XCode.app/Contents/Developer" {command_sep} /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/PrivateFrameworks/DTDeviceKit.framework/Versions/A/Resources/symbolicatecrash     $1 $2 :: mac
relay = ssh wuzijing@relay.xiaomi.com
gitdiff = git --no-pager diff --relative -w $1

#mygrep = python "env{myEnvFolder}/find.py" -r . -s "*.git*;*boost*;*thirdparty*;*lightning*;*gt-*;*node_module*;*lightning*;*thirdparty*;*server*;*service*;*gt-*;*admin*;*ppapi*;*live*;*.git*;*backup*;*ffmpeg*;*cef-*" -e "grep -H \"$1\" \"{path}\"":: mac
#mygrepf = python "env{myEnvFolder}/find.py" -r . -s "*.git*;*boost*;*thirdparty*;*lightning*;*gt-*;*node_module*;*lightning*;*thirdparty*;*server*;*service*;*gt-*;*admin*;*ppapi*;*live*;*.git*;*backup*;*ffmpeg*;*cef-*" -e "grep -H -f pattern \"{path}\"":: mac
