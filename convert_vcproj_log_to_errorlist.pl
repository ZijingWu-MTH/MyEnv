##path parser
#use File::Basename;
#use File::;
#my ($name,$parent,$suffix) = fileparse($path);
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
#open OUT_FH, ">", $org_setting or die $!;
#open BAK_FH, $bak_setting or die $!;
#while (my $line = <BAK_FH>)
#{
#    chomp $line;
#    print OUT_FH $line ."\n" or die $!;
#}
#close BAK_FH;
#close OUT_FH;

##data struct and algorithm
#my @language = ("zh-CN","zh-TW");
#push (@existFiles, $fileName);
#my %hash = (foo=>42, bar=>23);

use File::Basename;

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

my @projs = getFilesFromFileList("\\.vcxproj\$");
#print @projs;
#my $cmdRes = `cd %ROOT% & dir /s /B *.vcxproj`;
#my @projs = split /\n/, $cmdRes;


my %proj2PossibleDirs = ();
my %id2Proj = ();
#initialize
foreach $proj (@projs)
{
    chomp($proj);
    my ($name,$parent,$suffix) = fileparse($proj, "\.[^.]*");
    $name = lc($name);
    $proj2PossibleDirs{$name}=[];
}

foreach $proj (@projs)
{
    chomp($proj);
    my ($name,$parent,$suffix) = fileparse($proj, "\.[^.]*");
    $name = lc($name);
    #print "find $parent for -$name -$suffix in $proj\n";

    my $array = $proj2PossibleDirs{$name};
    push(@$array, ($parent));
    $proj2PossibleDirs{$name}=$array;
}

$FH = STDIN;
$OUT_FH = STDOUT;
#open OUT_FH, ">", $org_setting or die $!;
while (my $line = <$FH>)
{
   chomp $line;
   my $id = 0;
   if ($line =~ m/^(\d+)>/)
   {
       $id = $1;
   }
   else
   {
       print "no id line: " . $line . "\n";
       next;
   }

   if ($line =~ m/(Rebuild All|Build) started: Project: ([^,]+)/i)
   {
       my $proj = $2;
       $id2Proj{$id} = lc($proj);
       #print "find project $proj for thread $id, the dir is @$proj2PossibleDirs{$proj}\n";
       next;
   }
   
   my $file = "";
   my $lineNum = 0;
   my $msg = "unknown pls check log file";
   #print "handle line: $line\n";
   if ($line =~ m/^(\d+)>([^()]+)\((\d+)\)\s*:\s*((fatal )?error C\d+:.*$)/)
   {
       $file = $2;
       $lineNum = $3;
       $msg = $4;
       #print "find the error file $line\n";

   }
   else
   {
       next;
   }

   #if $file is absolute path it also works
   my $projName = $id2Proj{$id};
   my $fileDir = "";
   my $possibleDir = "";
   my $possibleDirs = $proj2PossibleDirs{$projName};
   foreach $possibleDir (@$possibleDirs)
   {
       if (-e ($possibleDir . $file))
       {
           $fileDir = $possibleDir;
       }
   }
   print "correct dir: $fileDir\n";

   #print $file . ":" . $lineNum . ":" . $msg. " " . $projName . "--\n";
   my $newLine = $fileDir . $file . ":" . $lineNum . "::" . $msg;
   print $OUT_FH $newLine ."\n" or die $!;
}
close $OUT_FH;

$FH = STDIN;
$OUT_FH = STDOUT;
#open OUT_FH, ">", $org_setting or die $!;
while (my $line = <$FH>)
{
   chomp $line;

   my $file = "";
   my $lineNum = 0;
   my $msg = "unknown pls check log file";
   if ($line =~ m/^([^()]+)\((\d+)\) : ((fatal )?error C\d+:.*$)/)
   {
       $file = $1;
       $lineNum = $2;
       $msg = $3;
   }
   else
   {
       next;
   }
   my $fileDir = "";
   #print $file . ":" . $lineNum . ":" . $msg. " " . $projName . "--\n";
   my $newLine = $fileDir . $file . ":" . $lineNum . "::" . $msg;
   print $OUT_FH $newLine ."\n" or die $!;
}
close $OUT_FH;

