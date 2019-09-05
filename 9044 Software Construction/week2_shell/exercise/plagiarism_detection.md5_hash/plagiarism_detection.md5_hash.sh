#!/bin/sh
#
# written by andrewt@cse.unsw.edu.au as a COMP2041 case study, Aug 2017
#
# Improved version of plagiarism_detection.reordering.sh
#
# Note use md5sum to calculate a Cryptographic hash of the modified file
#  http://en.wikipedia.org/wiki/MD5
# and then use sort && uniq to find files with the same hash
#
# This allows  execution time linear in the number of files

substitutions='s/\/\/.*//;s/"[^"]"/s/g;s/[a-zA-Z_][a-zA-Z0-9_]*/v/g'

for file in "$@"
do
    echo `sed "$substitutions" "$file"|sort|md5sum` $file
done|
sort|
uniq -w32 -d --all-repeated=separate|
cut -c36-
