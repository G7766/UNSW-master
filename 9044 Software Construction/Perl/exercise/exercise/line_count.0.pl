#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP2041 lecture example
# Count the number of lines on standard input.
#1
=pod
$line_count = 0;
while (1) {
    $line = <STDIN>;
    last if !$line;
    $line_count++;
}
print "$line_count lines\n";

#2
$line_count = 0;
while (<STDIN>) {
    $line_count++;
}
print "$line_count lines\n";
=cut
#3
$line_count = 0;
$line_count++ while <STDIN>;
print "$line_count lines\n";

#4
#Count the number of lines on standard input. read the input into an array and use the array size. 
@lines = <STDIN>;
print $#lines+1, " lines\n";
#5
#Count the number of lines on standard input. 
#Assignment to () forces a list context and hence reading all lines of input. 
#The special variable $. contains the current line number

() = <STDIN>;
print "$. lines\n";