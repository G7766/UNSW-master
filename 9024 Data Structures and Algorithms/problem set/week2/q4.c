#include<stdio.h>
#include<stdlib.h>
#define LEN(x) (sizeof(x)/sizeof(x[0]))
#define MAX 10

void fun1(int n)
{
	printf("%d\n", n);
	while (n!=1){
		if(n%2==0){
			n = (n/2);
		}
		else{
			n = (3*n+1);
		}
		printf("%d\n",n );
	}
}

int Fibonacci(int n)
{
	int fib[MAX]={1,1};
	if(n>2 && n<=10 )
	{
		for(int i=2; i< n;i++)
		{
			fib[i] = fib[i-1] + fib[i-2];
		}
	}
	for(int i=0;i<n;i++)
	{
		printf("Fib[%d] = %d\n",i+1,fib[i] );
		fun1(fib[i]);
	}
	return 0;
}


int main(void)
{
	Fibonacci(4);
}

