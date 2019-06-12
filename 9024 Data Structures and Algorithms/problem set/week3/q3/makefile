binary : binary.o IntStack.o
		gcc -o binary binary.o IntStack.o

binary.o : binary.c IntStack.h
		gcc -Wall -Werror -std=cll -c binary.c

IntStack.o : IntStack.c IntStack.h
		gcc -Wall -Werror -std=cll -c IntStack.c