package Example_Module;
# written by andrewt@cse.unsw.edu.au for COMP2041 
# 
# Definition of a simple Perl module.
#
# List::Util provides the functions below and more

use base 'Exporter';
our @EXPORT = qw/sum min max minstr maxstr/;
use List::Util qw/reduce/;


sub sum {
	return reduce {$a + $b} @_;
}

sub min {
	return reduce {$a < $b ? $a : $b} @_;
}

sub max {
	return reduce {$a > $b ? $a : $b} @_;
}

sub minstr {
	return reduce {$a lt $b ? $a : $b} @_;
}

sub maxstr {
	return reduce {$a gt $b ? $a : $b} @_;
}

# necessary
1;
