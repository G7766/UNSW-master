#!/usr/bin/perl -w
# Written by andrewt@cse.unsw.edu.au for COMP2041
# Simple cp implementation via system!
# Will break if filenames contain single quotes

die "Usage: $0 <infile> <outfile>\n" if @ARGV != 2;

$infile = shift @ARGV;
$outfile = shift @ARGV;

exit system "/bin/cp '$infile' '$outfile'";
