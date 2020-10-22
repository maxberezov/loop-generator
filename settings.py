import os


number_of_iterations_for_random_generation = 10


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
json_input_path = os.path.join(PROJECT_PATH, 'input')
src_path = os.path.join(PROJECT_PATH, 'src')
init_array_path = os.path.join(PROJECT_PATH, 'init_array_lib')
generation_script_path = os.path.join(PROJECT_PATH, 'create_kernels_with_deps.py')

array_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
dimension_names = 'xyzv'
number_of_array_range = [1, 2, 3, 4, 5]
number_of_arrays_weights = [0.25, 0.3, 0.25, 0.1, 0.1]
dimensions_of_array_range = (1, 3)
nest_eq_dimensionality_pattern = [[2 ** 18, 2 ** 19, 2 ** 17, 2 ** 16], [2 ** 9, 2 ** 8, 2 ** 7],
                                  [2 ** 6, 2 ** 5, 2 ** 4], [2 ** 6, 2 ** 5, 2 ** 4]]

huge_ranges = [[ 2 ** 21], [2 ** 14, 2 ** 13, 2 ** 12],
                                  [2 ** 10, 2 ** 9, 2 ** 8], [2 ** 10, 2 ** 9, 2 ** 8]]
loop_nest_level_range = (1, 4)
distances_range = (0, 5)
number_of_dependencies_range = [1, 2, 3, 4, 5, 6, 7]
number_of_dependencies_weights = [0.15,0.2,0.2,0.15,0.15,0.1,0.05]


array_type_options = ['int']
array_init_options = ['ones', 'zeros', 'random']
dependence_type_options = ['FLOW', 'ANTI', 'INPUT', 'OUTPUT']
mix_in_options = ['num_val', 'random']

header_string = r'''# if !defined(DATA_TYPE_IS_INT) && !defined(DATA_TYPE_IS_FLOAT) && !defined(DATA_TYPE_IS_DOUBLE)
#  define DATA_TYPE_IS_DOUBLE
# endif

#ifdef DATA_TYPE_IS_INT
#  define DATA_TYPE int
#  define DATA_PRINTF_MODIFIER "%d "
#endif

#ifdef DATA_TYPE_IS_FLOAT
#  define DATA_TYPE float
#  define DATA_PRINTF_MODIFIER "%0.2f "
#  define SCALAR_VAL(x) x##f
#  define SQRT_FUN(x) sqrtf(x)
#  define EXP_FUN(x) expf(x)
#  define POW_FUN(x,y) powf(x,y)
# endif
#ifdef DATA_TYPE_IS_DOUBLE
#  define DATA_TYPE double
#  define DATA_PRINTF_MODIFIER "%0.2lf "
#  define SCALAR_VAL(x) x
#  define SQRT_FUN(x) sqrt(x)
#  define EXP_FUN(x) exp(x)
#  define POW_FUN(x,y) pow(x,y)
# endif
# endif
'''

