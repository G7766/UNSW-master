#!/usr/bin/perl -w

# Reads lines of input until end-of-input
# Print snap! if a line has been seen previously

while (1) {
    print "Enter line: ";
    $line = <STDIN>;
    if (!defined $line) {
        last;
    }
    if ($seen{$line}) {
        print "Snap!\n";
    }
    $seen{$line}++;
}
