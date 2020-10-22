#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *A = create_one_dim_int(65536, "random");
	int *B = create_one_dim_int(524288, "random");
    clock_t start = clock();

	for (int a = 5; a < 65536; a++)
	{
	  
	    A[a]=B[a];
	    A[a-4]=B[a];
	  
	    int var_a=B[a]*49;
	    int var_b=B[a-5]+2;
	}

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_1d_array(A);
	deallocate_1d_array(B);
    return 0; 
    }