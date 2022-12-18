#from tqdm import tqdm
from copy import deepcopy
import sys
import math
from collections import deque
import functools
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


WIDTH = 7
HEIGHT = 50
default_prior = tuple([tuple([1 for x in range(WIDTH)])])
THE_LOOP = NUM_OF_JETSTREAM*NUM_ROCK_SHAPES


@functools.cache
def run_blocks(total_rocks=2022, prior=default_prior):
    #print(total_rocks, hash(initial), last_max)
    grid = [list(item) for item in prior]
    init_val = len(grid)
    max_row = init_val
    while len(grid) < HEIGHT:
        grid.append([0 for x in range(WIDTH)])
    jet_count = 0
    for rock_num in range(total_rocks):
        rock = get_next_rock(rock_num, max_row)
        max_y = max([c[Y] for c in rock]) + 1
        for i in range(max_row + 1, max_y +1):
            for x in range(WIDTH):
                grid[(i)%HEIGHT][x] = 0
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
                for coord in rock:
                    coord[X] += jet_dir
            else:
                ...
            # drop rock
            ###############################################################
            # can drop
            can_drop = True
            for coord in rock:
                new_x, new_y = coord[X], coord[Y] - 1
                if grid[(new_y)%HEIGHT][new_x] != 0:
                    can_drop = False
                    break
            # done with rock
            if not can_drop:
                break
            # drop rock
            for coord in rock:
                coord[Y] -= 1
        # set rock
        ###############################################################
        max_y = max([c[Y] for c in rock]) + 1
        if max_y > max_row:
            max_row = max_y
        for coord in rock:
            grid[(coord[Y]) % HEIGHT][coord[X]] = 1
        None

    new_grid = []
    moar = max_row + 1
    while sum(grid[moar%HEIGHT]) == 0:
        moar += 1
    for i in range(moar, moar+int(HEIGHT/2)):
        asdf = grid[i%HEIGHT]
        new_grid.append(asdf)
    new_grid = tuple([tuple(item) for item in new_grid])
    max_row -= init_val
    return max_row, new_grid


def convert(x):
    if x == 0:
        return '.'
    elif x == 1:
        return '#'
    return ' '

def print_grid(grid):
    print("+" + 7*'-' + "+")
    for i in range(len(grid)-1, -1, -1):
    #for i in range(len(grid)):
        print("|" + "".join([convert(x) for x in grid[i]]) + "|")
    print("+" + 7*'-' + "+")
        


# part 1
max_row, _ = run_blocks(10)
#print_grid(_)
max_row, _ = run_blocks()
#print_grid(_)
print(max_row)
print()
# part 2
BIG = 1_000_000_000_000
print(THE_LOOP)
steps = int(BIG/THE_LOOP)
#print(steps)
rest = BIG % THE_LOOP
total = 0
max_row = 0
offset = 0
previous = deepcopy(default_prior)
#print(max_row)
previous_p = None
#for i in tqdm(range(steps)):
for i in range(steps):
    previous_p = previous
    max_row, previous = run_blocks(THE_LOOP, previous)
    #print_grid(previous)
    total += max_row
    test, _ = run_blocks(THE_LOOP*(i+1))
    #print((i+1), total, test)
    if total != test:
        print("BAD")
        print_grid(_)
        print_grid(previous)
        print((i+1), total, test)
        exit(1)
    if i >= 100:
        break

max_row, previous = run_blocks(rest, previous, offset)
total += max_row

print(total)









# 1560717471037
# 1560737290682
# 1514285714288
# 1560658012114
# 1560899790897
# 1560935466164
# 1560915646636
# 1559121989969