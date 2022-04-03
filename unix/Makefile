CC = gcc
CFLAGS = -Wall -g -pedantic
LDFLAGS = -pthread -lm

all: generator poslužitelj

generator: generator.c
		gcc $(CFLAGS) $(LDFLAGS) -o generator generator.c

poslužitelj: poslužitelj.c
		gcc $(CFLAGS) $(LDFLAGS) -o poslužitelj poslužitelj.c


clean:
		-rm -f generator poslužitelj *.o *.core

