import sys
from typing import NamedTuple, DefaultDict, Tuple, List
from collections import defaultdict

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


class Extents(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class Pair(NamedTuple):
    x: int
    y: int


DIRS = {
    "<": Pair(-1, 0),
    ">": Pair(1, 0),
    "^": Pair(0, -1),
    "v": Pair(0, 1),
}
CHOICES = [
    Pair(1, 0),
    Pair(0, 1),
    Pair(0, 0),
    Pair(-1, 0),
    Pair(0, -1),
]
DIRS_R = {v: k for k, v in DIRS.items()}
OPPOSITE_DIR = {
    Pair(-1, 0): Pair(1, 0),
    Pair(1, 0): Pair(-1, 0),
    Pair(0, -1): Pair(0, 1),
    Pair(0, 1): Pair(0, -1),
}

wp_typ = DefaultDict[Pair, List[Pair]]


def parse_grid() -> Tuple[Pair, Pair, Extents, wp_typ]:
    wind_positions: wp_typ = defaultdict(list)
    extents = Extents(1, len(lines[0]) - 2, 1, len(lines) - 2)
    start, end = Pair(0, 0), Pair(0, 0)
    for y, line in enumerate(lines):
        for x, v in enumerate(line):
            if y == 0:
                if v == ".":
                    start = Pair(x, 0)
            elif y == len(lines) - 1:
                if v == ".":
                    end = Pair(x, len(lines) - 1)
            else:
                if v in DIRS:
                    wind_positions[Pair(x, y)].append(DIRS[v])

    return start, end, extents, wind_positions


def next_wind(wind_positions: wp_typ, extents: Extents) -> wp_typ:
    new_winds: wp_typ = defaultdict(list)
    for p, l_dirs in wind_positions.items():
        for d in l_dirs:
            new_p = Pair(p.x + d.x, p.y + d.y)
            if new_p.x > extents.max_x:
                new_p = Pair(extents.min_x, new_p.y)
            elif new_p.x < extents.min_x:
                new_p = Pair(extents.max_x, new_p.y)
            elif new_p.y > extents.max_y:
                new_p = Pair(new_p.x, extents.min_y)
            elif new_p.y < extents.min_y:
                new_p = Pair(new_p.x, extents.max_y)
            new_winds[new_p].append(d)
    return new_winds


def print_winds(wp: wp_typ, extents: Extents):
    se_row = "#" * (extents.max_x - extents.min_x + 3)
    print(se_row)
    for y in range(extents.min_y, extents.max_y + 1):
        row = "#"
        for x in range(extents.min_x, extents.max_x + 1):
            p = Pair(x, y)
            if p in wp:
                if len(wp[p]) == 1:
                    row += DIRS_R[wp[p][0]]
                else:
                    row += f"{len(wp[p])}"
            else:
                row += '.'
        row += "#"
        print(row)
    print(se_row)


def get_winds(
    winds: dict[int, wp_typ], wind_hashs: dict[int, int], extents: Extents, minute: int
) -> wp_typ:
    if minute in wind_positions:
        return winds[minute]
    for i in range(max(winds.keys()) + 1, minute + 1):
        winds[i] = next_wind(winds[i - 1], extents)
        wind_hashes[i] = hash_winds(winds[i])
        # print(f'winds at {i}')
        #print_winds(winds[i], extents)
    return winds[minute]


def hash_winds(wp: wp_typ):
    li = []
    for i, j in wp.items():
        for k in j:
            li.append((i, k))
    return hash(tuple(li))


SHORTEST = 9999999999999999
SEEN = dict()


def dfs(
    m: int,
    pos: Pair,
    winds: dict[int, wp_typ],
    wind_hashes: dict[int, int],
    extents: Extents,
    start: Pair,
    end: Pair,
):
    global SHORTEST, SEEN
    if (pos, wind_hashes[m]) in SEEN:
        # if (pos, m) in SEEN:
        old_m = SEEN[((pos, wind_hashes[m]))]
        if m >= old_m:
            return
    SEEN[(pos, wind_hashes[m])] = m
    #if len(SEEN) % 1000 == 0:
    #    print(len(SEEN))
    # SEEN.add((pos, m)
    shortest_to_end = (end.y - pos.y) + (end.x - pos.x)
    if m + shortest_to_end >= SHORTEST:
        return
    else:
        ...
        #print(f'moar potentail: {m,shortest_to_end}')
    if pos == end:
        SHORTEST = m
        return
    n_winds = get_winds(winds, wind_hashes, extents, m + 1)
    for c in CHOICES:
        c_pos = Pair(pos.x + c.x, pos.y + c.y)
        if c_pos not in n_winds:
            if c_pos == start or c_pos == end:
                dfs(m + 1, c_pos, winds, wind_hashes, extents, start, end)
            elif (
                c_pos.x >= extents.min_x
                and c_pos.x <= extents.max_x
                and c_pos.y >= extents.min_y
                and c_pos.y <= extents.max_y
            ):
                dfs(m + 1, c_pos, winds, wind_hashes, extents, start, end)


import help
help.go(lines)
exit(0)

## part 1
start, end, extents, wind_positions = parse_grid()
winds = {0: wind_positions}
wind_hashes = {0: hash_winds(wind_positions)}
SHORTEST = 9999999999999999
SEEN = dict()
dfs(0, start, winds, wind_hashes, extents, start, end)
print("--pt1--")
print(SHORTEST)

## part 2
# there
print("--pt2--")
s1 = SHORTEST
# back
SHORTEST = 9999999999999999
SEEN = dict()
CHOICES = [
    Pair(-1, 0),
    Pair(0, -1),
    Pair(0, 0),
    Pair(1, 0),
    Pair(0, 1),
]
dfs(s1, end, winds, wind_hashes, extents, end, start)
print(SHORTEST)
s2 = SHORTEST
# there
CHOICES = [
    Pair(1, 0),
    Pair(0, 1),
    Pair(0, 0),
    Pair(-1, 0),
    Pair(0, -1),
]
SHORTEST = 9999999999999999
SEEN = dict()
dfs(s2, start, winds, wind_hashes, extents, start, end)
print(SHORTEST)