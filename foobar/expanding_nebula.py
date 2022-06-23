'''
Ryan Grayson
Google Foobar level 5: Expanding Nebula
06/14/22
'''
from collections import defaultdict

def get_next_nebula_row(prev_col1_val, prev_col2_val, next_bits):
    tl = prev_col1_val & ~(1 << next_bits)
    tr = prev_col2_val & ~(1 << next_bits)
    bl = prev_col1_val >> 1
    br = prev_col2_val >> 1
    return (tl & ~tr & ~bl & ~br) | (~tl & tr & ~bl & ~br) | (~tl & ~tr & bl & ~br) | (~tl & ~tr & ~bl & br)

def get_row_map(c, row_nums):
    # print(row_nums)
    map = defaultdict(set)
    for n1 in range(1 << (c + 1)):
        for n2 in range(1 << (c + 1)):
            next_gen = get_next_nebula_row(n1, n2, c)
            if next_gen in row_nums:
                map[(next_gen, n1)].add(n2)
    return map



def solution(g):
    g = list(zip(*g))
    c = len(g[0])
    row_nums = []
    for row in g:
        row_nums.append( sum([1 << i if bit else 0 for i, bit in enumerate(row)]) )

    # print(row_nums)
    
    row_nums_set = set(row_nums)
    row_map = get_row_map(c, row_nums_set)
    # print(row_map)

    prev_row_options = {}
    for prev_gen_num in range(1 << (c + 1)):
        prev_row_options[prev_gen_num] = 1

    # print(prev_row_options)
    
    for cur_row_val in row_nums:
        next_row = defaultdict(int)
        for c1 in prev_row_options:
            for c2 in row_map[(cur_row_val, c1)]:
                next_row[c2] += prev_row_options[c1]
        prev_row_options = next_row

    # print(prev_row_options)
    return sum(prev_row_options.values())



### TESTING ###
test1 = [
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 0], 
    [1, 1, 0, 0, 0, 0, 1, 1, 1, 0], 
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
    [0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
]
test2 = [
    [1, 0, 1], 
    [0, 1, 0], 
    [1, 0, 1],
]
test3 = [
    [1, 0, 1, 0, 0, 1, 1, 1], 
    [1, 0, 1, 0, 0, 0, 1, 0], 
    [1, 1, 1, 0, 0, 0, 1, 0], 
    [1, 0, 1, 0, 0, 0, 1, 0], 
    [1, 0, 1, 0, 0, 1, 1, 1],
]
print
print(solution(test1)) # expected 11567
print
print(solution(test2)) # expected 4
print
print(solution(test3)) # expected 254
print