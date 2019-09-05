#!/usr/bin/perl -w
# Written by andrewt@cse.unsw.edu.au  for COMP2041
# Simple cp implementation using line by line I/O
#1
die "Usage: $0 <infile> <outfile>\n" if @ARGV != 2;

$infile = shift @ARGV;
$outfile = shift @ARGV;

open my $in, '<', $infile or die "Cannot open $infile: $!";
open my $out, '>', $outfile or die "Cannot open $outfile: $!";

while ($line = <$in>) {
    print $out $line;
}

close $in;
close $out;
exit 0;

#2
#Simple cp implementation using line by line I/O relying on the default variable $_ 
die "Usage: $0 <infile> <outfile>\n" if @ARGV != 2;

$infile = shift @ARGV;
$outfile = shift @ARGV;

open my $in, '<', $infile or die "Cannot open $infile: $!";
open my $out, '>', $outfile or die "Cannot open $outfile: $!";

# loop could also be written in one line:
# print OUT while <IN>;
