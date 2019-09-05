#!/bin/sh
#
# written by andrewt@cse.unsw.edu.au as a COMP2041 case study, Aug 2017
#
# Improved version of plagiarism_detection.comments.sh
#
# This version converts  C strings to the letter 's'
# and it converts identifiers to the letter 'v'.
# Hence changes in strings & identifiers won't prevent detection of plagiarism.

# The substitution s/"["]*"/s/g changes strings to the letter 's'
# This pattern won't match a few C strings which is fine for our purposes
#
# The  s/[a-zA-Z_][a-zA-Z0-9_]*/v/g changes all variable names to 'v'
# which means changes to variable names won't affect comparison.
# Note this  also may change function names, keywords etc.
# This is fine for our purposes.


TMP_FILE1=/tmp/plagiarism_tmp1$$
TMP_FILE2=/tmp/plagiarism_tmp2$$
substitutions='s/\/\/.*//;s/"[^"]"/s/g;s/[a-zA-Z_][a-zA-Z0-9_]*/v/g'

for file1 in "$@"
do
    for file2 in "$@"
    do
        test "$file1" = "$file2" && break # don't compare pairs of assignments twice
        sed "$substitutions" "$file1" >$TMP_FILE1
        sed "$substitutions" "$file2" >$TMP_FILE2
        if diff -i -w $TMP_FILE1 $TMP_FILE2 >/dev/null
        then
            echo "$file1 is a copy of $file2"
        fi
    done
done
rm -f $TMP_FILE1 $TMP_FILE2
