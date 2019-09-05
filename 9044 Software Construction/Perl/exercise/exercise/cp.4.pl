#!/usr/bin/perl -w
# Written by andrewt@cse.unsw.edu.au for COMP2041
# Simple cp implementation reading entire file into array
# $/ contains the line separator for Perl
# if it is undefined we can slurp an entire file
# into a scalar variable with a single read

die "Usage: cp <infile> <outfile>\n" if @ARGV != 2;
$infile = shift @ARGV;
$outfile = shift @ARGV;

undef $/;
open my $in, '<', $infile or die "Cannot open $infile: $!";
$contents = <$in>;
close $in;

open my $out, '>', $outfile or die "Cannot open $outfile: $!";
print $out $contents;
close $out;

exit 0;
