#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP[29]041 lecture example

# This shows a bug due to a missing my declaration

# In this case the use of $i in is_prime without
# a my declarations changes $i outside the function
# and breaks the while loop calling the function

sub is_prime {
    my ($n) = @_;
    $i = 2;
    while ($i < $n) {
        return 0 if $n % $i == 0;
        $i++;
    }
    return 1;
}

$i = 0;
while ($i < 1000) {
    print "$i\n" if is_prime($i);
    $i++;
}
