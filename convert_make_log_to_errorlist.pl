
##path parser
#use File::Basename;
#use File::;
#my ($name,$parent,$suffix) = fileparse($path, "\.[^.]*");
#if (not -e $path) {}
#if (-d $path) {}
#if (defined($file)) {}
#opendir DIR, $path or die "Can not open $path\n";
#my @list = readdir DIR;

##regular expression
#if ($line =~ m/(\s*)<File Source="(.*\\)([^\\]*.resx)" \/>/)
#    $neturalLanguageName =~ s/!\(wix\.\$\(var.Culture\)_RESOURCE_EXT\)//;
#    $enLine =~ s/<File /<File Name="$enLanguageName" /s;
#    $line =~ s/<File /<File Name="$fileNameForLang" /s;

##function
#sub generate() {
#    my $path = shift @_;
#}

##create guid 
#use Win32::Guidgen;
#my $guid = Win32::Guidgen::create();

##access enviroment variables
#my $setting = $ENV{"_NTTREE"}
#my $file = $ARGV[0];

##open file for output and input.
#use File::Find;
#find(\&callback, @dirs)
#find({wanted=>\&callback, no_chdir => 1 , bydepth => 1, preprocess=>\&callback1, postprocess=>\&callback2}, @dirs)
#sub callback{...}
#$FH = STDIN;
#open $OUT_FH, ">", $org_setting or die $!;
#open $BAK_FH, $bak_setting or die $!;
#while (my $line = <$BAK_FH>)
#{
#    chomp $line;
#    print $OUT_FH $line ."\n" or die $!;
#}
#close $BAK_FH;
#close $OUT_FH;

##data struct and algorithm
#my @language = ("zh-CN","zh-TW");
#push (@existFiles, $fileName);
#my %hash = (foo=>42, bar=>23);
#my @keys = keys %hash;
#my @values = values %hash;
#while(($key, $value) = each %hash) {delete $hash{$key};}
#foreach my $lan (@language){}
#sort {$b <=> $a} @files;
#sort callback @files;

##The time function
#my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime;
#sleep 5; #5 seconds sleep EXPR
#srand(); rand();

##string function
#rindex/index("abcd", "cd");
#reverse "world"; #reverse LIST/STR
#length("abcd");
#split(//, #hi there#); #split /PATTERN/,EXPR,LIMIT   
#substr $s, 4, 5; #substr EXPR,OFFSET,LENGTH
#print join("\n", @files); join("\n", file1, file2, file3);
#uc/lc($name)
#if ($str1 eq $str2) {}
#
#NOTE:: 1. my will limit veriable to local. 2. Use {} instead of [] to access hash

use File::Basename;
#my $cmdRes = `cd %ROOT% & dir /s /B *.vcproj`;
#my @projs = split /\n/, $cmdRes;


#my %proj2PossibleDirs = ();
#my %id2Proj = ();
#initialize
#foreach $proj (@projs)
#{
#    chomp($proj);
#    my ($name,$parent,$suffix) = fileparse($proj, "\.[^.]*");
#    $name = lc($name);
#    $proj2PossibleDirs{$name}=[];
#}

#foreach $proj (@projs)
#{
#    chomp($proj);
#    my ($name,$parent,$suffix) = fileparse($proj, "\.[^.]*");
#    $name = lc($name);
#    #print "find $parent for -$name -$suffix in $proj\n";

#    my $array = $proj2PossibleDirs{$name};
#    push(@$array, ($parent));
#    $proj2PossibleDirs{$name}=$array;
#}

sub getFilesFromFileList($)
{
    my $filePattern = shift;
    my @result = ();
    open FILE_LIST_FH, "<", $ENV{"ROOT"} . "/filelist" or die "Open the filelist failed, please make sure it exist. Error:" . $1;
    while (my $line = <FILE_LIST_FH>)
    {
        chomp $line;
        unless ($line =~ m/$filePattern/i)
        {
            next
        }
        push(@result, $line);

    }
    close FILE_LIST_FH;
    @result;
}

$FH = STDIN;
$OUT_FH = STDOUT;
#open OUT_FH, ">", $org_setting or die $!;
while (my $line = <$FH>)
{
   chomp $line;

   my $file = "";
   my $lineNum = 0;
   my $colNum = 0;
   my $msg = "unknown pls check log file";
#../src/media_processor/private/mac/content/content_device.mm:15:20: error: logger.h: No such file or directory
#../src/media_processor/private/mac/content/content_device.mm: In constructor 
   if ($line =~ m/^\s*([^():]+):(\d+).*: error:(.*)$/)
   {
       $file = $1;
       $lineNum = $2;
       $msg = $3;
   }
   else
   {
       next;
   }

   if (not -e $file)
   {
       my ($name,$parent,$suffix) = fileparse($file, "");
       my @possibleFiles = getFilesFromFileList($name);
       foreach $possibleFile (@possibleFiles)
       {
            if (-e $possibleFile)
            {
                $file = $possibleFile;
            }
       }
   }

   #print $file . ":" . $lineNum . ":" . $msg. " " . $projName . "--\n";
   my $newLine = $file . ":" . $lineNum . ":" . $colNum . ":" . $msg;
   print $OUT_FH $newLine ."\n" or die $!;
}
close $OUT_FH;

