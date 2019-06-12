
#include "IntStack.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct 
{
	int item[MAXITEMS];
	int top;
}StackRep;


static StackRep stackObject;

void StackInt(){
	stackObject.top = -1;
}

int StackIsEmpty(){
	return (stackObject.top < 0);
}

void StackPush(int n){
	assert(stackObject.top < MAXITEMS -1);
	stackObject.top++;
	int i = stackObject.top;
	stackObject.item[i] = n;
}

int StackPop(){
	assert(stackObject.top < MAXITEMS -1);
	int i = stackObject.top;
	int n = stackObject.item[i];
	stackObject.top--;
	return n;
}

//3a
/*
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
*/


/* solution:
int main(int argc, char *argv[]) {
   int n;

   if (argc != 2) {
      printf("Usage: %s number\n", argv[0]);
      return 1;
   }

   StackInit();
   n = atoi(argv[1]);
   while (n > 0) {
      StackPush(n % 2);
      n = n / 2;
   }
   while (!StackIsEmpty()) {
      printf("%d", StackPop());
   }
   putchar('\n');
   return 0;
}


*/


