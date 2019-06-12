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

#include "Graph.c"

#define LENGTH 1000

int* advisor(p){
	printf("P is: %d\n",p);
	int *node_list = malloc(sizeof(int)*LENGTH);
	assert(node_list!=NULL);
	/*
	int s_p = sqrt(p)+1;
	printf("s_p: %d\n",s_p);
	for(int i=1;i<s_p;i++){
		if(p%i==0){
			printf("i: %d\n",i);
		}
	}
	*/
	int j=0;
	for(int i=1;i<p;i++){
		if(p%i==0){
			node_list[j]=i;
			j++;
		}
	}
	node_list[j]=p;
	/*
	for(int i=0;i<=j;i++){
		printf(":%d\n",node_list[i]);
	}
	*/
	
	//printf("j:%d\n",j);

	return node_list;


}

int len(int *l){
	int j=0;
	for(int i=0;i<sizeof(l);i++){
		if(l[i]!=0){
			j++;
		}
	}
	return j;
}

bool check(int i, int j){
	char ii[10] ;
	char jj[10];
	sprintf(ii,"%d",i);
	sprintf(jj,"%d",j);
	//printf("!!!:%c\n",ii[0]);
	//printf("???%lu\n",sizeof(ii));
	//printf("???%lu\n",sizeof(jj));
	//printf("???%lu\n",strlen(jj));
	/*
	for(int i=0;i<strlen(ii);i++){
		printf("~~~!%c\n",ii[i] );
	}
	*/
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

void show_Partial_order(Graph g,int *l){
	showGraph(g);
	printf("Partial order:\n");
	for (int i = 0; i < g->nV; i++){
		printf("%d:",l[i]);
		for (int j = i+1; j < g->nV; j++){
			if (g->edges[i][j]){
				printf(" %d",l[j]);
			}
		}
		printf("\n");
	}
}





int visited[LENGTH];


bool dfsPathCheck(Graph g, Vertex v, Vertex dest) {
   Vertex w;
   if (v == dest)
      return true;
   else {
      for (w = 0; w < numOfVertices(g); w++) {
	 if (adjacent(g, v, w) && visited[w] == -1) {
	    visited[w] = v;
	    if (dfsPathCheck(g, w, dest))
	       return true;
	 }
      }
   }
   return false;
}

bool findPathDFS(Graph g, Vertex src, Vertex dest) {
   Vertex v;
   for (v = 0; v < numOfVertices(g); v++)
      visited[v] = -1;
   visited[src] = src;
   return dfsPathCheck(g, src, dest);
}

int max_and_pos(int *arr,int N){
	int i,max;
	max = arr[0];
	for(i = 1;i<N;i++){
		if(max < arr[i]){
			max = arr[i];
		}
	}
	printf("max number:%d\n", max);

	int pos[N];
	int j=0;
	for(i = 0;i<N;i++){
		if(arr[i]==max){
			pos[j] = i;
			j++;
		}
	}

	for(i=0;i<j;i++){
		printf("position:%d\n", pos[i]);
	}
	return max;
}

void find_longest_path(Graph g,int *l,int N){
	//int src = 0;
	int dest = N-1;
	int node_list[N][N];
	int node_len[N];

	printf("%d\n", dest);
	for(int src=0;src<N;src++){
		int i=0;
		int k=0;
		if (findPathDFS(g, src, dest)) {
			Vertex v = dest;
			while (v != src && l[src]<=l[v] && check(l[src],l[v])) {
				printf("%d - ", l[v]);
				node_list[src][i]=l[v];
				i++;
				k++;
				v = visited[v];
			}
			printf("%d\n", l[src]);
			printf("k: %d\n", k);
			node_len[src]=k;
			node_list[src][i+1]=l[src];
   		} 
	}
	/*
	for(int i=0;i<N;i++){
		for(int j=0;j<N;j++){
			printf(" %d",node_list[i][j]);
		}
		printf("\n");
	}
	
	for(int i=0;i<N;i++){
		printf("??%d\n", node_len[i]);
	}
	*/
	int max= max_and_pos(node_len,N);
	printf("max:%d \n",max);


	/*
	if (findPathDFS(g, src, dest)) {
		Vertex v = dest;
		while (v != src) {
			printf("%d - ", l[v]);
			v = visited[v];
		}
		printf("%d\n", l[src]);
   }
   */
   
}



int main(int argc, char *argv[]) {
	printf("Input Number: %s\n",argv[1]);
	int p = atoi(argv[1]);
	int* L = advisor(p);

	int NODES = len(L);
	printf("length:%d\n",NODES );

	/*
	for(int i=0;i<sizeof(L);i++){
		printf(":%d\n",L[i]);
	}
	*/


	//int a = check(4995,94812);
	//printf("a:%d\n", a);


	Graph g = newGraph(NODES);
	Edge e;

	for(int i=0;i<NODES-1;i++){
		for(int j=i+1;j<NODES;j++){
			if(check(L[i],L[j])){
				//printf("i:%d, j:%d \n",L[i],L[j]);
				e.v = i;
				e.w = j;
				//printf("%d\n", __LINE__);
				insertEdge(g,e);
			}

		}
	}
	show_Partial_order(g,L);
	find_longest_path(g,L,NODES);




}


