from tqdm import tqdm
from copy import deepcopy
import sys
import math
from collections import deque
import functools

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
CNT = int(sys.argv[2]) if len(sys.argv) > 2 else 100

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


def jet_direction(jetchar):
    if jetchar == "<":
        return -1
    elif jetchar == ">":
        return 1
    else:
        print("bad")
        exit(1)


JETSTREAM = [jet_direction(x) for x in lines[0]]
NUM_OF_JETSTREAM = len(JETSTREAM)
ROCK_SHAPES = [
    [[2, 0], [3, 0], [4, 0], [5, 0]],
    [[3, 2], [2, 1], [3, 1], [4, 1], [3, 0]],
    [[4, 2], [4, 1], [2, 0], [3, 0], [4, 0]],
    [[2, 3], [2, 2], [2, 1], [2, 0]],
    [[2, 1], [3, 1], [2, 0], [3, 0]],
]
NUM_ROCK_SHAPES = len(ROCK_SHAPES)
X = 0
Y = 1


def get_next_rock(rock_num, max_row):
    rock = deepcopy(ROCK_SHAPES[rock_num % NUM_ROCK_SHAPES])
    for coord in rock:
        coord[Y] += max_row + 3
    return rock


WIDTH = 7
HEIGHT = CNT
default_prior = tuple([tuple([1 for x in range(WIDTH)])])
THE_LOOP = NUM_OF_JETSTREAM * NUM_ROCK_SHAPES


def run_blocks(
    rocks_to_drop=2022,
    current_rock_num=0,
    max_row=1,
    jet_count=0,
    prior=default_prior,
):
    grid = [list(item) for item in prior]
    while len(grid) < HEIGHT:
        grid.append([0 for x in range(WIDTH)])
    for rock_num in range(current_rock_num, current_rock_num + rocks_to_drop):
        rock = get_next_rock(rock_num, max_row)
        max_y = max([c[Y] for c in rock]) + 1
        for i in range(max_row + 1, max_y + 1):
            for x in range(WIDTH):
                grid[(i) % HEIGHT][x] = 0
        while True:
            # shift rock
            ###############################################################
            jet_dir = JETSTREAM[jet_count % NUM_OF_JETSTREAM]
            jet_count += 1
            # can shift
            can_shift = True
            for coord in rock:
                new_x, new_y = coord[X] + jet_dir, coord[Y]
                if new_x < 0 or new_x >= WIDTH:
                    can_shift = False
                    break
                elif grid[(new_y) % HEIGHT][new_x] != 0:
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
                if grid[(new_y) % HEIGHT][new_x] != 0:
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
        if rock_num % 1000 == 0:
            ...
            # print(rock_num)

    new_grid = tuple([tuple(item) for item in grid])
    return max_row, new_grid, rock_num + 1, jet_count


def convert(x):
    if x == 0:
        return "."
    elif x == 1:
        return "#"
    return " "


def print_grid(grid):
    print("+" + 7 * "-" + "+")
    for i in range(len(grid) - 1, -1, -1):
        # for i in range(len(grid)):
        print("|" + "".join([convert(x) for x in grid[i]]) + "|")
    print("+" + 7 * "-" + "+")


# part 1
max_row, _, _, _ = run_blocks()
print(max_row - 1)
print()

# part 2
max_row = 1
prior_max_row = 1
rock_num = 0
jet_count = 0
new_grid = default_prior

for i in range(max(NUM_OF_JETSTREAM * 3, 10_000)):
    max_row, new_grid, rock_num, jet_count = run_blocks(
        1, rock_num, max_row, jet_count, new_grid
    )
    #print(rock_num % 5, max_row - prior_max_row, hash(new_grid))
    prior_max_row = max_row

cache = set()
cache_l = list()
j = 0
prior_grid = None
for i in range(max(NUM_OF_JETSTREAM * 10, 10_000)):
    max_row, new_grid, rock_num, jet_count = run_blocks(
        1, rock_num, max_row, jet_count, new_grid
    )
    c = (rock_num % 5, max_row - prior_max_row, jet_count % NUM_OF_JETSTREAM, hash(new_grid))
    if c not in cache:
        cache.add(c)
        cache_l.append(c)
    else:
        break
    prior_max_row = max_row
    prior_grid = new_grid


len_of_cache = len(cache)
sum_of_cache = sum([c[1] for c in cache])

BIG = 1_000_000_000_000
remaining = BIG - rock_num
#print(f"remaining:{remaining}")
num_times = remaining // len_of_cache
#print(f"num_times:{num_times}")
max_row += num_times * sum_of_cache
rock_num += len_of_cache * num_times
now_remaining = BIG - rock_num
#print(f"now_remaining:{now_remaining}")

rest = cache_l[1:1+now_remaining]
rest_sum = sum([c[1] for c in rest])
print(max_row+rest_sum-1)