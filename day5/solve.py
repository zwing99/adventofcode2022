import sys
from collections import deque

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

with open("stacks.txt") as fh:
    stacks = [line.rstrip() for line in fh.readlines()]

# part 1
the_stacks = [deque() for i in range(9)]
for line in stacks:
    readpos = 1
    i = 0
    while readpos < len(line) - 1:
        the_item = line[readpos]
        if the_item != ' ':
            the_stacks[i].appendleft(the_item)
        readpos += 4
        i += 1

for line in lines:
    parts = line.split()
    amt = int(parts[1])
    f = int(parts[3])
    t = int(parts[5])
    for i in range(amt):
        the_stacks[t-1].append(the_stacks[f-1].pop())

the_str = ''
for s in the_stacks:
    the_str += s[-1]

print(the_str)

# part 2
the_stacks = [deque() for i in range(9)]
for line in stacks:
    readpos = 1
    i = 0
    while readpos < len(line) - 1:
        the_item = line[readpos]
        if the_item != ' ':
            the_stacks[i].appendleft(the_item)
        readpos += 4
        i += 1

for line in lines:
    parts = line.split()
    amt = int(parts[1])
    f = int(parts[3])
    t = int(parts[5])
    mov = deque()
    for i in range(amt):
        mov.appendleft(the_stacks[f-1].pop())
    the_stacks[t-1].extend(mov)

the_str = ''
for s in the_stacks:
    the_str += s[-1]

print(the_str)
