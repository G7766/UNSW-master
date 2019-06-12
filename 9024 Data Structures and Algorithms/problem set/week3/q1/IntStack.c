
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

int main(){
	printf("Stack:\n");
	StackRep s;
	StackPush(2);
	int a = StackPop();
	printf("%d\n",a);

}