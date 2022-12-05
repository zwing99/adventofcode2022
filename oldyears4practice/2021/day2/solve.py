import sys
from operator import add
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

def parse(line):
    cmd, amt = line.split()
    amt = int(amt)
    if cmd == 'forward':
        return (amt,0)
    elif cmd == 'up':
        return (0,-1*amt)
    elif cmd == 'down':
        return (0,amt)

with open(filename) as fh:
    lines = [parse(line.strip()) for line in fh.readlines()]
    

# part 1
where_i_am = (0,0)
for line in lines:
    where_i_am = tuple(map(add,line,where_i_am))

print(where_i_am)
print(where_i_am[0]*where_i_am[1])


# part 2
where_i_am = (0,0)
aim = 0
for line in lines:
    if line[1] != 0:
        aim += line[1]
    else:
        amt = (line[0],line[0]*aim)
        where_i_am = tuple(map(add,amt,where_i_am))

print(where_i_am)
print(where_i_am[0]*where_i_am[1])
