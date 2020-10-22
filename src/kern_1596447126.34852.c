#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *B = create_one_dim_int(131072, "ones");
	int **A = create_two_dim_int(512, 256, "ones");
    clock_t start = clock();

	for (int a = 0; a < 131071; a++)
	{
	  
	    int var_a=B[a]+31;
	    int var_b=B[a+1]*38;
	}

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_1d_array(B);
	deallocate_2d_array(A, 512, 256);
    return 0; 
    }