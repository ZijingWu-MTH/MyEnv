pushd .
cd $ROOT
# TODO by zijwu, we should define an variable for file type.

python "$myEnvFolder"/find.py -r $ROOT >$ROOT/filelist

python "$myEnvFolder"/find.py -r /System/Library/Frameworks>> $ROOT/filelist
python "$myEnvFolder"/find.py -r /usr/include >> $ROOT/filelist

python $myEnvFolder/filelist_filter.py --org $ROOT/filelist --plugin $myEnvFolder/filelist_filter_plugin.py --output  $ROOT/filelist.filter_tmp
python $myEnvFolder/filelist_filter.py --org $ROOT/filelist.filter_tmp --plugin $CUE/filelist_filter_plugin.py --output $ROOT/filelist.filtered
rm -f -r $ROOT/filelist.filter_tmp
popd

