import os
import sys
import json
import math
import random
import string
import re
import cgen as c
import datetime
from auxillary_functions import get_timestamp

from dependencies_templates import flow_dependency, anti_dependency, output_dependency, input_dependency


def create_file_name():
    extension = '.c'
    file_name = 'src/kern' + '_' + get_timestamp() + extension
    return file_name


result_c_file = create_file_name()
input_file = sys.argv[1]
dependency_function = {'FLOW': (lambda dest, source, optimize, mix_in: flow_dependency(dest, source, optimize, mix_in)),
                       'ANTI': (lambda dest, source, optimize, mix_in: anti_dependency(dest, source, optimize, mix_in)),
                       'OUTPUT': (
                           lambda dest, source, optimize, mix_in: output_dependency(dest, source, optimize, mix_in)),
                       'INPUT': (
                           lambda dest, source, optimize, mix_in: input_dependency(dest, source, optimize, mix_in))}

unique_arrays_write = {"used": set(), "unused": set()}
unique_arrays_read = {"used": set(), "unused": set()}
array_init_functions = {1: 'create_one_dim_', 2: 'create_two_dim_', 3: 'create_three_dim_'}
array_dealloc_functions = {1: 'deallocate_1d_array', 2: 'deallocate_2d_array', 3: 'deallocate_3d_array'}

"""
Dicts used to keep control of arrays used in statements. 
Needed to optimize (reduce) the number of statements.
KEYS: string, used arrays with their access functions
VALUES: int, represents number of line of code (within statements) 
in which this array access function was used for the first time.
<destination> = <source>
"""
literal_values_source = {}
literal_values_destination = {}

stmt_counter = 0

maths_operations = ['+', '-', '*']
amount_of_vars = 0
types_to_init = ['int', 'float', 'double']
init_with = ['ones', 'zeros', 'random']


def gen_random_scalar():
    if type_to_init == 'int':
        return random.randint(0, 50)
    else:
        return round(random.random(), 3)


def populate_values(destination, source):  # todo rename
    """
    Update dicts of destination and sources array usages.
    """
    populate_literal_values(literal_values_destination, destination)
    populate_literal_values(literal_values_source, source)


def inc_stmt_counter():
    """
    Increment statement counter by 1 when a new statement is added.
    """
    global stmt_counter
    stmt_counter += 1


def generate_var(type):
    """
    Generate names for variables to store data when "init_with" in input file is set to "num_val"
    so as not to generate any new dependencies.
    """
    global amount_of_vars
    first_iterator = 'a'
    calculated_iterator = chr(ord(first_iterator) + amount_of_vars % 26)
    random_var = type + " var_" + calculated_iterator
    amount_of_vars += 1
    return random_var


def gen_random_stmt(unique_arrays):
    """
    If there are any unused arrays, get one, other way choose randomly from used.
    Add indexes to array (less than loops nest depth).
    """
    if unique_arrays['unused']:
        el = random.sample(unique_arrays['unused'], 1)[0]
        unique_arrays['unused'].remove(el)
        unique_arrays['used'].add(el)
    else:
        el = random.sample(unique_arrays['used'], 1)[0]
    curr = el[0]
    for size in range(len(el[1])):
        curr += f'[{generate_loop_index(size % loop_nest_level)}]'
    return curr


def generate_loop_index(loop_level):
    first_iterator = 'a'
    calculated_iterator = chr(ord(first_iterator) + loop_level % 26)
    return calculated_iterator


def parse_string_array(name_with_dims):
    """From string array in input make a tuple (name, (sizes))"""
    name_with_dims = name_with_dims.replace(" ", "").split('[')
    array_name = name_with_dims[0]
    sizes = name_with_dims[1][:-1].split(',')
    iter = 0
    for size in sizes:
        size.replace(" ", "")
        if re.match(r'(\d+)', size):
            sizes[iter] = int(size)
        elif re.match(r'((-\d+)|(\d+\.\d*)|(\d*\.\d+)([eE][+-]?\d+)?)', size):
            raise TypeError("Allowed sizes for arrays are only positive integer")
        elif size in array_sizes_vars:
            if array_sizes_vars[size] > 0:
                sizes[iter] = array_sizes_vars[size]
            else:
                raise TypeError("Allowed array size is only positive integer")
        else:
            error = f'There is no variable for array size named "{size}"'
            raise TypeError(error)
        iter += 1
    sizes = tuple(map(int, sizes))
    return (array_name, sizes)


def gen_calc_for_read(num_of_calculations, arr_def):
    """
    Random right-hand side of a statement is created by merging
    arrays and operators drew by lot.
    """
    stmt = ""
    arrays = generate_arrays_with_indexes1(num_of_calculations, arr_def)
    operators = generate_operators(num_of_calculations)
    for i in range(num_of_calculations):
        stmt += operators[i]
        stmt += str(arrays[i])
    return stmt


def generate_arrays_with_indexes1(num_of_calculations, arr_def):  # todo rename to generate_arrays_with_indexes
    """
    Generate a right-hand side of a statement.
    Favor to use unused arrays from "unique_arrays_read".
    :return: an array of array names
    """

    # temporarily remove the array on which we create dependencies so as not to use it again in the same stmt
    tmp_used, tmp_unused = False, False
    if arr_def in unique_arrays_read['unused']:
        tmp_unused = True
        unique_arrays_read['unused'].remove(arr_def)
    if arr_def in unique_arrays_read['used']:
        tmp_used = True
        unique_arrays_read['used'].remove(arr_def)

    gen_arr = generate_arrays_helper1([], num_of_calculations, arr_def)

    if tmp_unused:
        unique_arrays_read['unused'].add(arr_def)
    if tmp_used:
        unique_arrays_read['used'].add(arr_def)

    # reduce number of numerical values by adding them only with 24% of probability
    global coin_flip
    coin_flip = random.random()
    if coin_flip > 0.75:  # todo clean code extract to another function
        scalar_position_in_arr = random.randrange(0, len(gen_arr))
        gen_arr.append(gen_arr[scalar_position_in_arr])
        gen_arr[scalar_position_in_arr] = ('', gen_random_scalar())
    res = []
    for el in gen_arr:
        curr = el[0]
        if type(el[1]) is tuple:
            for size in range(len(el[1])):
                curr += f'[{generate_loop_index(size % loop_nest_level)}]'
        else:
            curr = el[1]
        res.append(curr)
    return res


def generate_arrays_helper1(arrays_drew_by_lot, num_of_calculations, arr_def):
    """
    Draw arrays by lot from the unique_arrays_read so as to use them as a right-hand side of a stmt.
    :return: arrays of array names drew by lot
    """
    if num_of_calculations > 0:
        unused_arr_size = len(unique_arrays_read['unused'])
        if unused_arr_size > 0:
            random_sample = random.sample(unique_arrays_read['unused'], min(num_of_calculations, unused_arr_size))
            for el in random_sample:
                unique_arrays_read['unused'].remove(el)
                unique_arrays_read['used'].add(el)
        else:
            random_sample = random.sample(unique_arrays_read['used'],
                                          min(num_of_calculations, len(unique_arrays_read['used'])))
        num_of_calculations -= len(random_sample)
        arrays_drew_by_lot += random_sample
        generate_arrays_helper1(arrays_drew_by_lot, num_of_calculations, arr_def)
    return arrays_drew_by_lot


def generate_operators(num_of_calculations):
    """
    :return: an array of mathematical operators from {+, -, *, /} drew by lot
    """
    global maths_operations_size
    maths_operations_size = len(maths_operations)
    if coin_flip > 0.75:  # if there is a scalar added increase the number of operators
        num_of_calculations += 1
    return generate_operators_helper([], num_of_calculations)


def generate_operators_helper(maths_oper_drew_by_lot, num_of_calculations):
    """
    Use recursion to generate expected amount of maths_operations.
    """
    if num_of_calculations > 0:
        tmp = random.sample(maths_operations, min(num_of_calculations, len(maths_operations)))
        maths_oper_drew_by_lot += tmp
        num_of_calculations -= len(tmp)
        generate_operators_helper(maths_oper_drew_by_lot, num_of_calculations)
    return maths_oper_drew_by_lot


def parse_input():
    """
    Parse input, init global variables, call validate sizes for arrays. Put all arrays to 'unused'.
    """
    with open(input_file, 'r') as file:
        data = json.load(file)[0]
        global loop_nest_level, unique_arrays_write, unique_arrays_read, dependencies, all_arrays, array_sizes_vars, \
            distances_vars, type_to_init, rand_num_of_calculations, init_with
        loop_nest_level = validate_loop_nest_lvl(data['loop_nest_level'])
        type_to_init = validate_type(data['type'])
        init_with = validate_init_value(data['init_with'])
        unparsed_arrays_write = data['unique_arrays_write']
        unparsed_arrays_read = data['unique_arrays_read']
        array_sizes_vars = data['array_sizes']
        distances_vars = data['distances']
        for arr in unparsed_arrays_write:
            unique_arrays_write['unused'].add(parse_string_array(arr))
        for arr in unparsed_arrays_read:
            unique_arrays_read['unused'].add(parse_string_array(arr))
        all_arrays = validate_array_sizes()
        dependencies = parse_dependencies(data['dependencies'])
        rand_num_of_calculations = []
    for i in range(len(unique_arrays_read["unused"]) - 1):
        rand_num_of_calculations.append(i + 1)


def validate_loop_nest_lvl(lvl_to_validate):
    if type(lvl_to_validate) == int:
        return lvl_to_validate
    else:
        raise TypeError("Wrong loop nest level")


def validate_type(type_to_validate):
    if type_to_validate in types_to_init:
        return type_to_validate
    else:
        error = f'Possible types are: {types_to_init}'
        raise TypeError(error)


def validate_init_value(init_to_validate):
    if init_to_validate in init_with:
        return init_to_validate
    else:
        error = f'Possible values to validate arrays with are: {init_with}'
        raise TypeError(error)


def parse_dependencies(all_dependencies):
    """
    Check if left_side_index and distances are correct, parse indexes, check if optimization is possible.
    :arg all_dependencies: not parsed dependencies
    :return dependencies with parsed indexes
    """
    for dependency_name, arrays in all_dependencies.items():
        for array in arrays:
            array_name = array['array_name']
            try:
                all_arrays[array_name]
            except KeyError:
                error = f'Array "{array_name}" does not exist'
                raise TypeError(error)

            flip = random.choice(('-1', '+1'))
            tmp_distance = []

            deps_to_parse = re.findall(r'\(.*?\)', array['distance'])
            distances = []
            for dep in deps_to_parse:
                distances.append(parse_indexes(dep))

            # if at least one distance consists of 0, it can't be optimized
            optimize = True
            for dist in distances:
                filtered_dist = list(filter(lambda x: x == 0, dist))
                if len(filtered_dist) == len(dist):
                    optimize = False
            array['optimize'] = optimize

            # parse left_side_index
            if 'left_side_index' in array:
                left_side_index = parse_indexes(array['left_side_index'])
            else:
                left_side_index = tuple(0 for _ in range(0, len(distances[0])))
            array['left_side_index'] = left_side_index

            # check if left_side_index has the same size as array
            if not len(all_arrays[array_name]) == len(left_side_index):
                error = f'Array {array_name} has wrong left side index'
                raise TypeError(error)

            # check if distance has the same size as array
            if not len(list(filter(lambda x: len(x) == len(all_arrays[array_name]), distances))) == len(distances):
                error = f'Array {array_name} has wrong distance size in dependency'
                raise TypeError(error)

            for index in range(len(distances[0])):
                dest_dist = left_side_index[index]
                # check if distance is a positive number less then size
                for d in distances:
                    if d[index] < 0 or d[index] > all_arrays[array_name][index]:
                        error = f'Array {array_name} has wrong distance in dependency'
                        raise TypeError(error)

                if dependency_name == 'FLOW':
                    distance = [-d[index] + dest_dist for d in distances]
                elif dependency_name == 'ANTI':
                    distance = [d[index] + dest_dist for d in distances]
                else:
                    distance = [eval(flip) * d[index] + dest_dist for d in distances]

                distance.insert(0, dest_dist)
                distance = tuple(distance)
                tmp_distance.append(distance)
            array['distance'] = tuple(tmp_distance)
    return all_dependencies


def parse_indexes(tuple_to_parse):
    """
    Check if it is a positive int or variable from 'distances', otherwise throws exception.
    :arg tuple_to_parse: tuple to parse from json with 'left_side_index' or 'distance'
    :return parsed tuple
    """
    parsed_indexes = []
    tuple_to_parse = tuple_to_parse.replace(" ", "")[1:-2]
    tuple_to_parse = tuple_to_parse.split(',')
    for index in tuple_to_parse:
        if re.match(r'(\d+)|(-\d+)', index):
            parsed_indexes.append(int(index))
        elif re.match(r'((\d+\.\d*)|(\d*\.\d+)([eE][+-]?\d+)?)', index):
            raise TypeError("Allowed distance is only positive integer")
        elif index in distances_vars:
            if distances_vars[index] >= 0:
                parsed_indexes.append(distances_vars[index])
            else:
                raise TypeError("Allowed distance is only positive integer")
        else:
            error = f'There is no variable for distance named "{index}"'
            raise TypeError(error)
    return tuple(parsed_indexes)


def generate_nested_loops(loop_nest_depth, affine):
    """
    :arg loop_nest_depth: the loop nest depth
    recursively function to create for loop with depth d.
    The most inner loop run dependencies.
    Choose upper bound by going through each appropriate size of each array.
    :return for loop with depth d
    """
    loop_index = generate_loop_index(loop_nest_depth - 1)
    lower_bound = 0
    upper_bound = float("inf")
    for array_name, array_size in all_arrays.items():
        array_length = len(array_size)
        for index in range(loop_nest_depth - 1, array_length, loop_nest_level):
            if array_size[index] < upper_bound:
                upper_bound = array_size[index]

    if loop_nest_depth > 1 and not affine[0][1:]:
        return print_loop_structure(loop_index, lower_bound, upper_bound, affine,
                                    generate_nested_loops(loop_nest_depth - 1, affine))
    elif loop_nest_depth == 1:
        return print_loop_structure(loop_index, lower_bound, upper_bound, affine, run_dependencies())
    else:
        return print_loop_structure(loop_index, lower_bound, upper_bound, affine,
                                    generate_nested_loops(loop_nest_depth - 1, [affine[0][1:], affine[1][1:]]))


def print_loop_structure(loop_index, lower_bound, upper_bound, affine, fun):
    """
    Print loop structure: for(int {} = {}; {} < {}; {}++){ ... }
    """
    gen_scalar_part = ''
    curr_val = affine[1][0]
    if curr_val > 0:
        gen_scalar_part = ' - '
    elif curr_val < 0:
        gen_scalar_part = ' + '
    gen_scalar_part += str(abs(curr_val))
    return c.For('int {} = {}'.format(loop_index, affine[0][0]),
                 '{} < '.format(loop_index)
                 # + str(upper_bound)
                 + str(affine[1][0]),
                 '{}++'.format(loop_index),
                 fun)


def create_nested_loop():
    """
    Calls generate_nested_loops(d, i) and write it to file
    """
    with open(result_c_file, 'a+') as file:
        file.write('\n\n')
        for line in str(
                generate_nested_loops(loop_nest_level, adjust_bounds(global_bounds()))).splitlines():  # todo: rewrite
            file.write('\t{}\n'.format(line))


def init_dyn_arrays(file=result_c_file):
    """Init all arrays"""
    for array_name, array_size in all_arrays.items():
        write_init_dyn_array(array_name, array_size, file, type_to_init, init_with)


def write_init_dyn_array(array_name, array_sizes, file, typ='float', init_with='random'):
    """Write declaration and calling functions to init arrays to file"""
    if type(array_sizes) == tuple and len(array_sizes) == 1:
        init_array = c.Statement('\n\t{} {}{} = {}{}({}, "{}")'.format(typ, '*' * len(array_sizes), array_name,
                                                                       array_init_functions[len(array_sizes)], typ,
                                                                       str(array_sizes)[1:-2], init_with))
    else:
        init_array = c.Statement('\n\t{} {}{} = {}{}({}, "{}")'.format(typ, '*' * len(array_sizes), array_name,
                                                                       array_init_functions[len(array_sizes)], typ,
                                                                       str(array_sizes)[1:-1], init_with))
    with open(file, 'a+') as file:
        file.write(str(init_array))


def init_static_arrays(file=result_c_file):
    """Init all arrays"""
    for array_name, array_size in all_arrays.items():
        write_init_static_array(array_name, array_size, file, type_to_init)


def write_init_static_array(array_name, array_sizes, file, typ='int'):
    number_of_dimensions = len(array_sizes)
    if number_of_dimensions == 1:
        init_array = c.Statement('\n\t {} {}[{}] = {{0}}'.format(typ, array_name,*array_sizes))
    elif number_of_dimensions == 2:
        init_array = c.Statement('\n\t {} {}[{}][{}] = {{0}}'.format(typ, array_name, *array_sizes))
    else:
        init_array = c.Statement(
            '\n\t {} {}[{}][{}][{}] = {{0}}'.format(typ, array_name,*array_sizes))
    with open(file, 'a+') as file:
        file.write(str(init_array))


def dealloc_arrays(file=result_c_file):
    for array_name, array_size in all_arrays.items():
        write_dealloc_array(array_name, array_size, file)


def write_dealloc_array(array_name, array_sizes, file):
    number_of_dimensions = len(array_sizes)
    if number_of_dimensions == 1:
        dealloc_array = c.Statement('\n\t{}({})'.format(array_dealloc_functions[number_of_dimensions], array_name))
    else:
        dealloc_array = c.Statement('\n\t{}({}, {})'.format(array_dealloc_functions[number_of_dimensions], array_name,
                                                            str(array_sizes)[1:-1]))
    with open(file, 'a+') as file:
        file.write(str(dealloc_array))


def run_dependencies():
    """Go throw all dependencies, find indexes for each dependency and put each
     created dependency into c.Statement
    :return c.Block containing all statements
    """
    block_with_statements = []
    for dependency_name, arrays in dependencies.items():
        if arrays:
            for array in arrays:
                array_name = array['array_name']
                distances = array['distance']
                optimize = array['optimize']
                mix_in = array['mix_in']
                if not mix_in == 'random' and not mix_in == 'num_val':
                    raise KeyError("Mix_in can be only 'random' or 'num_val'")

                for arr_name, arr_size in all_arrays.items():
                    if array_name == arr_name:
                        dest_array = array_name
                        src_array = [array_name for _ in range(len(distances[0]) - 1)]
                        for index in range(len(arr_size)):
                            distance = distances[index]
                            if distance[0] == 0:
                                dest_dist = ''
                            elif str(distance[0])[0] == '-':
                                dest_dist = str(distance[0])
                            else:
                                dest_dist = '+' + str(distance[0])
                            for i in range(1, len(distances[0])):
                                if distance[i] == 0:
                                    src_dist = ''
                                elif str(distance[i])[0] == '-':
                                    src_dist = str(distance[i])
                                else:
                                    src_dist = '+' + str(distance[i])
                                src_array[i - 1] += f'[{generate_loop_index(index % loop_nest_level)}{src_dist}]'
                            dest_array += f'[{generate_loop_index(index % loop_nest_level)}{dest_dist}]'
                            src_array_str = ''
                            for src in src_array:
                                src_array_str += src + random.choice(maths_operations)
                        stmt = dependency_function[dependency_name](dest_array, src_array_str[:-1], optimize, mix_in)
                        if stmt:
                            block_with_statements.append(c.Statement('\n' + add_indent() + stmt))
    return c.Block(block_with_statements)


def validate_array_sizes():
    """Make union of read and write arrays, add array to array_dict if it's not there, otherwise
     checks if the sizes for similar arrays are the same if not raise an error
    :return dict with arrays name as key and size as value
    """
    arrays_union = unique_arrays_write['unused'].union(unique_arrays_read['unused'])
    arrays_dict = {}
    for el in arrays_union:
        if el[0] in arrays_dict and el[1] != arrays_dict[el[0]]:
            error = f'Arrays {el[0]} have different sizes'
            raise TypeError(error)
        else:
            arrays_dict[el[0]] = el[1]
    return arrays_dict


def adjust_bounds(affine_fcts):
    """
    Calculate loop bounds (lower and upper) for for-loops.
    """
    max_tuple_size = 0
    for tupl in affine_fcts:
        max_tuple_size = max(max_tuple_size, len(tupl[1]))

    max_tuple_size = min(max_tuple_size,
                         loop_nest_level)  # in case of arrays with bigger dimensions than the loop nest size

    lower_bounds = [-math.inf] * max_tuple_size
    upper_bounds = [math.inf] * max_tuple_size

    for tupl in affine_fcts:
        index = 0
        for t in tupl[1]:
            index = index % loop_nest_level
            lower_bounds[index] = max(lower_bounds[index], -1 * int(t[0]))
            lower_bounds[index] = max(lower_bounds[index], -1 * int(t[1]))
            upper_bounds[index] = min(upper_bounds[index], all_arrays[tupl[0]][index] - int(t[0]))
            upper_bounds[index] = min(upper_bounds[index], all_arrays[tupl[0]][index] - int(t[1]))

            lower_bounds[index] = max(lower_bounds[index],
                                      0)  # 0 because of "random" part which is always without a translation
            upper_bounds[index] = min(upper_bounds[index],
                                      all_arrays[tupl[0]][index])  # don't exceed the size of an array
            index += 1

    return [lower_bounds[::-1], upper_bounds[::-1]]


def global_bounds():
    """
    todo
    :return:
    """
    global concat_depen  # todo rename
    concat_depen = []
    for dependency_name, arrays in dependencies.items():
        if arrays:
            for array in arrays:
                concat_depen.append([array['array_name'], array['distance']])
    return concat_depen


def populate_literal_values(literal_values_set, data):
    """
    Assign to each array[index] its first usage line.
    """
    data = "".join(data.split())  # remove all whitespaces
    expresion_as_string = get_arrays_from_string(data)
    for res in expresion_as_string:
        if res not in literal_values_set.keys():
            literal_values_set[res] = [0, stmt_counter]
        literal_values_set[res][0] += 1


def get_arrays_from_string(string_with_arrays):
    """
    Extract and return the list of arrays with name and its indexes
    """
    string_with_arrays = re.findall(r'(\w+(\[.*?\])+)', string_with_arrays)
    return [i[0] for i in string_with_arrays]


def add_indent():
    return " " * (loop_nest_level + 3)
