#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <memory.h>
#include <time.h>
#include <err.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/shm.h>
#include <pthread.h>

#define MQ_MAX_SIZE 2048
#define SHM_MAX_SIZE 10
#define SHM_INIT_KEY 7788
#define SHM_MUTEX_KEY 7889
#define SHM_MESS_KEY 8000

struct msg_buff {
	int id;
	int timer;
	key_t msg_key;
};


void printHelp()
{
	printf("\nHelp:\n\n");
	printf("./generator BROJ_POSLOVA BROJ_JEDINICA_VREMENA");
}


int main(int argc, char *argv[]) {
	int i, j, nJobs, maxJobTime, msg_ret;

	struct msg_buff msg_tmp;

	key_t msg_key;
	int msgid;


	int shmid;
	int new_shmid = 0;
	key_t key = SHM_INIT_KEY;
	int *shm;

	int last_job_key_id;
	int new_last_job_id = 0;
	key_t key_l_job = SHM_MESS_KEY;
	int *last_job_key;

	int mutex_id;
	key_t mutex_key = SHM_MUTEX_KEY;
	pthread_mutex_t *my_mutex;

	int job_id;
	int *job_list;


	if(argc != 3) {
		printHelp();
		err(1, "\n\nWrong input args (exit code 1)");
	}

	nJobs = atoi(argv[1]);
	maxJobTime = atoi(argv[2]);

	/* init */
	srand(time(NULL));
	msg_key = ftok("text.txt", 65);
	msgid = msgget(msg_key, 0666 | IPC_CREAT);


	/* last number */
	shmid = shmget(key, SHM_MAX_SIZE, 0666);
	if( shmid < 0 ) {
		new_shmid = 1;
		shmid = shmget(key, SHM_MAX_SIZE, IPC_CREAT | 0666);
		if( shmid < 0 ) {
			err(2, "\n\nShared mem (exit code 2)");
		}
	}

	shm = shmat(shmid, NULL, 0);
	if( shm == (int *)(-1) ) {
			err(3, "\n\nShared mem attach (exit code 3)");
	}


	/* Mutex */
	mutex_id = shmget(mutex_key, 50, 0666);
	if( mutex_id < 0 ) {
		mutex_id = shmget(mutex_key, 50, IPC_CREAT | 0666);
		if( mutex_id < 0 ) {
			err(4, "\n\nShared mem mutex (exit code 4)");
		}
	}

	my_mutex = shmat(mutex_id, NULL, 0);
	if( my_mutex == (pthread_mutex_t *)(-1) ) {
			err(5, "\n\nShared mem attach mutex (exit code 5)");
	}
	pthread_mutex_init(my_mutex, NULL);


	if(new_shmid) {
		pthread_mutex_lock(my_mutex);
		*shm = 0;
		pthread_mutex_unlock(my_mutex);
	}
	printf("\nGenerator: Krecem sa %d porukom\n\n", *shm);

	

	/* read last job key */
	last_job_key_id = shmget(key_l_job, SHM_MAX_SIZE, 0666);
	if( last_job_key_id < 0 ) {
		new_last_job_id = 1;
		last_job_key_id = shmget(key_l_job, SHM_MAX_SIZE, IPC_CREAT | 0666);
		if( last_job_key_id < 0 ) {
			err(6, "\n\nShared mem last job mem (exit code 6)");
		}
	}
	last_job_key = shmat(last_job_key_id, NULL, 0);
	if( last_job_key == (int *)(-1) ) {
			err(6, "\n\nShared mem attach last job mem (exit code 7)");
	}
	if(new_last_job_id) {
		pthread_mutex_lock(my_mutex);
		*last_job_key = SHM_MESS_KEY + 20;
		pthread_mutex_unlock(my_mutex);
	}
	printf("\nGenerator: last_job_key = %d\n\n", *last_job_key);



	for(i=0; i<nJobs; i++) {
		pthread_mutex_lock(my_mutex);
		msg_tmp.id = *shm;
		*shm = msg_tmp.id + 1;

		msg_tmp.timer = rand() % maxJobTime + 1;

		msg_tmp.msg_key = *last_job_key;
		*last_job_key = *last_job_key + msg_tmp.timer*sizeof(int);
		pthread_mutex_unlock(my_mutex);
		
		job_id = shmget(msg_tmp.msg_key, msg_tmp.timer*sizeof(int), IPC_CREAT | 0666);
		if(job_id < 0) {
			printf("\nError in job_id = shmget(. . .)\n");
		}
		job_list = shmat(job_id, NULL, 0);

		printf("Generator: Poruka: id=%d timer=%d msg_key=%d\nPosao:",
											msg_tmp.id, msg_tmp.timer, msg_tmp.msg_key);
		
		for(j=0; j<msg_tmp.timer; j++) {
			job_list[j] = rand() % 900 + 100;
			printf(" %d", job_list[j]);
		}
		printf("\n\n");
		shmdt(job_list);

		msg_ret = msgsnd(msgid, &msg_tmp, sizeof(msg_tmp), IPC_NOWAIT);
		if(msg_ret<0) {
			printf("\n\nGreska u slanju poruke\n");
			exit(1);
		}
	}

	return 0;
}


