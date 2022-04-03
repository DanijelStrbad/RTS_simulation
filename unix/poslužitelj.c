#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <memory.h>
#include <sys/signal.h>
#include <signal.h>
#include <time.h>
#include <err.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <pthread.h>

#define MQ_MAX_SIZE 2048
#define MAX_DRETVI 20


struct msg_buff {
	int id;
	int timer;
	key_t msg_key;
};

struct msg_atom {
	int id;
	int timer;
	key_t msg_key;
	struct msg_atom *next;
};


/* Global */
pthread_mutex_t M;
pthread_cond_t red = PTHREAD_COND_INITIALIZER;
pthread_t thr_id[MAX_DRETVI];
int broj_poslova, thr_int[MAX_DRETVI];
int nThr, ugasi_program = 0;
struct msg_atom *lista_poslova = NULL;


void print_poslove() {
	struct msg_atom *tmp;
	tmp = lista_poslova;
	printf("\nPoslužitelj: Lista %d poslova:\n", broj_poslova);
	while (tmp) {
		printf("id=%d timer=%d msg_key=%d\n", (*tmp).id, (*tmp).timer, (*tmp).msg_key);
		tmp = (*tmp).next;
	}
	printf("\n");
}

void prekidna_rutina() {
	int i;
	pthread_mutex_lock(&M);
	ugasi_program = 1;
	pthread_mutex_unlock(&M);
	for(i=0; i<nThr; i++) {
		//pthread_cond_broadcast(&red);
		//pthread_join(thr_id[i], NULL);
		pthread_cancel(thr_id[i]);
		printf("\nPoslužitelj: Gasim %d dretvu\n", i+1);
	}
	printf("\n\nPoslužitelj: gotov sam sa radom\n\n");
	exit(0);
}

void printHelp()
{
	printf("\nHelp:\n\n");
	printf("./poslužitelj BROJ_DRETVI MIN_VRIJEME_ZA_AKTIVIRANJE_DRETVI");
}


void *radna_dretva(void *dretva_id) {
	int shmid, my_id = *((int *)dretva_id);
	int *shm;
	struct msg_atom *my_atom;
	int i, j = 0;
	//time_t start_t, end_t;
	struct timespec start, stop;

	while(1) {
		pthread_mutex_lock(&M);

		while(broj_poslova == 0) {
			printf("\nDretva %d ceka na red, broj_poslova = %d\n", my_id, broj_poslova);
			pthread_cond_wait(&red, &M);
			//printf("\nDretva %d se probudila, ugasi_program = %d\n", my_id, ugasi_program);
			if(ugasi_program) {
				pthread_exit(NULL);
			}
		}

		my_atom = lista_poslova;
		lista_poslova = (*my_atom).next;
		broj_poslova--;

		pthread_mutex_unlock(&M);

		/* citaj posao */
		shmid = shmget((*my_atom).msg_key, ((*my_atom).timer)*sizeof(int), 0666);
		if( shmid < 0 ) {
			err(10, "\n\nShared mem thread (exit code 10)");
		}
		shm = shmat(shmid, NULL, 0);
		if( shm == (int *)(-1) ) {
			err(11, "\n\nShared mem attach thread (exit code 11)");
		}
		
		/* working . . . */
		for(i=0; i<(*my_atom).timer; i++) {
			/* sleep(10); */

			asm volatile ("":::"memory");
			//time(&start_t);
			clock_gettime(CLOCK_THREAD_CPUTIME_ID, &start);
			//time(&end_t);
			clock_gettime(CLOCK_THREAD_CPUTIME_ID, &stop);
			asm volatile ("":::"memory");
			//while( difftime(end_t, start_t) < 10/(*my_atom).timer ) {
			while( (float)
				((stop.tv_sec-start.tv_sec)*1e6 + (stop.tv_nsec-start.tv_nsec)/1e3)
						< ((float)10/(float)(*my_atom).timer)*1e6 ) {
				asm volatile ("":::"memory");
				j = (j + 1)%2048;
				// time(&end_t);
				clock_gettime(CLOCK_THREAD_CPUTIME_ID, &stop);
			}
			// printf("\nDretva %d, time = %f\n", my_id, difftime(end_t, start_t));
			j++;

			printf("\nDretva %d, zad %d, obavljeno %d/%d (%f), data %d",
					my_id, (*my_atom).id, i+1, (*my_atom).timer,
				(float)
				((stop.tv_sec-start.tv_sec)*1e6 + (stop.tv_nsec-start.tv_nsec)/1e3)/1e6,
					shm[i]);
		}
		j++;
		printf("\n");
		
		shmdt(shm);
		free(my_atom);
	}
	//return;
}


int main(int argc, char *argv[]) {
	int minJobTime, msg_ret, i, my_tmp;
	int brojac_spavanja;
	struct msg_buff msg_tmp;
	struct msg_atom *atom_tmp;

	key_t msg_key;
	int msgid;


	if(argc != 3) {
		printHelp();
		exit(1);
	}

	nThr = atoi(argv[1]);
	minJobTime = atoi(argv[2]);
	if( nThr > MAX_DRETVI ) {
		printf("\nPreviše dretvi\n");
		exit(2);
	}


	/* init */
	broj_poslova = 0;
	brojac_spavanja = 0;
	pthread_mutex_init(&M, NULL);

	sigset(SIGINT, prekidna_rutina);
	sigset(SIGTERM, prekidna_rutina);

	msg_key = ftok("text.txt", 65);
	// msgid = msgget(msg_key, 0666 | IPC_CREAT);
	msgid = msgget(msg_key, 0666 | IPC_CREAT);
	if(msgid<0) {
		printf("\nError\n");
		exit(3);
	}

	/* stvori dretve */
	for(i=0; i<nThr; i++) {
		thr_int[i] = i;
		my_tmp = pthread_create(&thr_id[i], NULL, radna_dretva, &thr_int[i]);
		if(my_tmp != 0) {
			err(4, "\n\npthread_create (exit code 4)");
		}
	}

	/* zaprimaj poslove */
	while(1) {
		msg_tmp.id = -123;
		msg_ret = msgrcv(msgid, &msg_tmp, sizeof(msg_tmp), 0, 0 | IPC_NOWAIT);
		// printf("\nmsg_ret=%d\n", msg_ret);

		if( msg_ret == -1 ) {
			/* nema nove poruke */
			sleep(5);
			brojac_spavanja++;

			if(brojac_spavanja >= 4) {
				/* cekao sam 20 [s] */
				brojac_spavanja = 0;

				if(broj_poslova > 0) {
					/* obavi poslove */
					printf("\nPoslužitelj: spavao sam 20 sekundi, obavljam %d zadataka\n",
											broj_poslova);
					/* Pokreni dretve */
					pthread_cond_broadcast(&red);
				} else {
					printf("\nPoslužitelj: spavao sam 20 sekundi, nemam zadataka (%d)\n",
											broj_poslova);
				}
			}


		} else {
			/* dosla poruka */
			brojac_spavanja = 0;

			pthread_mutex_lock(&M);

			broj_poslova++;
			atom_tmp = (struct msg_atom *) malloc(sizeof(struct msg_atom));
			(*atom_tmp).id = msg_tmp.id;
			(*atom_tmp).timer = msg_tmp.timer;
			(*atom_tmp).msg_key = msg_tmp.msg_key;
			(*atom_tmp).next = lista_poslova;
			lista_poslova = atom_tmp;

			print_poslove();

			pthread_mutex_unlock(&M);
		}

		if( broj_poslova >= minJobTime ) {
			/* pokreni dretve */
			brojac_spavanja = 0;
			pthread_cond_broadcast(&red);
		}
		
	}


	return 0;
}


