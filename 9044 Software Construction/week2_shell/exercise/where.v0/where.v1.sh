#!/bin/sh
# Print all occurances of executable programs with the specified names in $PATH
# written by geoffw@cse.unsw.edu.au as a COMP2041 example
# Note use of tr to produce a list of directories one per line
# suitable for a while loop.
# Won't work if directories contain spaces (fixing this left as an exercise)

if test $# = 0
then
    echo "Usage $0: <program>" 1>&2
    exit 1
fi

for program in "$@"
do
    echo "$PATH"|
    tr ':' '\n'|
    while read directory
    do
        f="$directory/$program"
        if test -x "$f"
        then
            ls -ld "$f"
        fi
    done|
    egrep '.' || echo "$program not found"
done
