#!/bin/bash
echo "Hello World!"

your_name="Tim"
echo $your_name
echo ${your_name}

for skill in Ada Coffee Action Java; do
	echo "i am good at ${skill} Script"
done

myUrl="localhost:8080"
readonly myUrl


#string="abcd"
#echo ${#string}
#unset string

string="runnoob is a great site"
#echo `expr index "$string" io`
#expr index 'alibaba is a great company' is
temp=${string%%i*}
echo $((${#temp}+1))

array_name=(
a
b
c
d
)
echo "$array_name[0]"
echo ${array_name[0]}
length=${#array_name[*]}
length1=${#array_name[@]}
length2=${#array_name[n]}
echo $length $length1 $length2

:<<EOF
XCAS
sadas
sadasd
EOF


echo '$0' is "$0"
echo '$1' is "$1"


echo -n "Enter your name:"
read name
echo Hello, $name



url='http://localhost'
curl "$url"