#!/bin/bash
<<eop
sed 's/ /\n/g' "$@"|      # convert to one word per line
tr A-Z a-z|               # map uppercase to lower case
sed "s/[^a-z']//g"|       # remove all characters except a-z and '
egrep -v '^$'|            # remove empty lines
sort|                     # place words in alphabetical order
uniq -c|                  # use uniq to count how many times each word occurs
sort -n                   # order words in frequency of occurrance



# 1
if test $# = 1
then
	start=1
	finish=$1
elif test $# = 2
then
	start=$1
	finish=$2
else
	echo "Usage: $0 <start> <finish>" 1>&2
	#exit 1
fi

for argument in "$@"
do
	# clumsy way to check if argument is a valid integer
	if echo "$argument"|egrep -v '^-?[0-9]+$' >/dev/null
	then
		echo "$0: argument '$argument' is not an integer" 1>&2
		exit 1
	fi
done

number=$start
while test $number -le $finish
do
	echo $number
	number=`expr $number + 1`    # or number=$(($number + 1))
done


#2
if (($# == 1))
then
	start=1
	finish=$1
elif (($# == 2))
then
	start=$1
	finish=$2
else
	echo "Usage: $0 <start> <finish>" 1>&2
	exit 1
fi

for argument in "$@"
do
	# This use of a regex is a bash extension missing from many Shells
	# It should be avoided if portability is a concern
	if [[ "$argument" =~ '^-?[0-9]+$' ]]
	then
		echo "$0: argument '$argument' is not an integer" 1>&2
		exit 1
	fi
done

number=$start
while ((number <= finish))
do
	echo $number
	number=$((number + 1))
done


eop



