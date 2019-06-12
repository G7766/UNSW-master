
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

//2b
//atoi 功 能: 把字符串转换成长整型数
//atof 功 能: 把字符串转换成浮点数
int main(int argc, char *argv[]){
	int i;
	StackInt();
	for( i=1; i<argc ; i++){
		StackPush(atoi(argv[i]));
	}
	while (!StackIsEmpty()){
		printf("%d\n", StackPop());
	}
	return 0;
}





