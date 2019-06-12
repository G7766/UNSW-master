#include <stdlib.h>
#include <stdio.h>
#include "IntStack.h"
#include "IntStack.c"


int main(){
	int n,k,i;
	printf("Enter a number:");
	scanf("%d",&n);
	printf("Change to base:");
	scanf("%d",&k);

	StackInt();
	while(n!=0){
		i = n%k;
		StackPush(i);
		n = n/k;
	}
	printf("Here is result:\n");
	while (!StackIsEmpty()){
		printf("%d",StackPop());
	}
	putchar('\n');
	return 0;
}