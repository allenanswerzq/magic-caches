#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <limits.h>
#include <sys/time.h>
#include <time.h>

#define N 100000000
#define FREQ 2.2

struct elem {
   struct elem *next;
}array[SIZE];

unsigned long usec_diff(struct timeval *a, struct timeval *b)
{
  unsigned long usec;

  usec = (b->tv_sec - a->tv_sec)*1000000;
  usec += b->tv_usec - a->tv_usec;
  return usec;
}

int main(int argc, char** argv) {

  struct timeval start, end;
  double cycles;
  unsigned long usec;
  int64_t dummy = 0;
  char *arg;
  int random_list = 0;

  srandom(time(NULL));

	while ((arg = argv[1]) != NULL) {
		if (*arg != '-')
			break;
		for (;;) {
			switch (*++arg) {
			case 0:
				break;
			case 'r':
				random_list = 1;
				continue;
			default:
				printf("Unknown flag '%s'", arg);
			}
			break;
		}
		argv++;
	}

  for (size_t i = 0; i < SIZE - 1; ++i) 
    array[i].next = &array[i + 1];
  array[SIZE - 1].next = array;

  if (random_list) {
    // Fisher-Yates shuffle the array.
    for (size_t i = 0; i < SIZE - 1; ++i) {
      size_t j = i + rand() % (SIZE - i);
      struct elem temp = array[i]; 
      array[i] = array[j];
      array[j] = temp;
    }
  }
  // Randomly access this array 
  gettimeofday(&start, NULL);
  struct elem *i = array;
  for (size_t n = 0; n < N; ++n) {
    dummy += (int64_t)i;
    i = i->next;
  }
  gettimeofday(&end, NULL);
  usec = usec_diff(&start, &end);

  // Make sure the compiler doesn't compile away offset
	*(volatile unsigned int *)(&dummy);

  cycles = 1000 * (double) usec / N;

  // return cycle time in ns
  printf("|%6.2fns |(~%.1f cycles)\n",
    cycles, cycles*FREQ);
}
