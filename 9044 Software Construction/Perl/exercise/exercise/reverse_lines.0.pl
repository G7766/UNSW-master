#!/usr/bin/perl -w
#1
# written by andrewt@cse.unsw.edu.au as a COMP2041 lecture example
# Print lines read from stdin in reverse order.
# In a C-style

while ($line = <STDIN>) {
    $line[$line_number++] = $line;
}


for ($line_number = $#line; $line_number >= 0 ; $line_number--) {
    print $line[$line_number];
}


#2
#Print lines read from stdin in reverse order. 
#Using <> in a list context 
@line = <STDIN>;
for ($line_number = $#line; $line_number >= 0 ; $line_number--) {
    print $line[$line_number];
}

#3
#Print lines read from stdin in reverse order. 
#Using <> in a list context & reverse 
@lines = <STDIN>;
print reverse @lines;

#4
#Print lines read from stdin in reverse order. 
#Using <> in a list context & reverse 
print reverse <STDIN>;

#5
#Print lines read from stdin in reverse order. 
#Using push & pop 
while ($line = <STDIN>) {
    push @lines, $line;
}
while (@lines) {
    my $line = pop @lines;
    print $line;
}
#6
#Print lines read from stdin in reverse order. 
#More succintly with pop 
@lines = <STDIN>;
while (@lines) {
    print pop @lines;
}

#7
#Print lines read from stdin in reverse order. 
#Using unshift 
while ($line = <STDIN>) {
    unshift @lines, $line;
}
print @lines;