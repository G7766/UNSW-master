#!/usr/bin/perl -w

# Simple example of sorting a list based on the values in a hash.
# This is very common pattern in Perl.

%days = (Sunday => 0, Monday => 1, Tuesday => 2, Wednesday => 3,
         Thursday => 4, Friday => 5, Saturday => 6);

sub random_day {
    my @days = keys %days;
    return $days[rand @days];
}

sub compare_day {
    return $days{$a} <=> $days{$b};
}

push @random_days, random_day() foreach 1..5;
print "random days = @random_days\n";
@sorted_days = sort compare_day @random_days;
print "sorted days = @sorted_days\n";
