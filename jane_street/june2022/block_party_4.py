# Ryan Grayson
# Jane Street Puzzle June 2022

'''
Block Party 4

Fill each region with the numbers 1 through N, where N is the number of cells in the region. 
For each number K in the grid, the nearest K via taxicab distance must be exactly K cells away.
Once the grid is completed, the answer to the puzzle is found as follows: 
compute the product of the values in each row, and then take the sum of these products.
'''
# original_grid = [
#     [0, 3, 0, 0, 0, 7, 0, 0, 0, 0],
#     [0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [6, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 3, 0, 6],
#     [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
#     [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 6, 0, 0, 0],
#     [0, 0, 0, 0, 5, 0, 0, 0, 2, 0],
# ]

# manually did some of the puzzle because program was initially too slow
grid = [
    [0, 3, 6, 0, 3, 7, 0, 0, 6, 5],
    [0, 0, 2, 4, 1, 1, 2, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 1, 2, 4],
    [0, 0, 0, 1, 0, 6, 3, 1, 1, 3],
    [6, 0, 1, 1, 0, 0, 1, 4, 2, 7],
    [0, 1, 0, 5, 1, 0, 1, 3, 5, 6],
    [0, 0, 0, 0, 0, 0, 2, 1, 2, 3],
    [0, 2, 0, 0, 0, 1, 0, 1, 4, 0],
    [0, 0, 0, 0, 0, 0, 6, 2, 3, 0],
    [0, 0, 0, 0, 5, 0, 4, 0, 2, 5],
]

sections = [
    [ (0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (5, 0), (6, 0) ],
    [ (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4) ],
    [ (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 5), (1, 8), (1, 9) ],
    [ (1, 6), (1, 7), (2, 7) ],
    [ (2, 2), (2, 3), (3, 3) ],
    [ (2, 4), (2, 5) ],
    [ (2, 6), (3, 5), (3, 6), (3, 7), (4, 7), (4, 8) ],
    [ (2, 8), (2, 9), (3, 8), (3, 9), (4, 9), (5, 8), (5, 9) ],
    [ (3, 2), (4, 1), (4, 2), (5, 2) ],
    [ (3, 4), (4, 3), (4, 4) ],
    [ (4, 5), (5, 5) ],
    [ (4, 6) ],
    [ (5, 1) ],
    [ (5, 3), (6, 3), (6, 4), (6, 5), (7, 4) ],
    [ (5, 4) ],
    [ (5, 6), (5, 7), (6, 6) ],
    [ (6, 1), (7, 0), (7, 1), (8, 0), (8, 1), (8, 2), (9, 0), (9, 1), (9, 2), (9, 3) ],
    [ (6, 2), (7, 2) ],
    [ (6, 7), (6, 8), (6, 9) ],
    [ (7, 3), (8, 3), (8, 4), (9, 4), (9, 5) ],
    [ (7, 5) ],
    [ (7, 6), (7, 9), (8, 5), (8, 6), (8, 9), (9, 6), (9, 7), (9, 8), (9, 9) ],
    [ (7, 7), (7, 8), (8, 7), (8, 8) ],
]

section_nums = []
for section in sections:
    section_nums.append(set())
    for box in section:
        row, col = box
        if grid[row][col] != 0:
            section_nums[-1].add(grid[row][col])
ls = len(sections)

# returns true if no nums are too close to fit puzzle constraints, else false
def no_encroaching_nums(row, col, num):
    for i in range(max(0, row - num + 1), min(row + num, 10)):
        width = num - abs(i - row) - 1
        for j in range(max(0, col - width), min(col + width + 1, 10)):
            if (i != row or j != col) and grid[i][j] == num:
                return False
    return True

#returns true if there is either a 0 or another instance of the same number the correct taxicab distance away
def valid_closest_num(row, col, num):
    for i in range(max(0, row - num), min(row + num + 1, 10)):
        offset = num - abs(i - row)
        if col - offset >= 0 and (grid[i][col - offset] == 0 or grid[i][col - offset] == num):
            return True
        if col + offset < 10 and (grid[i][col + offset] == 0 or grid[i][col + offset] == num):
            return True
    return False

#returns the next box to fill, completing each whole section before moving on to the next
def get_next_box(section_id, section_pos):
    if section_pos == len(sections[section_id]) - 1:
        if section_id == ls - 1:
            return None, None
        return section_id + 1, 0
    return section_id, section_pos + 1
    
# recursive solution similar to sudoku solver
def fill_one_box(section_id, section_pos):
    # pass over filled boxes
    row, col = sections[section_id][section_pos]
    while grid[row][col] != 0:
        section_id, section_pos = get_next_box(section_id, section_pos)
        if section_id == None:
            return True
        row, col = sections[section_id][section_pos]

    print("section_id:", section_id, "section_pos:", section_pos)

    # try a possible number until it is seen to be invalid, then move on
    section_size = len(sections[section_id])
    for num in range(1, section_size + 1):
        if num not in section_nums[section_id]:
            grid[row][col] = num
            section_nums[section_id].add(num)
            valid = 1
            for i in range(10):
                for j in range(10):
                    if grid[i][j] != 0:
                        if not no_encroaching_nums(i, j, grid[i][j]) or not valid_closest_num(i, j, grid[i][j]):
                            valid = 0
                            break
                if not valid:
                    break
            new_si, new_sp = get_next_box(section_id, section_pos)
            if not valid:
                grid[row][col] = 0
                section_nums[section_id].remove(num)
            elif new_si is None or fill_one_box(new_si, new_sp):
                return True
            else:
                grid[row][col] = 0
                section_nums[section_id].remove(num)

    return False


fill_one_box(0, 0)
print('\n')
print('final grid:')
for r in grid:
    print(r)
print()
answer = 0
for row in grid:
    cur = 1
    for num in row:
        cur *= num
    answer += cur
print('answer: ', answer)
print()