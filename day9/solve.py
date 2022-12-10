import sys
import math
from dataclasses import dataclass
import gnuplotlib as gp
import numpy as np
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


@dataclass
class Point:
    x: int
    y: int
    
    def coord(self):
        return (self.x,self.y)


def distance(a, b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)


def are_adjacent(a, b):
    if distance(a, b) < 1.5:
        return True
    return False


def get_single(x):
    if x == 0:
        return 0
    return int(x / abs(x))



# Part 1
h = Point(0,0)
t = Point(0,0)
tail_positions = set()
tail_positions.add(t.coord())


for line in lines:
    cmd, amt = line.split()
    amt = int(amt) 
    for i in range(amt):
        if cmd == 'R':
            h.x += 1
        elif cmd == 'L':
            h.x += -1
        elif cmd == 'U':
            h.y += 1
        elif cmd == 'D':
            h.y += -1
        else:
            print('bad')

        # are not ajacent
        if not are_adjacent(h,t):
            x_move = get_single(h.x - t.x)
            y_move = get_single(h.y - t.y)
            #print(h,t)
            #print(x_move, y_move)
            t.x += x_move
            t.y += y_move
            #print(h,t)
            #print()

        tail_positions.add(t.coord())


#print(tail_positions)
print(len(tail_positions))


# Part 2
rope = [Point(0,0) for i in range(10)]
h = Point(0,0)
t = Point(0,0)
tail_positions = list()
tail_positions.append(rope[9].coord())


for line in lines:
    cmd, amt = line.split()
    amt = int(amt) 
    for i in range(amt):
        if cmd == 'R':
            rope[0].x += 1
        elif cmd == 'L':
            rope[0].x += -1
        elif cmd == 'U':
            rope[0].y += 1
        elif cmd == 'D':
            rope[0].y += -1
        else:
            print('bad')

        # are not ajacent
        for i in range(1,len(rope)):
            c = rope[i]
            p = rope[i-1]
            while not are_adjacent(c,p):
                #print(f"distance:{distance(c,p)}")
                #if distance(c,p) > 2:
                #    print(c,p)
                #    exit(1)
                x_move = get_single(p.x - c.x)
                y_move = get_single(p.y - c.y)
                #print(h,t)
                #print(x_move, y_move)
                c.x += x_move
                c.y += y_move
                #print(h,t)
                #print()
                tail_positions.append(rope[9].coord())


print(len(set(tail_positions)))

x_s = np.array([p[0] for p in tail_positions])
y_s = np.array([p[1] for p in tail_positions])

gp.plot( (x_s, y_s),
      _with    = 'points',
      terminal = 'dumb 100,50',
      unset    = 'grid')
