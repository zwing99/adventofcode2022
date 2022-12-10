import sys
from collections import defaultdict
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


def get_dir(a,b):
    if a == b:
        return 0
    return int((b-a)/abs(b-a))

# part 1
points = defaultdict(lambda: 0)
for line in lines:
    p1, p2 = line.split(' -> ')
    p1 = tuple(int(i) for i in p1.split(','))
    p2 = tuple(int(i) for i in p2.split(','))
    # is horizonal or verticle
    if p1[0] == p2[0]:
        dirt = get_dir(p1[1],p2[1])
        for i in range(0,abs(p2[1]-p1[1])+1):
            to_add = (p1[0], p1[1] + dirt*i)
            points[to_add] += 1
    elif p1[1] == p2[1]:
        dirt = get_dir(p1[0],p2[0])
        for i in range(0,abs(p2[0]-p1[0])+1):
            to_add = (p1[0] + dirt*i, p1[1])
            points[to_add] += 1

print(len([p for p in points if points[p] >= 2]))
#print([p for p in points if points[p] >= 2])
#print({p:c for p,c in points.items()})

# part 2
points = defaultdict(lambda: 0)
for line in lines:
    p1, p2 = line.split(' -> ')
    p1 = tuple(int(i) for i in p1.split(','))
    p2 = tuple(int(i) for i in p2.split(','))
    dirt_y = get_dir(p1[1],p2[1])
    dirt_x = get_dir(p1[0],p2[0])
    cnt = max(abs(p2[1] - p1[1]),abs(p2[0]-p1[0]))
    for i in range(0,cnt+1):
        to_add = (p1[0] + dirt_x*i, p1[1] + dirt_y*i)
        points[to_add] += 1

print(len([p for p in points if points[p] >= 2]))