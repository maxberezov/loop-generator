#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int **B = create_two_dim_int(512, 512, "zeros");
	int *A = create_one_dim_int(262144, "zeros");
    clock_t start = clock();

	for (int b = 1; b < 512; b++)
	  for (int a = 5; a < 512; a++)
	  {
	    
	     A[a]=A[a-3]+46;
	    
	     B[a][b]=B[a-5][b-1]*41;
	    
	     A[a]=A[a+3]-B[a][b];
	    
	     int var_a=A[a]-38;
	     int var_b=A[a-5]-24;
	  }

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_2d_array(B, 512, 512);
	deallocate_1d_array(A);
    return 0; 
    }