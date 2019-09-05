#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP2041 example
# rename specified files using specified Perl code
# For each file the Perl code  is executed with $_ set to the filename
# and the file is renamed to the value of $_ after the execution.
# /usr/bin/rename provides this functionality

die "Usage: $0 <perl> [files]\n" if !@ARGV;
$perl_code = shift @ARGV;
foreach $filename (@ARGV) {

    $_ = $filename;
    eval $perl_code;
    die "$0: $?" if $?; # eval leaves any error message in $?
    $new_filename = $_;

    next if $filename eq $new_filename;

    die "$0: $new_filename exists already\n" if -e $new_filename;

    rename $filename, $new_filename or
        die "$0: rename '$filename' -> '$new_filename' failed: $!\n";
}
