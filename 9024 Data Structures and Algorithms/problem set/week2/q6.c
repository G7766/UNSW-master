#include<stdio.h>
#include<stdlib.h>
#define LEN(x) (sizeof(x)/sizeof(x[0]))
#define MAX 10

int max(int a, int b, int c) {
   int d = a * (a >= b) + b * (a < b);   // d is max of a and b （a>=b）? 1 or 0
   										 // (a<b)?  1 or 0
   return  c * (c >= d) + d * (c < d);   // return max of c and d
}





