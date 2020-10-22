#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *A = create_one_dim_int(262144, "zeros");
	int *B = create_one_dim_int(262144, "zeros");
	int **C = create_two_dim_int(256, 512, "zeros");
    clock_t start = clock();

	for (int a = 1; a < 262140; a++)
	{
	  
	    B[a]=B[a-1]-34;
	  
	    A[a]=A[a+4]-B[a];
	}

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_1d_array(A);
	deallocate_1d_array(B);
	deallocate_2d_array(C, 256, 512);
    return 0; 
    }