#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "../init_array_lib/init_dyn_array.h"


int main( int argc, const char* argv[] )
{
    srand(time(NULL));

    
	int *A = create_one_dim_int(100, "random");
	int ***C = create_three_dim_int(50, 50, 50, "random");
	int **B = create_two_dim_int(50, 50, "random");

	for (int c = 0; c < 50; c++)
	  for (int b = 0; b < 50; b++)
	    for (int a = 5; a < 49; a++)
	    {
	      
	      A[a-3]=38;
	      A[a-3]=B[a][b]-C[a][b][c];
	      
	      C[a][b][c]=A[a];
	      C[a-1][b][c]=B[a][b];
	      
	      C[a][b][c]=42;
	      
	      int var_a=A[a-3]+41;
	      int var_b=A[a-5]/36;
	      
	      B[a][b]=C[a][b][c]*B[a][b]/A[a];
	      A[a]=C[a-1][b][c]*A[a];
	      
	      int var_c=C[a][b][c]/25;
	      int var_d=C[a+1][b][c]-3;
	    }

    return 0;
}