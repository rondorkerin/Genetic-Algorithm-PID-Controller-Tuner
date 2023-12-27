from functools import reduce
import random

def sum_list(L):
    return reduce(lambda x, y: x + y, L)

def avg_list(L):
    return sum_list(L) / (len(L) * 1.0)

def norm_list(L, normalize_to=1):
    v_max = max(L)
    return [x / (v_max * 1.0) * normalize_to for x in L]

def norm_list_sum_to(L, sum_to=1):
    _sum = sum_list(L)
    return [x / (_sum * 1.0) * sum_to for x in L]

def accum_list(L, normalize_to=None):
    new_list = [L[0]]
    for i in range(1, len(L)):
        new_list.append(new_list[-1] + L[i])

    if normalize_to:
        new_list = norm_list_sum_to(new_list, sum_to=normalize_to)

    return new_list

def find_index(sorted_list, x, index_buffer=0):
    if len(sorted_list) == 2:
        if x == sorted_list[-1]:
            return index_buffer + 2
        elif x >= sorted_list[0]:
            return index_buffer + 1

    else:
        L = len(sorted_list)
        first_half = sorted_list[:L//2 + 1]
        second_half = sorted_list[L//2:]

        if second_half[-1] <= x:
            return index_buffer + len(sorted_list)
        elif x < first_half[0]:
            return index_buffer
        else:
            if first_half[-1] < x:
                return find_index(second_half, x, index_buffer=L//2 + index_buffer)
            else:
                return find_index(first_half, x, index_buffer=index_buffer)

def random_pick_list(L):
    return find_index(accum_list(L, 1), random.random())

def deep_list(L_string):
    result = [x[0] for x in [x.split(']') for x in L_string.split('[') if len(x) > 1]]
    if result == ['']:
        result = []
    return result

def get_list_startswith(a_list, starts_with, is_strip=1):
    tmp = a_list[:]
    if is_strip:
        tmp = [x.strip() for x in tmp]

    start_line_index = 0
    for i in range(len(tmp)):
        if tmp[i].startswith(starts_with):
            start_line_index = i

    return a_list[start_line_index:]

def rezip(a_list):
    return list(map(list, zip(*a_list)))

def sum_in_list(complex_list):
    d = rezip(complex_list)
    return [sum_list(z) for z in d]

def avg_in_list(complex_list):
    d = rezip(complex_list)
    return [avg_list(z) for z in d]

def max_value_in_list(lst):
    return max(lst, default=None)

def max_index_in_list(lst):
    return lst.index(max_value_in_list(lst))

def min_value_in_list(lst):
    return min(lst, default=None)
