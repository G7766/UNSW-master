#!/usr/bin/perl -w
# Written by andrewt@cse.unsw.edu.au for COMP2041
# Simple cp implementation reading entire file into array
# note that <> returns an array of lines
# in a list context (in a scalar context it returns a single line)

die "Usage: $0 <infile> <outfile>\n" if @ARGV != 2;

$infile = shift @ARGV;
$outfile = shift @ARGV;

open my $in, '<', $infile or die "Cannot open $infile: $!";
@lines = <$in>;
close $in;

open my $out, '>', $outfile or die "Cannot open $outfile: $!";
print $out @lines;
close $out;

exit 0;
