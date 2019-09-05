#!/bin/sh
# create 1001 C files, compile and runs them

# file f$i.c contains a defintion of function f$i which returns $i
# for example file42.c will contain a function f42 that returns 42
#
# main.c contains code to call all 1000 functions
# and print the sum of their return values


# add the initial lines to main.c
# note the use of quotes on eof to disable variable interpolation
# in the here document

#创建main.c 把放进去， 'eof' 加引号没效果
cat >main.c <<'eof'
#include <stdio.h>

int main(void) {
    int v = 0 ;
eof

i=0
#while test $i -lt 1000
while test $i -lt 10
do
    # add a line to main.c to call the function f$i

    cat >>main.c <<eof
    int f$i(void);
    v += f$i();
eof

    # create file$i.c containing function f$i

    cat >file$i.c <<eof
int f$i(void) {
    return $i;
}
eof

    i=$((i + 1))
done

cat >>main.c <<'eof'
    printf("%d\n", v);
    return 0;
}
eof

# compile and run the 11 C files

time clang main.c file*.c
./a.out
