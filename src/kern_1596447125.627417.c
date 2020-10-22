#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int **B = create_two_dim_int(128, 512, "ones");
	int *A = create_one_dim_int(524288, "ones");
	int *C = create_one_dim_int(131072, "ones");
    clock_t start = clock();

	for (int a = 0; a < 131069; a++)
	{
	  
	    C[a]=C[a+3]*32;
	  
	    A[a]=C[a];
	    A[a+5]=34;
	}

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_2d_array(B, 128, 512);
	deallocate_1d_array(A);
	deallocate_1d_array(C);
    return 0; 
    }