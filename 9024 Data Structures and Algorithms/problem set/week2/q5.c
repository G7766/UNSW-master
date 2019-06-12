#include<stdio.h>
#include<stdlib.h>
#define LEN(x) (sizeof(x)/sizeof(x[0]))
#define MAX 10

typedef struct
{
	int day, month, year;
} DateT;

typedef struct 
{
	int hour, minute;
} TimeT;

typedef struct 
{
	int transaction;
	char weekday[4];
	char weekends[2];
	DateT date;
	TimeT time;
	char mode; //'B' 'F' or 'T'
	char from[32], to[32];
	int journey;
	char faretext[12];
	float fare, discount, amount;
}JourneyT;

//Memory requirement for one element of type JourneyT: 
//4 + 4 + 12 + 8 + 1 (+ 3 padding) + 2·32 + 4 + 12 + 3·4 = 124 bytes.

/*
The data structure can be improved in various ways: 
encode both origin and destination (from and to) using Sydney 
Transport's unique stop IDs along with a lookup table that 
links e.g. 203311 to "Anzac Pde Stand D at UNSW"; use a single 
integer to encode the possible "Fare Applied" entries; 
avoid storing redundant information like the weekday, 
which can be derived from the date itself.
*/







