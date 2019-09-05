#!/bin/sh
# written by andrewt@cse.unsw.edu.au as a COMP2041 case study, Aug 2017
#
# Run as plagiarism_detection.simple_diff.sh <files>
#
# Report if any of the files are copies of each other
#
# The use of diff -iw means changes in white-space or case won't affect comparisons

for file1 in "$@"
do
    for file2 in "$@"
    do
        test "$file1" = "$file2" && break
        if diff -i -w "$file1" "$file2" >/dev/null
        then
            echo "$file1 is a copy of $file2"
        fi
    done
done
