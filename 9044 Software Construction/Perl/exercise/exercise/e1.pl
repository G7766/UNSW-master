#!/usr/bin/perl -w
# writen by andrewt@cse.unsw.edu.au as a COMP2041 example
# Perl implementation of /bin/echo
# always writes a trailing space
#1
foreach $arg (@ARGV) {
    print $arg, " ";
}
#2
print "\n";

#3
print "@ARGV\n";
#4
print join(" ", @ARGV), "\n";
#5
$sum = 0;
foreach $arg (@ARGV) {
    $sum +=$arg;
}
print "Sum of the number is $sum\n";

#6
while (1) {
    print "Enter array index: ";
    $n = <STDIN>;
    if (!$n) {
        last;
    }
    chomp $n;
    $a[$n] = 42;
    print "Array element $n now contains $a[$n]\n";
    printf "Array size is now %d\n", $#a+1;
}