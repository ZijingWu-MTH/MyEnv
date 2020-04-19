# one language object-c more than windows.
s="\t "
S="[$s]*"
w="_a-zA-Z0-9"
CN="[A-Z][$w]*"
NM="[$w][$w]*"


/usr/local/bin/ctags -L $ROOT/filelist.filtered -f $ROOT/mytags --recurse=yes --langdef=objc --langmap=objc:.m --regex-objc="/^@(interface|protocol|implementation)$S($CN($S\($CN\))*)/\2/f/" --regex-objc="/^$S(\-|\+)$S\($S$NM($S$NM)*$S\**$S\)*$S($NM)$S[:;]/\3/f/"
cscope -bkq -i $ROOT\filelist.filtered
