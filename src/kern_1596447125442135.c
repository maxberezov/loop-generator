#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int ***A = create_three_dim_int(32, 16, 64, "random");
    clock_t start = clock();

	for (int a = 0; a < 28; a++)
	{
	  
	    A[a][a][a]=A[a+1][a+2][a+4]*40;
	}

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_3d_array(A, 32, 16, 64);
    return 0; 
    }