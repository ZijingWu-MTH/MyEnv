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
   if ($line =~ m/^\s*([^()]+)\((\d+),(\d+)\): ((fatal )?error CS\d+:.*)\[(.*)\]$/)
   {
       my ($projName,$projParent,$projSuffix) = fileparse($6);
       $file = $projParent . "\\" . $1;
       $lineNum = $2;
       $colNum = $3;
       $msg = $4;
   }
   else
   {
       next;
   }

   my $fileDir = "";
   #print $file . ":" . $lineNum . ":" . $msg. " " . $projName . "--\n";
   my $newLine = $fileDir . $file . ":" . $lineNum . ":" . $colNum . ":" . $msg;
   print $OUT_FH $newLine ."\n" or die $!;
}
close $OUT_FH;

