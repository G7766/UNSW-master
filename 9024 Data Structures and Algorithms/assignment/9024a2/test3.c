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
int t[1000][1000];
//int L[1000];

int visited[LENGTH];
int max_length = 0;
int indx = 0;

int* advisor(p){
	//printf("P is: %d\n",p);
	int *node_list = malloc(sizeof(int)*LENGTH);
	assert(node_list!=NULL);

	int j=0;
	for(int i=1;i<p;i++){
		if(p%i==0){
			node_list[j]=i;
			j++;
		}
	}
	node_list[j]=p;
	/*
	for(int i =0;i<j;i++){
		printf("%d,",node_list[i] );
	}*/
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

bool check(int i, int j){
	char ii[10] ;
	char jj[10];
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





bool dfsPathCheck(Graph g, Vertex v, Vertex dest) {
   Vertex w;
	for (w = 0; w < numOfVertices(g); w++){
		if (adjacent(g, v, w) && visited[w] == -1) {
			visited[w] = v;
			if (w==dest)
				return true;
			if (dfsPathCheck(g, w, dest))
				return true;
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
	return max;
}
/*
void find_longest_path(Graph g,int *l,int N){
	//int src = 0;
	int dest = N-1;

	printf("%d\n", dest);
	for(int src=0;src<N;src++){
		int i=0;
		int k=0;
		if (findPathDFS(g, src, dest)) {
			Vertex v = dest;
			while (v != src) {
				printf("%d <- ", l[v]);
				v = visited[v];
			}
			printf("%d\n", l[src]);
   		} 
	}
}
*/
int find_max_path(Graph g,int *l,int N){
	int max_list[N-1];
	int dest = N-1;
	for(int src = 0;src<N-1;src++){
		int i=0;
		if (findPathDFS(g, src, dest)) {
			Vertex v = dest;
			while (v != src) {
				//printf("%d <- ", l[v]);
				v = visited[v];
				//printf("vvvvvvvv:%d\n", v );
				i++;
			}
			//printf("??\n");
			//printf("%d\n", l[src]);
			i++;
   		}
   		max_list[src]=i;
   		//printf("mmmmm:%d\n",i);

	}
	int max = max_and_pos(max_list,N-1);
	//printf("mmmmm:%d\n",max);
	return max;

}
/*
void path_h(Graph g,int *l,int N,int src,int dest){
	for(int i=0;i<N;i++){
		visited[i]=false
	}
	return path_r(g,src,dest,N-1);

}
void path_r(Graph g,int v,int dest,int N){
	if(v==dest){
		if(d==0){
			return 1;
		}
		return 0;
	}
	else{
		visited[v]=1;
		for
	}
}
*/
/*
void show_matrix(Graph g, int *l,int N){
	int t[N][N];
	for (int i = 0; i < N; i++){
		for (int j = 0; j < N; j++){
			if (g->edges[i][j]){
				t[i][j]=1;
			}
			else{
				t[i][j]=0;
			}
		}
	}
	for(int i =0;i<N;i++){
		for(int j=0;j<N;j++){
			printf(" %d",t[i][j]);
		}
		printf("\n");
	}
}
*/

void dfs_find_all_path(int src,int N){
	int stack[1000];
	stack[0]=1;
	int m=1;
	for(int i=0;i<N;i++){
		if(t[src][i]==1){
			if(i == N-1){
				printf(" >%d",i);
				if(src==N-1){
					return;
				}
				else{
					return dfs_find_all_path(src+1,N);
				}
			}
			else{
				src = i;
				printf(" %d >",src);
				return dfs_find_all_path(src,N);
			}
		}
		printf("!!\n");
	}
}


void all_path(Graph g, int src,int N,int count){
	if(src==N-1){
		printf("gg\n");
		return;
	}
	for(int v=src;v<N-1;v++){
		//int stack[0]=v;
		printf(" %d",v);
		for(int w=v+1;w<N;w++){
			if(g->edges[v][w]){
				count++;
				printf("-%d",w );
				all_path(g,w,N,count);
			}
		}
		if(count==3){
			printf("!!!!\n");
		}
	}
	printf("\n");
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
	//printf("Input Number: %s\n",argv[1]);
	int p = atoi(argv[1]);
	int* L = advisor(p);
	//int *L = node_list;
	//advisor(p);
	int NODES = len(L);
	//printf("\n");
	//printf("length:%d\n",NODES );

	Graph g = newGraph(NODES);
	Edge e;

	for(int i=0;i<NODES-1;i++){
		for(int j=i+1;j<NODES;j++){
			printf("i:%d j: %d\n",L[i],L[j]);
			if(check(L[i],L[j])){
				//printf("i:%d, j:%d \n",L[i],L[j]);
				e.v = i;
				e.w = j;
				//printf("%d\n", __LINE__);
				insertEdge(g,e);
				//printf("~~~~~~~~");
				
			}
		}
	}
	//printf("!!!!!!\n");
	show_Partial_order(g,L);
	int tc[NODES*(NODES-1)][NODES];
	max_length = find_max_path(g,L,NODES);
	//printf("max_length :%d\n", max_length);

	/*
	
	show_matrix(g, L,NODES);
	// show matrix
	
	//int t[NODES][NODES];
	*/

	//printf("********** Matrix *************\n");
	//int matrix[NODES][NODES];
	for (int i = 0; i < NODES; i++){
		for (int j = 0; j < NODES; j++){
			if (g->edges[i][j]){
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
	}*/

	//printf("**************************\n");

	//find_longest_path(g,L,NODES);
	//printf("**************************\n");
	/*
	int node_L[NODES*(NODES-1)][NODES];
	int length[1000*1000]={0};
	int count = 0;
	int ka =0 ,kb=0;

	for(int src=0; src<NODES-1;src++){
		for(int dest=NODES-1;dest>src;dest--){
			if(findPathDFS(g,src, dest)){
				Vertex v = dest;
				while(v != src){
					node_L[ka][kb]=v;
					count++;
					kb++;
					printf("%d <", v);
					v = visited[v];
				}
				//printf("%d\n", src);
				node_L[ka][kb]=src;
				length[ka]=count+1;
			}
			count=0;
			ka++;
			kb=0;
		}
	}
	*/

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







