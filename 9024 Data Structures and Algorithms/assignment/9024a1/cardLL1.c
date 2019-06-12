// Linked list of transport card records implementation ... Assignment 1 COMP9024 18s2
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "cardLL.h"
#include "cardRecord.h"

// linked list node type
// DO NOT CHANGE
typedef struct node {
    cardRecordT data;
    struct node *next;
} NodeT;

// linked list type
typedef struct ListRep {
   NodeT *head;

/* Add more fields if you wish */

} ListRep;

/*** Your code for stages 2 & 3 starts here ***/

// Time complexity: O(1)
// Explanation: there is no loop in function and there is no iteration, so the time complexity is O(1);
List newLL() {
	List list = malloc(sizeof(ListRep));
	assert(list!=NULL);
	list->head=NULL;
   return list;  /* needs to be replaced */
}

// Time complexity: O(n)
// Explanation: There is one loop in function, so the time complexity is O(n);
void dropLL(List listp) {
	NodeT *current = listp->head;
	while(current!=NULL){
		NodeT *p = current->next;
		free(current);
		current = p;
	}

   return;  /* needs to be replaced */
}

// Time complexity: O(n)
// Explanation:  there are many if statements and one while loop in function, so the time comlexity is O(1)+O(n) = O(n)
void removeLL(List listp, int cardID) {
	NodeT *p;
	p=listp->head;
	if (p==NULL){
		printf("Card removed.\n");
		return;
	}
	else{
		NodeT *q,*s;
		if (p->data.cardID == cardID){
			listp->head = p->next;
			free(p);
			printf("Card removed.\n");
			return;
		}
		else{
			q=listp->head->next;
			while(q){
				if (q->data.cardID == cardID){
					p->next=q->next;
					s=q;
					q=q->next;
					free(s); 
					printf("Card removed.\n");
					return;
				}
				else{
					p=p->next;
					q=q->next;
				}
			}
			printf("Card not found.\n" );
			return;
		}
	}
}

// Time complexity: O(n)
// Explanation: there are many if statements and while loops in function, but there are no any loop in loop in function so the time comlexity is O(1)+O(n) = O(n)
void insertLL(List listp, int cardID, float amount) {
	NodeT *new=malloc(sizeof(NodeT));
	assert(new!=NULL);
	//NodeT *current = malloc(sizeof(NodeT));


	new->data.cardID = cardID;
	new->data.balance = amount;

	/*
	if (listp->head == NULL){
		new->next = listp->head;
        listp->head = new;
        printf("Student record added.\n");
	}else{
		NodeT *current = malloc(sizeof(NodeT));
		current = listp->head;
		new->next = current->next;
		current->next = new;
		printf("Card record added.\n");
	}
	*/
	//printf("pass1\n");
	
	NodeT *current;
	current = listp->head;
	//check if is existed
	while(current!=NULL){
		if(current->data.cardID == cardID){
			current->data.balance=current->data.balance + amount;
			//printf("Card record updated.\n");
			printCardData(current->data);
			free(new);
			return;
		}
		else{
			current = current->next;
		}
	}

	//printf("pass2\n");

	//ascending order
	// if head is null  or  head ID value is larger than new ID
	// add on the top
	//else iterate to find the  less than new
	//NodeT *curr = malloc(sizeof(NodeT));
	
	if(listp->head == NULL || listp->head->data.cardID > new->data.cardID){					// empty list /. start
		new->next = listp->head;
		listp->head = new;
		//printf("kkkkkk\n");
	}
	else{
		//printf("33333\n");
		NodeT *curr = malloc(sizeof(NodeT));
		//printf("4444\n");
		curr = listp->head;
		//printf("2222\n");
		while(curr->next!=NULL && new->data.cardID > curr->next->data.cardID){
			curr = curr->next;
		}
		new->next = curr->next;
		curr->next = new;
		//free(curr);
	}
	printf("Card added.\n");
	return;  /* needs to be replaced */
}

// Time complexity: O(n)
// Explanation: there is a while loop in function, 
//				so it will systematically iterate through Linked List from start to end so time complexity is O(n).
void getAverageLL(List listp, int *n, float *balance) {
	int i=0;
	float total=0.0;

	NodeT *p;
	p = listp->head;
	while(p!=NULL){
		i +=1;
		total += p->data.balance;
		p = p->next; 
	}
	*n = i;
	*balance = total/i;

	//print	
	printf("Number of cards on file: %d\n", *n);
    if (balance>=0){
       printf("Average balance: $%.2f\n", *balance);
    }
    else{
       float z;
       z = *balance * (-1);
       printf("Average balance: -$%.2f\n", z);
    }

	return;  /* needs to be replaced */
}

// Time complexity: O(n)
// Explanation: there is a for loop in function, 
//				so it will systematically iterate through Linked List from start to end so time complexity is O(n).
void showLL(List listp) {
	NodeT *current;
	//current = listp->head;
	for(current = listp->head;current!=NULL;current = current->next){
		printCardData(current->data);
	}
   return;  /* needs to be replaced */
}
