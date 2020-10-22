#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *B = create_one_dim_int(524288, "random");
	int **A = create_two_dim_int(512, 256, "random");
    clock_t start = clock();

	for (int d = 1; d < 252; d++)
	  for (int c = 2; c < 510; c++)
	    for (int b = 2; b < 510; b++)
	      for (int a = 2; a < 510; a++)
	      {
	        
	       B[a]=A[a][b];
	       A[a][b]=B[a]-A[a][b];
	        
	       B[a]=12;
	        
	       A[a][b]=B[a];
	        
	       B[a]=A[a][b]*B[a];
	       B[a]=A[a][b+4]-B[a];
	        
	       B[a]=A[a][b]*B[a];
	       B[a]=A[a+2][b+1]*24;
	        
	       B[a]=A[a][b]+B[a];
	       B[a]=A[a+2][b]-B[a];
	      }

    clock_t stop = clock();
    double elapsed = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("%f", elapsed); 
	deallocate_1d_array(B);
	deallocate_2d_array(A, 512, 256);
    return 0; 
    }