#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP[29]041 example
# implementations of Perl's push

sub my_push1 {
    my ($array_ref,@elements) = @_;

    @$array_ref = (@$array_ref, @elements);

    return $#$array_ref + 1;
}


# same but with prototype
sub my_push2(\@@) {
    my ($array_ref,@elements) = @_;

    @$array_ref = (@$array_ref, @elements);

    return $#$array_ref + 1;
}

sub mypush2 {
    my ($array_ref,@elements) = @_;
    if (@elements) {
        @$array_ref = (@$array_ref, @elements);
    } else {
        @$array_ref = (@$array_ref, $_);
    }
}

@a = (1..5);

# note explicitly passing an array reference \@a
my_push1 \@a, 10..15;

# note prototype allows caused reference to array to be passed
my_push2 @a, 20..25;

# prints 1 2 3 4 5 10 11 12 13 14 15 20 21 22 23 24 25
print "@a\n";
