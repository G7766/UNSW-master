#include <stdio.h>
#include <stdlib.h>
#define len(x) (sizeof(x)/sizeof(x[0]))
// int i=sizeof(a)/sizeof(a[0])

int main(){

	int *numberID;
	int n = 123456789;
	int m;
	numberID = (int*)malloc(sizeof(int)*m);
	int i =0;
	while (n!=0){
		int z;
		z = n % 10;
		//printf("%d\n",z);
		numberID[i]=z;
		i++;
		n = n/10;
	}
	printf("here is i :%d\n",i);
	//int q = sizeof(numberID);
	//printf("size of numberID: %d\n",q);
	
	for(int j=0; j<i; j++){
		printf("%d\n", numberID[j]);
	}

	printf("size: %lu\n",len(numberID));
	
	printf("first element %d\n:",numberID[i-1]);



	int xz[6]={211,42,53,64,85,12};
	int len=0;
	int q,l=0;
	while (xz[l]){
		printf("xz:%d\n",xz[l]);
		l=l+1;
	}
	printf("len: %d\n",l);
	return 0;
}

