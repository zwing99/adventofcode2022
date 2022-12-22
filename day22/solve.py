import re
import sys
import functools

path_re = re.compile(r"(\d+[RL])")
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
SIZE_CUBE = 50 if filename == "input.txt" else 4
X = 0
Y = 1

with open(filename) as fh:
    lines = [line.rstrip("\r\n") for line in fh.readlines()]


def pad_to_max_len(x, max_len):
    to_add = max_len - len(x)
    return x + to_add * " "


def to_map(chr):
    if chr == ".":
        return 0
    elif chr == "#":
        return 1
    else:  # empty space
        return 2


def to_print(chr):
    if chr == 0:
        return '.'
    elif chr == 1:
        return '#'
    elif chr == 2:
        return ' '
    return 'Z'


def print_grid(grid, path = []):
    p_grid = []
    for l in grid:
        p_grid.append([to_print(x) for x in l])
        # print(l)
    for item in path:
        p_grid[item[Y]][item[X]] = 'X'
    p_grid[item[Y]][item[X]] = 'Z'
    for row in p_grid:
        print("".join(row))
    


grid_lines = [line for line in lines if "." in line]
max_len = max([len(x) for x in grid_lines])
sequence = [line for line in lines if "L" in line][0]
grid = tuple(
    [tuple([to_map(x) for x in pad_to_max_len(line, max_len)]) for line in grid_lines]
)
MAX_Y = len(grid)
MAX_X = len(grid[0])
start = (min(grid[0].index(1), grid[0].index(0)), 0)
# print_grid(grid)
# print(start)

steps = []
for s in path_re.findall(sequence):
    amt = int(s[:-1])
    direction = s[-1]
    steps.append((amt, direction))
i = -1
while sequence[i] not in ('R','L'):
    i -= 1
steps.append((int(sequence[i+1:]), 'Z'))
# print(steps)


def get_next_mov(mov, d):
    if d == 'Z':
        return mov
    elif mov == (1, 0):
        if d == "L":
            return (0, -1)
        elif d == "R":
            return (0, 1)
        else:
            exit(99)
    elif mov == (-1, 0):
        if d == "L":
            return (0, 1)
        elif d == "R":
            return (0, -1)
        else:
            exit(99)
    elif mov == (0, 1):
        if d == "L":
            return (1, 0)
        elif d == "R":
            return (-1, 0)
        else:
            exit(99)
    elif mov == (0, -1):
        if d == "L":
            return (-1, 0)
        elif d == "R":
            return (1, 0)
        else:
            exit(99)
    else:
        exit(99)


def get_facing_num(mov):
    if mov == (1, 0):
        return 0
    elif mov == (0, 1):
        return 1
    elif mov == (-1, 0):
        return 2
    elif mov == (0, -1):
        return 3
    else:
        exit(99)


def at_extent(v, MAX_V):
    if v == MAX_V:
        return 0
    elif v == -1:
        return MAX_V - 1
    return v


def move(grid, pos, mov):
    next_x = at_extent(pos[X] + mov[X], MAX_X)
    next_y = at_extent(pos[Y] + mov[Y], MAX_Y)
    while grid[next_y][next_x] == 2:
        next_x = at_extent(next_x + mov[X], MAX_X)
        next_y = at_extent(next_y + mov[Y], MAX_Y)
    if grid[next_y][next_x] == 1:
        return pos
    return (next_x, next_y)


# part 1
path = [start]
pos = start
mov = (1, 0)
for amt, d in steps:
    # take_steps:
    previous_pos = pos
    for i in range(amt):
        pos = move(grid, pos, mov)
        if pos != previous_pos:
            path.append(pos)
        previous_pos = pos
    # turn:
    mov = get_next_mov(mov, d)
    #print_grid(grid, path)
    #print("-"*(MAX_X+10))

final_x, final_y = pos[X] + 1, pos[Y] + 1
facing_num = get_facing_num(mov)

#print_grid(grid, path)
print(mov)
print(final_y, final_x, facing_num)
print(1000 * final_y + 4 * final_x + facing_num)

# 93242
# 93226

# part 2