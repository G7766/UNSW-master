/**
     main.c

     Program supplied as a starting point for
     Assignment 1: Transport card manager

     COMP9024 18s2
**/
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <ctype.h>

#include "cardRecord.h"
#include "cardLL.h"

void printHelp();
void CardLinkedListProcessing();

int main(int argc, char *argv[]) {
   if (argc == 2) {
      int cardID,i;
      float cardAmount;
      
      int n = atoi(argv[1]);
      //printf("here is n :%d\n",n);
      //allocate n  memory
      cardRecordT *cardRecird = malloc(n*sizeof(cardRecordT));
      assert(cardRecird!=NULL);
      // 
      for(i=0;i<n;i++){
         cardID = readValidID();
         cardAmount = readValidAmount();

         cardRecird[i].cardID = cardID;
         cardRecird[i].balance = cardAmount;
      }
      //print
      float total=0.0,avg;
      for(i = 0;i<n;i++){
         printCardData(cardRecird[i]);
         total += cardRecird[i].balance;
      }
      //n=n+1;
      avg = total/n;
      printf("Number of cards on file: %d\n",n);
      printf("Average balance: $%.2f\n", avg);

      free(cardRecird);
      /*** Insert your code for stage 1 here ***/
      
   } else {
      CardLinkedListProcessing();
   }
   return 0;
}

/* Code for Stages 2 and 3 starts here */

void CardLinkedListProcessing() {
   int op, ch;
   int cardID;
   float cardAmount;
   int n;
   float balance;

   List list = newLL();   // create a new linked list
   
   while (1) {
      printf("Enter command (a,g,p,q,r, h for Help)> ");

      do {
	 ch = getchar();
      } while (!isalpha(ch) && ch != '\n');  // isalpha() defined in ctype.h
      op = ch;
      // skip the rest of the line until newline is encountered
      while (ch != '\n') {
	 ch = getchar();
      }

      switch (op) {

         case 'a':
         case 'A':
            cardID = readValidID();
            cardAmount = readValidAmount();
            insertLL(list,cardID,cardAmount);
            /*** Insert your code for adding a card record ***/

	    break;

         case 'g':
         case 'G':

            getAverageLL(list,&n,&balance);
            /*
            printf("Number of cards on file: %d\n", n);
            if (balance>=0){
               printf("Average balance: $%.2f\n", balance);
            }
            else{
               float z;
               z = balance * (-1);
               printf("Average balance: -$%.2f\n", z);
            }
            */
            /*** Insert your code for getting average balance ***/

	    break;
	    
         case 'h':
         case 'H':
            printHelp();
	    break;
	    
         case 'p':
         case 'P':
            showLL(list);

	    break;

         case 'r':
         case 'R':
            cardID = readValidID();
            removeLL(list,cardID);
            /*** Insert your code for removing a card record ***/

	    break;

	 case 'q':
         case 'Q':
            dropLL(list);       // destroy linked list before returning
	    printf("Bye.\n");
	    return;
      }
   }
}

void printHelp() {
   printf("\n");
   printf(" a - Add card record\n" );
   printf(" g - Get average balance\n" );
   printf(" h - Help\n");
   printf(" p - Print all records\n" );
   printf(" r - Remove card\n");
   printf(" q - Quit\n");
   printf("\n");
}
