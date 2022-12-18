import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


items: dict[tuple[int, int, int], int] = {}

X = 0
Y = 1
Z = 2

for line in lines:
    key = tuple([int(i) for i in line.split(",")])
    ajacent = [
        (key[X]+1,key[Y],key[Z]),
        (key[X]-1,key[Y],key[Z]),
        (key[X],key[Y]+1,key[Z]),
        (key[X],key[Y]-1,key[Z]),
        (key[X],key[Y],key[Z]+1),
        (key[X],key[Y],key[Z]-1),
    ]
    items[key] = 6
    for a in ajacent:
        if a in items:
            items[a] -= 1
            items[key] -= 1

print(sum(items.values()))