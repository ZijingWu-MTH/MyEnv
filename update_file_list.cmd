pushd .
cd /d %ROOT%
dir /s /B /A:-D *.cpp *.cxx *.c *.cc *.h *.hpp *.cs *.xaml *.css *.js *.css *.java *.m4 *.aspx *.vcxproj *.vcproj *.csproj *.sln sources dirs *.xml *.sh *.bat *.txt *.tcl makefile* *.reg *.py *.res *.resources *.resx *.sql *.proj *.hxx *.html *.htm | find /V "~">%ROOT%\filelist
cd /d "%programfiles%\Microsoft SDKs"
dir /s /B /A:-D *.h *.cpp | find /V "~" >> %ROOT%\filelist

python %myEnvFolder%/filelist_filter.py --org %ROOT%\filelist --plugin %myEnvFolder%\filelist_filter_plugin.py --output  %ROOT%\filelist.filter_tmp
python %myEnvFolder%\filelist_filter.py --org %ROOT%\filelist.filter_tmp --plugin %CUE%\filelist_filter_plugin.py --output  %ROOT%\filelist.filtered

del %ROOT%\filelist.filter_tmp
popd
