#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP2041 lecture example
# More concise version of snap_memory.0.pl

while (1) {
    print "Enter line: ";
    $line = <STDIN>;
    last if !defined $line;
    print "Snap!\n" if $seen{$line};
    $seen{$line} = 1;
}
