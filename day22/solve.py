import re
import sys
import operator
import functools

print("---p1---")
path_re = re.compile(r"(\d+[RL])")
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
SIZE_CUBE = 50 if filename == "input.txt" else 4
FLIP_MAP = dict(zip(range(SIZE_CUBE), range(SIZE_CUBE - 1, -1, -1)))
X = 0
Y = 1
T = True
F = False
FACE_MAP = {
    1: {  #   F, S, X, Y, mov
        "D": (2, F, T, T, (0, 1)),  # check
        "R": (6, F, T, T, (-1, 0)),  # check
        "U": (4, F, F, F, (0, 1)),  # check
        "L": (3, T, T, F, (0, 1)),  # check
    },
    2: {  #   F, S, X, Y, mov
        "D": (1, F, T, T, (0, 1)),  # check
        "R": (3, F, F, F, (1, 0)),  # check
        "U": (5, F, T, T, (0, -1)),  # check
        "L": (6, T, T, F, (0, -1)),  # check
    },
    3: {  #   F, S, X, Y, mov
        "D": (1, T, T, F, (1, 0)),  # check
        "R": (4, F, F, F, (1, 0)),  # check
        "U": (5, T, T, F, (1, 0)),  # check
        "L": (2, F, F, F, (-1, 0)),  # check
    },
    4: {  #   F, S, X, Y, mov
        "D": (1, F, F, F, (0, -1)),  # check
        "R": (6, T, T, F, (0, 1)),  # check
        "U": (5, F, F, F, (0, 1)),  # check
        "L": (3, F, F, F, (-1, 0)),  # check
    },
    5: {  #   F, S, X, Y, mov
        "D": (4, F, F, F, (0, -1)),  # check
        "R": (6, F, F, F, (1, 0)),  # check
        "U": (2, F, T, T, (0, -1)),  # check
        "L": (3, T, T, F, (0, -1)),  # check
    },
    6: {  #   F, S, X, Y, mov
        "D": (4, T, F, T, (-1, 0)),  # check
        "R": (1, F, T, T, (-1, 0)),  # check
        "U": (2, T, F, T, (1, 0)),  # check
        "L": (5, F, F, F, (-1, 0)),  # check
    },
}
if filename == "input.txt":
    FACE_MAP = {
        1: {  #   F, S, X, Y, mov
            "D": (6, T, T, F, (1, 0)),  # check
            "R": (2, F, F, F, (1, 0)),  # check
            "U": (3, F, F, F, (0, 1)),  # check
            "L": (4, F, T, T, (1, 0)),  # check
        },
        2: {  #   F, S, X, Y, mov
            "D": (6, F, F, F, (0, -1)),  # check
            "R": (5, F, T, T, (-1, 0)),  # check
            "U": (3, T, T, F, (-1, 0)),  # check
            "L": (1, F, F, F, (-1, 0)),  # check
        },
        3: {  #   F, S, X, Y, mov
            "D": (1, F, F, F, (0, -1)),  # check
            "R": (2, T, F, T, (0, -1)),  # check
            "U": (5, F, F, F, (0, 1)),  # check
            "L": (4, T, F, T, (0, 1)),  # check
        },
        4: {  #   F, S, X, Y, mov
            "D": (3, T, T, F, (1, 0)),  # check
            "R": (5, F, F, F, (1, 0)),  # check
            "U": (6, F, F, F, (0, 1)),  # check
            "L": (1, F, T, T, (1, 0)),  # check
        },
        5: {  #   F, S, X, Y, mov
            "D": (3, F, F, F, (0, -1)),  # check
            "R": (2, F, T, T, (-1, 0)),  # check
            "U": (6, T, T, F, (-1, 0)),  # check
            "L": (4, F, F, F, (-1, 0)),  # check
        },
        6: {  #   F, S, X, Y, mov
            "D": (4, F, F, F, (0, -1)),  # check
            "R": (5, T, F, T, (0, -1)),  # check
            "U": (2, F, F, F, (0, 1)),  # check
            "L": (1, T, F, T, (0, 1)),  # check
        },
    }

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
        return "."
    elif chr == 1:
        return "#"
    elif chr == 2:
        return " "
    return "Z"


def print_grid(grid, path=[]):
    p_grid = []
    for l in grid:
        p_grid.append([to_print(x) for x in l])
        # print(l)
    for item in path:
        p_grid[item[Y]][item[X]] = "X"
    p_grid[item[Y]][item[X]] = "Z"
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
while sequence[i] not in ("R", "L"):
    i -= 1
steps.append((int(sequence[i + 1 :]), "Z"))
# print(steps)


def get_next_mov(mov, d):
    if d == "Z":
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
        return pos, mov
    return (next_x, next_y), mov


# part 1
path = [start]
pos = start
mov = (1, 0)
for amt, d in steps:
    # take_steps:
    previous_pos = pos
    for i in range(amt):
        pos, mov = move(grid, pos, mov)
        if pos != previous_pos:
            path.append(pos)
        previous_pos = pos
    # turn:
    mov = get_next_mov(mov, d)
    # print_grid(grid, path)
    # print("-"*(MAX_X+10))

final_x, final_y = pos[X] + 1, pos[Y] + 1
facing_num = get_facing_num(mov)

# print_grid(grid, path)
print(mov)
print(final_y, final_x, facing_num)
print(1000 * final_y + 4 * final_x + facing_num)

# 93242
# 93226

# part 2
print("---p2---")


def which_face(pos):
    if filename != "input.txt":
        if pos[Y] < SIZE_CUBE:
            return 1
        elif pos[Y] >= SIZE_CUBE and pos[Y] < SIZE_CUBE * 2:
            if pos[X] < SIZE_CUBE:
                return 2
            elif pos[X] >= SIZE_CUBE and pos[X] < SIZE_CUBE * 2:
                return 3
            elif pos[X] >= SIZE_CUBE * 2:
                return 4
        elif pos[Y] >= SIZE_CUBE * 2:
            if pos[X] < SIZE_CUBE * 3:
                return 5
            elif pos[X] >= SIZE_CUBE * 3:
                return 6
        else:
            exit(97)
    else:
        if pos[Y] < SIZE_CUBE:
            if pos[X] < SIZE_CUBE * 2:
                return 1
            if pos[X] >= SIZE_CUBE * 2:
                return 2
        elif pos[Y] >= SIZE_CUBE and pos[Y] < SIZE_CUBE * 2:
            return 3
        elif pos[Y] >= SIZE_CUBE * 2 and pos[Y] < SIZE_CUBE * 3:
            if pos[X] < SIZE_CUBE:
                return 4
            elif pos[X] >= SIZE_CUBE:
                return 5
        elif pos[Y] >= SIZE_CUBE * 3:
            return 6
        else:
            exit(97)


def face_shift(pos, face, op=operator.sub):
    if filename != "input.txt":
        if face == 1:
            y = pos[Y]
            x = op(pos[X], SIZE_CUBE * 2)
            return (x, y)
        elif face in (2, 3, 4):
            y = op(pos[Y], SIZE_CUBE)
            x = pos[X]
            if face == 3:
                x = op(x, SIZE_CUBE)
            if face == 4:
                x = op(x, SIZE_CUBE * 2)
            return (x, y)
        elif face in (5, 6):
            y = op(pos[Y], SIZE_CUBE * 2)
            x = pos[X]
            if face == 5:
                x = op(x, SIZE_CUBE * 2)
            if face == 6:
                x = op(x, SIZE_CUBE * 3)
            return (x, y)
        else:
            exit(96)
    else:
        if face in (1, 2):
            y = pos[Y]
            if face == 1:
                x = op(pos[X], SIZE_CUBE)
            if face == 2:
                x = op(pos[X], SIZE_CUBE * 2)
            return (x, y)
        elif face == 3:
            y = op(pos[Y], SIZE_CUBE)
            x = op(pos[X], SIZE_CUBE)
            return (x, y)
        elif face in (4, 5):
            y = op(pos[Y], SIZE_CUBE * 2)
            if face == 4:
                x = pos[X]
            if face == 5:
                x = op(pos[X], SIZE_CUBE)
            return (x, y)
        elif face == 6:
            y = op(pos[Y], SIZE_CUBE * 3)
            x = pos[X]
            return (x, y)
        else:
            exit(96)
    exit(96)


def move_on_cube(pos, mov, face):
    p = face_shift(pos, face)
    #print(pos, p, mov, face)
    p = (p[X] + mov[X], p[Y] + mov[Y])
    #print(p)
    d = ""
    if p[X] < 0:
        d = "L"
        p = (SIZE_CUBE - 1, p[Y])
    elif p[X] >= SIZE_CUBE:
        d = "R"
        p = (0, p[Y])
    elif p[Y] < 0:
        d = "D"
        p = (p[X], SIZE_CUBE - 1)
    elif p[Y] >= SIZE_CUBE:
        d = "U"
        p = (p[X], 0)
    if d:  # need to shift
        face, swap, flip_x, flip_y, mov = FACE_MAP[face][d]
        if swap:
            p = (p[Y], p[X])
        if flip_x:
            p = (FLIP_MAP[p[X]], p[Y])
        if flip_y:
            p = (p[X], FLIP_MAP[p[Y]])
    pos = face_shift(p, face, operator.add)
    return pos, mov, face


def move_cube(grid, pos, mov):
    face = which_face(pos)
    new_pos, new_move, new_face = move_on_cube(pos, mov, face)
    if grid[new_pos[Y]][new_pos[X]] == 1:
        return pos, mov
    else:
        return new_pos, new_move


path = [start]
pos = start
mov = (1, 0)
for amt, d in steps:
    # take_steps:
    previous_pos = pos
    # print(amt, mov)
    for i in range(amt):
        pos, mov = move_cube(grid, pos, mov)
        if pos != previous_pos:
            path.append(pos)
        previous_pos = pos
    # turn:
    mov = get_next_mov(mov, d)
    #print_grid(grid, path)
    #print("-"*(MAX_X+10))

final_x, final_y = pos[X] + 1, pos[Y] + 1
facing_num = get_facing_num(mov)
# print_grid(grid, path)
print(mov)
print(final_y, final_x, facing_num)
print(1000 * final_y + 4 * final_x + facing_num)

# 124288