import sys
from collections import defaultdict

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

ORDER = [1, 2, 3, 4]
LEN_ORDER = len(ORDER)
MOVES = {
    #  check_set, mov
    1: (((0, 1), (1, 1), (-1, 1)), (0, 1)),
    2: (((0, -1), (1, -1), (-1, -1)), (0, -1)),
    3: (((-1, 0), (-1, 1), (-1, -1)), (-1, 0)),
    4: (((1, 0), (1, 1), (1, -1)), (1, 0)),
}
POSITIONS = set()
LEN_LINES = len(lines)
X = 0
Y = 1


def read_positions():
    positions = set()
    for y, line in enumerate(lines):
        # print(line)
        for x, i in enumerate(line):
            p = (x + 1, LEN_LINES - y)
            if i == "#":
                # print(x, y)
                # print(p)
                if p in positions:
                    print("FAIL")
                positions.add(p)
    return positions


def extents(positions):
    max_x, max_y = (-1e99, -1e99)
    min_x, min_y = (1e99, 1e99)
    for elf in positions:
        if elf[X] > max_x:
            max_x = elf[X]
        if elf[X] < min_x:
            min_x = elf[X]
        if elf[Y] > max_y:
            max_y = elf[Y]
        if elf[Y] < min_y:
            min_y = elf[Y]
    return min_x, max_x, min_y, max_y


def print_positions(positions):
    min_x, max_x, min_y, max_y = extents(positions)
    for y in range(max_y + 1, min_y - 2, -1):
        row = ""
        for x in range(min_x - 1, max_x + 2):
            if (x, y) in positions:
                row += "#"
            else:
                row += "."
        print(row)




def run_rounds(positions, num_rounds=10):
    for rnd in range(num_rounds):
        # print(f"-r{rnd}-")
        proposed = defaultdict(list)
        for n, p in enumerate(positions):
            has_neighbor = False
            for u in range(-1, 2):
                for s in range(-1, 2):
                    if (s, u) != (0, 0):
                        # print(s,u)
                        new_p = (p[X] + s, p[Y] + u)
                        if new_p in positions:
                            has_neighbor = True
                            # print("FOUND")
                            break
                if has_neighbor:
                    break
            # print(n, p, has_neighbor)
            if has_neighbor:
                for i in range(LEN_ORDER):
                    check, mov = MOVES[ORDER[(rnd + i) % LEN_ORDER]]
                    can_move = True
                    for c in check:
                        new_p = (p[X] + c[X], p[Y] + c[Y])
                        if new_p in positions:
                            can_move = False
                            break
                    if can_move:
                        new_p = (p[X] + mov[X], p[Y] + mov[Y])
                        proposed[new_p].append(p)
                        # print("propose", p, new_p)
                        break
        if len(proposed) == 0:
            break
        did_move = False
        for prop, origs in proposed.items():
            # print(origs, prop)
            if len(origs) == 1:
                orig = origs[0]
                positions.remove(orig)
                positions.add(prop)
                did_move = True
            else:
                ...
                # print(f'too many: {origs}')
        if not did_move:
            break
        # print(len(positions)
        # print_positions(positions)
    return positions, rnd + 1

print("---pt1---")
positions = read_positions()
positions, rnd = run_rounds(positions)

min_x, max_x, min_y, max_y = extents(positions)
print_positions(positions)
print(f"rounds:{rnd}")
print(max_x, max_y, min_x, min_y)
grid_size = (max_y - min_y + 1) * (max_x - min_x + 1)
empty = grid_size - len(positions)
print(grid_size, empty)

print("---pt2---")
positions = read_positions()
positions, rnd = run_rounds(positions, 1_000_000_000)

min_x, max_x, min_y, max_y = extents(positions)
print_positions(positions)
print(f"rounds: {rnd}")
print(max_x, max_y, min_x, min_y)
grid_size = (max_y - min_y + 1) * (max_x - min_x + 1)
empty = grid_size - len(positions)
print(grid_size, empty)
