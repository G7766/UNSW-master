#!/usr/bin/perl -w

# simple example illustrating use of sorting comparison funcrion
# note use of <=?>

sub random_date {
    return sprintf "%02d/%02d/%04d", 1 + rand 28, 1 + rand 12, 2000+rand 20
}

sub compare_date {
    my ($day1,$month1,$year1) = split /\D+/, $a;
    my ($day2,$month2,$year2) = split /\D+/, $b;
    return $year1 <=> $year2 || $month1 <=> $month2 || $day1 <=> $day2;
}

push @random_dates, random_date() foreach 1..5;
print "random_dates=@random_dates\n";
@sorted_dates = sort compare_date @random_dates;
print "sorted dates=@sorted_dates\n";