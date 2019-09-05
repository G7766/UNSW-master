#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au as a COMP[29]041 example
# implementations of Perl's split & join

sub my_join {
    my ($separator, @list) = @_;

    return "" if !@list;

    my $string = shift @list;
    foreach $thing (@list) {
        $string .= $separator . $thing;
    }

    return $string;
}

sub my_split1 {
    my ($regexp, $string) = @_;
    my @list = ();

    while ($string =~ /(.*)$regexp(.*)/) {
        unshift @list, $2;
        $string = $1;
    }
    unshift @list, $string if $string ne "";

    return @list;
}

sub my_split2 {
    my ($regexp, $string) = @_;

    my @list = ();
    while ($string =~ s/(.*?)$regexp//) {
        push @list, $1;
    }
    push @list, $string if $string ne "";

    return @list;
}

$s = my_join("+", 1..5);

# prints 1+2+3+4+5 = 15
print "$s = ", eval $s, "\n";

# prints 2 4 8 16
@a = my_split1(",", "2,4,8,16");
print "@a\n";

# prints 2 4 8 16
@a = my_split2(",", "2,4,8,16");
print "@a\n";
