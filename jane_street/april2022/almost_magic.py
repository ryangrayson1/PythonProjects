# Ryan Grayson
# Jane Street Puzzle April 2022
# Almost Magic

def almost_magic(square):
    sums = set()
    for i in range(3):
        sums.add(sum(square[3*i:3*i+3]))
        sums.add(square[i] + square[i + 3] + square[i + 6])
    sums.add(square[0] + square[4] + square[8])
    sums.add(square[2] + square[4] + square[6])
    print(sums)
    return len(sums) == 1 or (len(sums) == 2 and abs(sums.pop() - sums.pop()) == 1)

# expects a list representing the puzzle grid (28 elements) 
# returns true if it is almost magic, else false
def valid_grid(grid):
    squares = []
    squares.append(grid[:3] + grid[3:6] + grid[9:12])
    squares.append(grid[5:8] + grid[11:14] + grid[17:20])
    squares.append(grid[8:11] + grid[14:17] + grid[20:23])
    squares.append(grid[16:19] + grid[22:25] + grid[25:])

    for square in squares:
        print(square)
        print()
        if not almost_magic(square):
            return False

    return sum(grid) < 1111




example = [50, 72, 16, 12, 46, 80, 75, 53, 77, 76, 20, 43, 69, 96, 1, 58, 114, 85, 64, 59, 95, 40, 39, 88, 137, 111, 90, 62]
print(sum(example))
print(valid_grid(example))