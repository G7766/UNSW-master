#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au

# 8 different ways to print the odd numbers in
# a list - illustrating various aspects of Perl

# simple for loop
sub print_odd0 {
    my (@list) = @_;

    foreach $element (@list) {
        print "$element\n" if $element % 2;
    }
}

# simple for loop using index
sub print_odd1 {
    my (@list) = @_;

    foreach $i (0..$#list) {
        print "$list[$i]\n" if $list[$i] % 2;
    }
}

# set $_ in turn to each item in list
# evaluate supplied expression
# print item if the expression evaluates to true

sub print_list0 {
    my ($select_expression, @list) = @_;
    foreach $_ (@list) {
        print "$_\n" if &$select_expression;
    }
}

# more concise version of print_list0
sub print_list1 {
   &{$_[0]} && print "$_\n" foreach @_[1..$#_];
}


# set $_ in turn to each item in list
# evaluate supplied expression
# return a list of items for which the expression evaluated to true
sub my_grep0 {
    my $select_expression = $_[0];
    my @matching_elements;
    foreach $_ (@_[1..$#_]) {
        push @matching_elements, $_ if &$select_expression;
    }
    return @matching_elements;
}


# more concise version of my_grep0
sub my_grep1 {
    my $select_expression = shift;
    my @matching_elements;
    &$select_expression && push @matching_elements, $_ foreach @_;
    return @matching_elements;
}

# calling helper function which returns
# list items selected by an expression
sub print_odd4 {
    my @odd = my_grep0 sub {$_ % 2}, @_;
    foreach $x (@odd) {
        print "$x\n";
    }
}


@numbers = (1..10);

# all 8 statements print the numbers 1,3,5,7,9 one per line

print_odd0(@numbers);

print_odd1(@numbers);

print_list0(sub {$_ % 2}, @numbers);

print_list1(sub {$_ % 2}, @numbers);

print_odd4(@numbers);

my_grep1 sub {odd $_ && print "$_\n"}, @_;

# using built-in grep and combining print
grep {$_ % 2 && print "$_\n"} @numbers;

# using built-in grep and join
print join("\n", grep {$_ % 2} @numbers), "\n";
