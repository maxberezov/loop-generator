#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *A = create_one_dim_int(131072, "ones");
	int ***C = create_three_dim_int(64, 16, 16, "ones");
	int **B = create_two_dim_int(256, 128, "ones");
    clock_t start = clock();

	for (int c = 0; c < 131068; c++)
	  for (int b = 0; b < 131068; b++)
	    for (int a = 0; a < 131068; a++)
	    {
	      
	      A[a]=A[a+4]-B[a][b]*C[a][b][c];
	    }

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_1d_array(A);
	deallocate_3d_array(C, 64, 16, 16);
	deallocate_2d_array(B, 256, 128);
    return 0; 
    }