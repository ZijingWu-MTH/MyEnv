REM Update nani index file
pushd . 
perl "%~dp0filter_nani_input_filelist.pl" %ROOT%\filelist.filtered %ROOT%\nani_filelist
cd /d %ROOT%
nani -index:%ROOT%\nani_filelist
popd .
