from tqdm import tqdm
from copy import deepcopy
import sys
import math
from collections import deque
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

JETSTREAM = lines[0]
NUM_OF_JETSTREAM = len(JETSTREAM)

ROCK_SHAPES = [
    [[2,0],[3,0],[4,0],[5,0]]
    ,
    [      [3,2],
     [2,1],[3,1],[4,1],
           [3,0]]
    ,
    [            [4,2],
                 [4,1],
     [2,0],[3,0],[4,0]]
    ,
    [[2,3],
     [2,2],
     [2,1],
     [2,0]]
    ,
    [[2,1],[3,1],
     [2,0],[3,0]]
]
NUM_ROCK_SHAPES = len(ROCK_SHAPES)
X = 0
Y = 1

def get_next_rock(rock_num, max_row):
    rock = deepcopy(ROCK_SHAPES[rock_num % NUM_ROCK_SHAPES])
    for coord in rock:
        coord[Y] += max_row + 3
    return rock

def get_jet_direction(jet_count):
    jetchar = JETSTREAM[jet_count%NUM_OF_JETSTREAM]
    if jetchar == "<":
        return -1
    elif jetchar == ">":
        return 1
    else:
        print('bad')
        exit(1)


def run_blocks(total_rocks=2022, print_it=False):
    WIDTH = 7
    HEIGHT = 1000
    first_rows = []
    grid = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]
    shift_y = 0
    jet_count = 0
    max_row = 0
    for rock_num in tqdm(range(total_rocks)):
        rock = get_next_rock(rock_num, max_row)
        max_y = max([c[Y] for c in rock]) + 1
        for i in range(max_row + 1, max_y +1):
            for x in range(WIDTH):
                grid[i%HEIGHT][x] = 0
        while True:
            # shift rock
            ###############################################################
            jet_dir = get_jet_direction(jet_count)
            jet_count += 1
            # can shift
            can_shift = True
            for coord in rock:
                new_x, new_y = coord[X] + jet_dir, coord[Y]
                if new_x < 0 or new_x >= WIDTH:
                    can_shift = False
                    break
                elif grid[(new_y)%HEIGHT][new_x] != 0:
                    can_shift = False
                    break
            # shift if can
            if can_shift:
                if print_it: print(f"shift: {jet_dir}")
                for coord in rock:
                    coord[X] += jet_dir
            else:
                if print_it: print(f"no shift: {jet_dir}")
            # drop rock
            ###############################################################
            # can drop
            can_drop = True
            for coord in rock:
                new_x, new_y = coord[X], coord[Y] - 1
                if new_y < 0:
                    can_drop = False
                    break
                elif grid[(new_y)%HEIGHT][new_x] != 0:
                    can_drop = False
                    break
            # done with rock
            if not can_drop:
                break
            # drop rock
            if print_it: print(f"drop")
            for coord in rock:
                coord[Y] -= 1
        # set rock
        ###############################################################
        max_y = max([c[Y] for c in rock]) + 1
        if max_y > max_row:
            max_row = max_y
        for coord in rock:
            grid[(coord[Y])%HEIGHT][coord[X]] = 1
        if rock_num == 10:
            first_rows = grid[:10]


    #print(shift_y)
    last_rows = []
    for i in range(max_row - 10, max_row):
        last_rows.append(grid[i % HEIGHT])
    return max_row, first_rows, last_rows


def convert(x):
    if x == 0:
        return '.'
    elif x == 1:
        return '#'
    return ' '

def print_grid(grid):
    print("+" + 7*'-' + "+")
    for i in range(len(grid)-1, -1, -1):
        print("|" + "".join([convert(x) for x in grid[i]]) + "|")
    print("+" + 7*'-' + "+")
        


#print([x for x in JETSTREAM])
#max_row = run_blocks(10, True)
# part 1
max_row, first_row, last_row = run_blocks()
#print_grid(first_row)
#print_grid(last_row)
print(max_row)
# part 2
BIG = 1_000_000_000_000
THE_LOOP = NUM_OF_JETSTREAM*NUM_ROCK_SHAPES
max_row, first_row, last_row = run_blocks(THE_LOOP)
rest_max_row, fr, lr = run_blocks(BIG%THE_LOOP)
print_grid(first_row)
print_grid(last_row)
# max_row = run_blocks(1_000_000_000_000)
# print(max_row)
print(NUM_OF_JETSTREAM)
print(NUM_ROCK_SHAPES)
print(THE_LOOP)
print(THE_LOOP%NUM_OF_JETSTREAM)
print(THE_LOOP%NUM_ROCK_SHAPES)
print(BIG%THE_LOOP)
print(int(BIG/THE_LOOP))
print(max_row)
val = rest_max_row + int(math.floor(BIG/THE_LOOP)) * (max_row)
print(val)







# 1560717471037
# 1560737290682
# 1514285714288