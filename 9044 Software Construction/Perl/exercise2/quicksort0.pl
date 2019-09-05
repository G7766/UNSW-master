#!/usr/bin/perl -w

@list = randomize_list(1..20);
print "@list\n";
@sorted_list0 = sort {$a <=> $b} @list;
print "@sorted_list0\n";
@sorted_list1 = quicksort0(@list);
print "@sorted_list1\n";
@sorted_list2 = quicksort1(sub {$a <=> $b}, @list);
print "@sorted_list2\n";

sub quicksort0 {
    return @_ if @_ < 2;
    my ($pivot,@numbers) = @_;
    my @less = grep {$_ < $pivot} @numbers;
    my @more = grep {$_ >= $pivot} @numbers;
    my @sorted_less = quicksort0(@less);
    my @sorted_more = quicksort0(@more);
    return (@sorted_less, $pivot, @sorted_more);
}


sub quicksort1 {
    my ($compare) = shift @_;
    return @_ if @_ < 2;
    my ($pivot, @input) = @_;
    my (@less, @more);
    partition1($compare, $pivot, \@input, \@less, \@more);
    my @sorted_less = quicksort1($compare, @less);
    my @sorted_more = quicksort1($compare, @more);
    my @r = (@sorted_less, $pivot, @sorted_more);
    return (@sorted_less, $pivot, @sorted_more);
}

sub partition1 {
    my ($compare, $pivot, $input, $smaller, $larger) = @_;
    foreach $x (@$input) {
        our $a = $x;
        our $b = $pivot;
        if (&$compare  < 0) {
            push @$smaller, $x;
        } else {
            push @$larger, $x;
        }
    }
}

sub randomize_list {
    my @newlist;
    while (@_) {
        my $random_index = rand @_;
        my $r = splice @_,  $random_index, 1;
        push @newlist, $r;
    }
    return @newlist;
}