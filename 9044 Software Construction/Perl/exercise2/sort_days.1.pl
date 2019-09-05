#!/usr/bin/perl -w

# Simple example of sorting a list based on the values in a hash.
# This is very common pattern in Perl.
# modified version ilustration Perl quote word operator and a hash slice

# Perl's quote appropriate is a convenient way to create a list of words
@days = qw/Sunday Monday Tuesday Wednesday Thursday Friday Saturday/;

# Perl allows you to assign to multiple values in a hash simultaneously
@days{@days} = (0..6);

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
