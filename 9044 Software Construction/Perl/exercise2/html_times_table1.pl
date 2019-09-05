#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP2041 example
# print a HTML times table
#
# Note use of a hash to pass named parameters

sub html_times_table {
    my %parameters = @_;

    my $html = "<table border=$parameters{border} bgcolor=$parameters{bgcolor}>\n";

    foreach $y ($parameters{min_y}..$parameters{max_y}) {
        $html .= "<tr>";
        foreach $x ($parameters{min_x}..$parameters{max_y}) {
            $html .= sprintf "<td align=right>%s</td>", $x * $y;
        }
        $html .=  "</tr>\n";
    }

    $html .=  "</table>\n";

    return $html;
}

# easy to understand what each paramater does
print html_times_table(bgcolor=>'pink', min_y=>1, max_y=>12, border=>1, min_x=>1, max_x=>12);
