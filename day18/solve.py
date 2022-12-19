import sys
from itertools import chain

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


XYZ = tuple[int, int, int]
X = 0
Y = 1
Z = 2
TOUCHING = "touching"
OPEN = "open"
items: dict[XYZ, dict[str, list[XYZ]]] = {}


def update_extents(key, max_extents, min_extents):
    for i in (X, Y, Z):
        if key[i] > max_extents[i]:
            max_extents[i] = key[i]
        if key[i] < min_extents[i]:
            min_extents[i] = key[i]


def get_ajacent(key):
    return {
        (key[X] + 1, key[Y], key[Z]),
        (key[X] - 1, key[Y], key[Z]),
        (key[X], key[Y] + 1, key[Z]),
        (key[X], key[Y] - 1, key[Z]),
        (key[X], key[Y], key[Z] + 1),
        (key[X], key[Y], key[Z] - 1),
    }


def out_of_bounds(items, max_extents, min_extents):
    rv = []
    for i in items:
        OOO = False
        for j in (X, Y, Z):
            if i[j] > max_extents[j]:
                OOO = True
                break
            if i[j] < min_extents[j]:
                OOO = True
                break
        if not OOO:
            rv.append(i)

    return set(rv)


max_extents = [0, 0, 0]
min_extents = [1000, 1000, 1000]
for line in lines:
    key = tuple([int(i) for i in line.split(",")])
    update_extents(key, max_extents, min_extents)
    ajacent = get_ajacent(key)
    items[key] = {TOUCHING: [], OPEN: []}
    for a in ajacent:
        if a in items:
            items[a][TOUCHING].append(key)
            items[a][OPEN].remove(key)
            items[key][TOUCHING].append(a)
        else:
            items[key][OPEN].append(a)


# pt1
print(sum([len(i[OPEN]) for i in items.values()]))

# pt2
voids: list[set[XYZ]] = []

used = set(items.keys())
known_open = set(chain(*[i[OPEN] for i in items.values() if len(i[OPEN]) > 0]))


def all_empty():
    for x in range(min_extents[X] - 1, max_extents[X] + 2):
        for y in range(min_extents[Y] - 1, max_extents[Y] + 2):
            for z in range(min_extents[Z] - 1, max_extents[Z] + 2):
                if (x, y, z) not in used:
                    yield (x, y, z)


voids: list[set[XYZ]] = []
for key in all_empty():
    ajacent = get_ajacent(key)
    ajacent -= used
    added = False
    for void in voids:
        if key in void:
            added = True
            break
        elif ajacent & void:
            void.add(key)
            added = True
            break

    if not added:
        void = set()
        void.add(key)
        voids.append(void)

len_voids = 0
while len(voids) != len_voids:
    len_voids = len(voids)
    new_voids = []
    for v in voids:
        added = False
        for nv in new_voids:
            for i in v:
                ajacent = get_ajacent(i)
                ajacent -= used
                added = False
                if i in nv:
                    added = True
                    break
                elif ajacent & void:
                    added = True
                    break
            if added:
                nv.update(v)
                break
        if not added:
            new_voids.append(v)
    voids = new_voids


total = 0
all_voids = set(chain(*voids[1:]))
for i in items.values():
    for o in i[OPEN]:
        if o not in all_voids:
            total += 1

print(len(voids)-1)
print(total)
