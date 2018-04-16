SHELL := /bin/bash
Q := @

all: cache-line test-tlb access-time

access-time:
	# Each pointer has a size 8 bytes
	# 1KB to 128MB workset 
	$(Q)for i in $(shell seq 7 24); \
	do echo "$$i:"; \
	gcc -g -O access-times.c -o access -lm -DSIZE=$$((2**i)); \
	printf "%3d" $$i >> random.out; \
	printf "%3d" $$i >> seq.out; \
	./access -r | tee -a random.out; \
	./access | tee -a seq.out; \
	done

cache-line:
	$(Q)for i in 1 2 4 8 16 32 64 128 256 512 1024; \
	do echo "$$i:"; \
	gcc -g -Wall -O line-size.c -o line -lm -DSTEP=$$i; \
	./line $$((2**i)) 64 | tee -a cache-line.out; \
	done


test-tlb:
	gcc -g -Wall -O test-tlb.c -o tlb -lm
	$(Q)for i in $(shell seq 10 28); \
	do echo "$$i:"; \
	printf "%3d" $$i >> tlb-random.out; \
	printf "%3d" $$i >> tlb-seq.out; \
	./tlb $$((2**i)) 64 | tee -a tlb-random.out; \
	./tlb -r $$((2**i)) 64 | tee -a tlb-seq.out; \
	done

clean:
	rm -rf tlb-random.out tlb-seq.out cache-line.out random.out seq.out \
	access line tlb