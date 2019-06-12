/**
     main.c

     Program supplied as a starting point for
     Assignment 1: Transport card manager

     COMP9024 18s2
**/
#include <stdio.h>
#include <stdlib.h>

//??????????????????????????????????????????


int main(int argc, char *argv[]) {
   if (argc == 2) {

      /*** Insert your code for stage 1 here ***/
      // dynamic array 
      int i=0;
      int *arr1;
      float *arr2;
      int a1;
      float amount;
      int amount_size;
      int tag1=0;
      while (i<argc){
         if (tag1==0){
            //printf("-----------------\n");
            printf("Enter card ID: ");
         }
         if (tag1==1){
            printf("Not valid. Enter a valid value: ");
         }
         //printf("i :%d\n", i);
         int a,m,ii=0,mm=0;
         scanf("%d",&a);
         // check input number n is 8-digit
         int n = a;
         int *numberID;
         numberID = (int*)malloc(sizeof(int)*m);
         while (n!=0){
            int z;
            z = n % 10;
            //printf("%d\n",z);
            numberID[ii]=z;
            ii++;
            n = n/10;
         }
         //printf("here is ii :%d\n",ii);
         int first_element = numberID[ii-1];

         // array of n   numberID = {1,2,3,4,5,6,7,8,\n}

         if (ii!=8){
            tag1=1;;
            continue;
         }
         else if (first_element == 0 ){
            tag1=1;
            continue;
         }

         else{
            tag1=0;
            int tag2=0;
            arr1 = (int*)malloc(sizeof(int)*a1);
            arr1[i] = a;
            printf("Enter amount: ");
            while (tag2==0){
               //float amount;
               scanf("%f", &amount);
               if (amount>=-2.35 && amount<=250){
                  tag2 = 1;
                  arr2 = (float*)malloc(sizeof(float)*amount_size);
                  mm++;
                 // printf("-----------------\n");
               }
               else{
                  printf("Not valid. Enter a valid value: ");
                  continue;
               }
            }
         }
         i = i+1;
      }
      //printf("-----------------\n");
      
      //printf all record
      for(int i=0; i<ii;i++){
         printf("-----------------\n");
         printf("Card ID: %d\n",arr1[i]);
      }
      //print some statistical information
      
   } 
   else {
      int q=1;
      printf("????");
   }
   return 0;
}