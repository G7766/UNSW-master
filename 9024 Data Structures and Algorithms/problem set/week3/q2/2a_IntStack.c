
#include "IntStack.h"
#include <assert.h>
#include <stdio.h>

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

//2a

int main(){
	printf("Stack start!\n");
	StackInt();
	int n;
	printf("Enter a positive number:");
	//scanf("%d",&n);
	//if (n<0){
	//	printf("The number is not positive!\n");
	//}
	if(scanf("%d",&n) == 1 && (n > 0)){
		for(int i=0;i < n;i++){
			int q;
			printf("Enter a number:");
			scanf("%d",&q);
			StackPush(q);
		}
		//StackPush(2);
		//int k = StackIsEmpty();
		while (!StackIsEmpty()) {
			//int z = StackPop();
			printf("%d\n",StackPop());
		}
	}
	return 0;
}





