#include<stdio.h>

#define min 10000
#define max 24999

/*
int main()
{
	int flag = 0;
	char *z;
	char list[5];
	//for(int i=10000;i<=99999;i = i + 1){
	for(int i = 0;i < 5;i = i + 1){
		sprintf(z,"%d",i);             //将数字i 赋值在 ‘%d’中 赋值给 字符串z
		list[i] = *z;
	}
	printf("%s\n",list);


	int a=1234;
	int b=1234;
	if (a==b){
		printf("True\n" );
	}
	else{
		printf("False\n");
	}

}
*/

int main()
{
	int a,b,c,d,e;
	for(int i=min; i<=max; i=i+1){
		a = (i/10000) % 10;
		b = (i/1000) % 10;
		c = (i/100) % 10;
		d = (i/10) % 10;
		e = (i/1) % 10;
		int value = (e*10000) + (d*1000) + (c*100) + (b*10) + (a);
		if (i == value){
			printf("%d\n", i );
		}
	}
	return 0;
}