#include<stdio.h>
#include<stdlib.h>
#define LEN(x) (sizeof(x)/sizeof(x[0]))

#define M 3
#define N 4
#define P 4

/*
float innerProduct(float a[], float b[], int n)
{
	int length;
	length = sizeof(a)/sizeof(a[0]);
	for(int j = 0; j<=length; j= j+1){
		n = n + (a[j] * b[j]);
	}
	return n;
}


int main()
{
	float a[3]={1,2,3};
	float b[3]={3,4,5};
	int n=LEN(a);
	innerProduct(a,b,n);
	printf("%d\n", n);
}
*/

float innerProduct(float a[], float b[], int n)
{
	float result = 0.0;
	for(int j = 0; j<=n; j= j+1){
		result = result + (a[j] * b[j]);
	}
	return result;
}

void matrixProduct(float a[M][N], float b[N][P], float c[M][P])
{
	for(int i = 0; i<M; i++){
		for(int j = 0;j<N;j++){
			c[i][j]=0.0;
			for(int k = 0;k<N;k++){
				c[i][j] += a[i][k] * b[k][i];
			}
		}
	}
}

int main()
{
	float a[3]={1,2,3};
	float b[3]={3,4,5};
	int n=LEN(a);
	float r = innerProduct(a,b,n);
	printf("%d\n", n);
	printf("%f\n", r);
}


