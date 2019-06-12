/**
     poG.c

     Assignment 2: Partial Order Graphs

     COMP9024 18s2
    // ********** TASK A **********
	// Here is TASK A:
	//Before i print the partial order, i use two for iteration and check function to get a binarry array
	// out of the check function the time complexity is n^2
	// In the check function the number of decimal p is m, and the worst condition of the time complexity is m^2
	// so the time complexity O(n*n*m*m)
	// The time complexity is : O(n^2)  n is represent for the number of divisors of p 
	//In function show_Partial_order1: there are two for iteration, 
	//the first one is check every n and the the second for iteration is check the rest of n
	//so the time complexity is O(n^2)
	//(n+n-1+n-2+....1) = n*(n-1)/2
	//                            => O(n^2)
	//O(n*n*m*m) + O(n^2) = O(n*n*m*m)

    // ********** TASK B **********
	// Here is TASK B:
	// I wrote a function  find_longest_number to check the max length of path
	//it is a regression of the path and increase number max
	//the worst condition is that it needs O(n^2) to get the max number
	// When the max path is 0+1 =1 then just print all the advisor
	//else we need to find out all the path that the length is equal to the max length 
	//in next_node function which is also a regression to add the advisor to the path and check the length
	//it is  a O(n^n) step because the for iteration out of the regression is n, and inside the regression 
	// check start from 0 to n and there are n level
	//so the worst condition is time complexity is O(n^n)
	//but there is a for iteration out of the function
	// so the time complexity is O(n*n^n)
**/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>
#include <math.h>

//#include "Graph.c"

#define LENGTH 1000
int t[1001][1001];

int max_l[1000];
int visited[LENGTH];
int max_length = 0;
int indx = 0;
int NODES=0;


int* advisor(p){
	//printf("P is: %d\n",p);
	int *node_list = malloc(sizeof(int)*LENGTH);
	assert(node_list!=NULL);

	int j=0;
	int i=1;
	while(i<p){
		if(p%i==0){
			node_list[j]=i;
			j++;
		}
		i++;
	}
	node_list[j]=p;
	//printf("j:%d",j);
	NODES =j+1;
	//printf("NODES:%d",NODES);
	/*
	for(int i =0;i<=j;i++){
		printf("%d,",node_list[i] );
	}
	*/
	return node_list;
}
/*
int len(int *l){
	int j=0;
	for(int i=0;i<1000;i++){
		if(l[i]!=0){
			j++;
		}
		else{
			return j;
		}
	}
	return j;
}
*/
int check(int i, int j){
	if(j<0 ||i<0){
		return 0;
	}
	char *ii = malloc(sizeof(char)*11);
	assert(ii!=NULL);
	char *jj = malloc(sizeof(char)*11);
	assert(jj!=NULL);
	//char ii[11] ;
	//char jj[11];
	sprintf(ii,"%d",i);
	sprintf(jj,"%d",j);
	//printf("i: %d ,j: %d\n",i,j);
	//printf("strlen(ii): %lu ,strlen(jj): %lu\n",strlen(ii),strlen(jj));

	//for(int m=0;m<strlen(ii);m++){
	//	printf("ii[m]:%hhd\n",ii[m]);
	//}
	//printf("ii:%s\n",ii);

	if(j%i!=0){
		return 0;
	}
	int tag=0;
	int m,n;
	for(m=0;m<strlen(ii);m++){
		for(n=0;n<strlen(jj);n++){
			if(ii[m]==jj[n]){
				tag++;
				//printf("m:%c n:%c\n",ii[m],jj[n]);
				//jj[n]= -1;
				ii[m]= -1;
				//printf("tag:%d\n",tag );
			}
			if(tag == strlen(ii)){
				return 1;
			}
		}
	}
	return 0;
}

/*
void show_Partial_order(Graph g,int *l){
	//showGraph(g);
	printf("Partial order:\n");
	int m=0;
	for(int i=0;i<g->nV;i++){
		if(l[i]!=0){
			m++;
		}
	}
	//printf("!!!!!!!!!!!!!!!!!!!!!!!!m:%d\n",m);
	for (int i = 0; i < m; i++){
		printf("%d:",l[i]);
		for (int j = i+1; j < m; j++){
			if (g->edges[i][j]){
				printf(" %d",l[j]);
			}
		}
		printf("\n");
	}
}
*/
void show_Partial_order1(int *l,int N){
	printf("Partial order:\n");
	//printf("!!!!!!!!!!!!!!!!!!!!!!!!m:%d\n",m);
	int i,j;
	for (i = 0; i < N; i++){
		printf("%d:",l[i]);
		for (j = i+1; j < N; j++){
			if (t[i][j]){
				printf(" %d",l[j]);
			}
		}
		printf("\n");
	}
}


int max_and_pos(int *arr,int N){
	int i,max;
	max = arr[0];
	for(i = 1;i<N;i++){
		if(max < arr[i]){
			max = arr[i];
		}
	}
	return max;
}



int count_path(int *l,int N){
	int count=0;
	int i;
	for(i=0;i<N;i++){
		if(l[i]!=0){
			count++;
		}
	}
	return count;
}

int* clear_path(int *l,int N, int n){
	int i;
	for(i=n;i<N;i++){
		l[i]=0; 
	}
	return l;
}
void show_path(int *l,int N){
	int i;
	for(i=0; i<N;i++){
		printf("%d\n", l[i]);
	}
}
void show_actual_path(int *p,int *l,int N){
	int k=0;
	int i,j;

	for(i=0; i<N;i++){
		if(p[i]==1){
			printf("%d", l[i]);
			k = i+1;
			break;
		}
	}
	for(j=k;j<N;j++){
		if(p[j]==1){
			printf(" < %d", l[j]);
		}
	}
	printf("\n");
}
void append(int n){
	int i;
	for(i=0;i<1000;i++){
		if(max_l[i]==0){
			max_l[i]=n;
			return;
		}
		else{
			continue;
		}
	}
}
void find_longest_number(int max,int i,int N){
	int ini=max;
	int j;
	for(j=0;j<N;j++){
		if(t[i][j]==1){
			max=max+1;
			//printf("%d\n",max);
			append(max);
			find_longest_number(max,j,N);
			max =ini;
		}
		else{
			continue;
		}
	}
}

void next_node(int i, int N, int max_length,int *p,int *L){
	//printf(" a\n");
	//printf("??:%d\n",t[1][3]);
	int j;
	for(j=0;j<N;j++){
		if(t[i][j]==1){
			//path[j]=1;
			//printf(" %d",j);
			p[j]=1;
			next_node(j,N,max_length,p,L);
			//printf("\n");
			//show_path(p,N);
			if(count_path(p,N)==max_length){
				//printf("\n");
				//printf("!!!!");
				show_actual_path(p,L,N);

			}
			p = clear_path(p,N,j);
		}
		else{
			continue;
		}
	}
	
}




int main(int argc, char *argv[]) {
	//char_to_int(*argv[1]);
	//printf("Input Number: %s\n",argv[1]);
	int p = atoi(argv[1]);
	int* L = advisor(p);
	int size=0;
	//int NODES = size;
	//printf("\n");
	//printf("length:%d\n",NODES );
	//printf("test\n");
	int i,j;
	
	for (i = 0; i < NODES-1; i++){
		for (j = i+1; j < NODES; j++){
			//printf("i:%d , j:%d\n", i,j);
			if (check(L[i],L[j])==1){
				t[i][j]=1;
			}
			else{
				t[i][j]=0;
			}
		}
	}


	show_Partial_order1(L,NODES);


	int max = 1;
	for(i=0;i<NODES;i++){
		find_longest_number(max,i,NODES);
	}



	int max_length = max_and_pos(max_l,1000);
	//printf("max_length:%d\n", max_length);

	
	printf("\n");
	printf("Longest monotonically increasing sequences:\n");
	//printf("Longest:%d\n", max_length);
	if (max_length==0){
		for(i=0;i<NODES;i++){
			printf("%d\n", L[i]);
		}
	}
	else{
		//printf("Longest:%d\n",max_length);
		for(i=0;i<NODES;i++){
			int p[1000]={0};
			p[i]=1;
			//printf("%d :", i);
			next_node(i,NODES,max_length,p,L);
			//printf("\n");
		}
		//printf("\n");x
	}
	
	
}








