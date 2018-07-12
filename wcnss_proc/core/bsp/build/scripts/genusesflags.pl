#! /usr/bin/perl
#
#=============================================================================
#
# AMSS USES_xxx flags generator
#
# Description: 
# Create a list of all USES flags from the current build based on the BUILDID.
#   
# Copyright (c) 2009 QUALCOMM Incorporated. 
# All Rights Reserved.
# Qualcomm Confidential and Proprietary
#=============================================================================
#
#  $Header: //components/rel/core.wcnss/2.1.c16/core/bsp/build/scripts/genusesflags.pl#1 $
#  $DateTime: 2014/06/10 11:46:41 $
#  $Author: coresvc $
#  $Change: 6057513 $
#                      EDIT HISTORY FOR FILE
#                      
#  This section contains comments describing changes made to the module.
#  Notice that changes are listed in reverse chronological order.
#  
# when       who     what, where, why
# --------   ---     ---------------------------------------------------------
# 05/18/09   cjb     Created
#
#=============================================================================

use strict;
use Getopt::Long;
use File::Spec;
use Env;

my $buildid;
my $makeflags;
my $usage;

sub genusesflags($$); 
sub fileToArray($);
sub checkArgs;
sub Usage();
sub main();

#run
main();

sub main()
{
   my %buildid;
   my %makeflags;
   
   checkArgs();
   genusesflags($buildid, $makeflags);
   exit(0);
}

sub checkArgs 
{
   GetOptions(
      "buildid=s"=>\$buildid,       # Build ID
      "makeflags=s"=>\$makeflags,   # makeflags passed in to parse
   );
   
   print "# BUILDID: " . $buildid . "\n";
   print "# MAKEFLAGS: ". $makeflags . "\n";

   Usage() if $usage;
   if(!$buildid)
   {
      print "Missing required pararmeter -buildid <buildid>\n";
      Usage();
   }
}

sub genusesflags($$) {
   my $buildid = shift(@_);
   my $mflags = shift(@_);
  
   my @filearr;
   my $makeCmd; 
   my $oldpath;
   
   if ($mflags) {
	   @filearr = split(/ /, $mflags);
   } else {
      if ($^O eq "linux") {
         $makeCmd = 'sh linux_build '.$buildid. ' -m corebsp_setup -m -p';
      } else {
         if (-e '../../core/bsp/tools/incgen') {
				 $oldpath = $ENV{PATH};
             $ENV{PATH} = '../../core/bsp/tools/incgen\;' .$ENV{PATH}. '\;';
         } 
         $makeCmd = 'build.cmd '.$buildid. ' -m corebsp_setup -m -p';
      }
	   print "# Path: " .$ENV{PATH}. "\n";
	   print "# Make Command: " .$makeCmd. "\n";
      @filearr = fileToArray($makeCmd);
		if (-e '../../core/bsp/tools/incgen') {
			 $ENV{PATH} = $oldpath;
		} 
   }
   my $foundLine = 0;

   my @parts;
   my $varname;
   my $varvalue;
   my $varvalue_lc;
   
   print "# Autogenerated file\n";
   print "# Build ID: " .$buildid. "\n";
   print "# Command: " .$makeCmd. "\n";
   if ($mflags) {
   	print "# Based on Makeflags: " . $mflags . "\n";
	}
   print "\n";
   

   print "def exists(env):\n";
   print "   return env.Detect('usesflags')\n";
   print "\n";

   print "def generate(env):\n";
   
   foreach my $line (@filearr)
   {
      #remove any preceding whitespace
      $line =~ s/^\s+//;
      if ($line =~ /^USES_/)
      {
         #print "$line\n";
         $line =~ s/\(/{/g;
         $line =~ s/\)/}/g;
         $line =~ s/\n//g;
         $line =~ s/:=/=/g;
         $line =~ s/\?=/=/g;
         
         @parts = split(/=/, $line);
         $varname = $parts[0];
         $varvalue = $parts[1];

         # cleanup varname
         $varname =~ s/^\s+//;
         $varname =~ s/export//g;
         #$varname =~ s/EXPORT//g;
         $varname =~ s/define//g;
         $varname =~ s/\s//g;
         $varname =~ s/\./_/g;
         
         # cleanup varvalue
         $varvalue =~ s/^\s+//;
         $varvalue =~ s/\s//g;
         
         $varvalue_lc = lc($varvalue);
         
         if ($varvalue_lc =~ m/no/)
         {
            #print "   skip ".$varname." = \"".$varvalue."\")\n";
         }
         else
         {
            print "   env.Replace(" .$varname ." = \"". $varvalue. "\")\n";
         }
      }
   }

   # ensure the file is always loadable even if no uses flags exist
   print "   return None\n";
   return;
}

sub fileToArray($)
{
   my $cmd = shift(@_);
   #print "$cmd";
   open IN, "$cmd|" || die "failed executing $cmd";
   my @arr = <IN>;
   close IN;
   return @arr;
}

sub trim($)
{
   my $str = shift(@_);
   $str =~ s/^\s+//s;
   $str =~ s/\s+$//s;
   return $str;
}

sub Usage()
{
   my $usage = <<END;
Usage: perl genusesflags.pl -buildid <buildid>

Example:
cd build/ms
perl genusesflags.pl -builid SCTUUS > ../../core/bsp/build/data/usessctuus.py
END

   print $usage;
   exit;
}
