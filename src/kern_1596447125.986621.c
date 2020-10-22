#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *A = create_one_dim_int(131072, "zeros");
	int *B = create_one_dim_int(262144, "zeros");
    clock_t start = clock();

	for (int c = 3; c < 131071; c++)
	  for (int b = 3; b < 131071; b++)
	    for (int a = 3; a < 131071; a++)
	    {
	      
	      A[a]=A[a-3]*B[a];
	      
	      B[a]=B[a+3]+50;
	      
	      int var_a=A[a]-47;
	      int var_b=A[a+1]+2;
	    }

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_1d_array(A);
	deallocate_1d_array(B);
    return 0; 
    }