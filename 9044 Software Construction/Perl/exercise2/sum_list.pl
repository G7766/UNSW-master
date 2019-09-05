#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au
# 3 different ways to sum a list
# - illustrating various aspects of Perl

# simple for loop
sub sum_list0 {
    my (@list) = @_;
    my $total = 0;
    foreach $element (@list) {
       $total += $element;
    }
    return $total;
}

# recursive
sub sum_list1 {
    my (@list) = @_;
    return 0 if !@list;
    return $list[0] + sum_list1(@list[1..$#list]);
}

# join+eval - interesting but not recommended
sub sum_list2 {
    my (@list) = @_;
    return eval(join("+", @list))
}

print sum_list0(1..10), " ", sum_list1(1..10), " ", sum_list2(1..10),  "\n";
