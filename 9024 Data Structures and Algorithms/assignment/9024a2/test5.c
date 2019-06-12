/**
     poG.c

     Assignment 2: Partial Order Graphs

     COMP9024 18s2
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
	/*
	for(int i =0;i<=j;i++){
		printf("%d,",node_list[i] );
	}
	*/
	return node_list;
}

int len(int *l){
	int j=0;
	for(int i=0;i<1000;i++){
		if(l[i]!=0){
			j++;
		}
	}
	return j;
}

int check(int i, int j){
	char ii[11] ;
	char jj[11];
	sprintf(ii,"%d",i);
	sprintf(jj,"%d",j);
	if(j%i!=0){
		return 0;
	}
	int tag=0;
	for(int i=0;i<strlen(ii);i++){
		for(int j=0;j<strlen(jj);j++){
			if(ii[i]==jj[j]){
				tag++;
				//printf("i:%c j:%c\n",ii[i],jj[j]);
				//jj[j]= -1;
				ii[i]= -1;
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
	for (int i = 0; i < N; i++){
		printf("%d:",l[i]);
		for (int j = i+1; j < N; j++){
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
	for(int i=0;i<N;i++){
		if(l[i]!=0){
			count++;
		}
	}
	return count;
}

int* clear_path(int *l,int N, int n){
	for(int i=n;i<N;i++){
		l[i]=0; 
	}
	return l;
}
void show_path(int *l,int N){
	for(int i=0; i<N;i++){
		printf("%d\n", l[i]);
	}
}
void show_actual_path(int *p,int *l,int N){
	int k;

	for(int i=0; i<N;i++){
		if(p[i]==1){
			printf("%d", l[i]);
			k = i+1;
			break;
		}
	}
	for(int j=k;j<N;j++){
		if(p[j]==1){
			printf(" < %d", l[j]);
		}
	}
	printf("\n");
}
void append(int n){
	for(int i=0;i<1000;i++){
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
	for(int j=0;j<N;j++){
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
	for(int j=0;j<N;j++){
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

	int NODES = len(L);
	//printf("\n");
	//printf("length:%d\n",NODES );
	//printf("test\n");
	
	
	for (int i = 0; i < NODES-1; i++){
		for (int j = i+1; j < NODES; j++){
			if (check(L[i],L[j])==1){
				t[i][j]=1;
			}
			else{
				t[i][j]=0;
			}
		}
	}
	/*
	for(int i =0;i<NODES;i++){
		for(int j=0;j<NODES;j++){
			printf(" %d",t[i][j]);
		}
		printf("\n");
	}
	*/
	show_Partial_order1(L,NODES);

	//printf("**************************************\n");

	//printf("****************test****************\n");

	int max = 1;
	for(int i=0;i<NODES;i++){
		find_longest_number(max,i,NODES);
	}



	int max_length = max_and_pos(max_l,1000);
	//printf("max_length:%d\n", max_length);


	
	printf("\n");
	printf("Longest monotonically increasing sequences:\n");

	//printf("************ USE MATRIX TO FIND**************\n");
	for(int i=0;i<NODES;i++){
		int p[1000]={0};
		p[i]=1;
		//printf("%d :", i);
		next_node(i,NODES,max_length,p,L);
		//printf("\n");
	}
	//printf("\n");
	
	
}







