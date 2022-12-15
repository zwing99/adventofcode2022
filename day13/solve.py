import json
import sys
from functools import cmp_to_key
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

stuff = []
for i in range(int(len(lines)/3)):
    left = json.loads(lines[3*i+1])
    right = json.loads(lines[3*i+2])
    stuff.append((left,right))

def test_it(left,right):
    #print(f"L: {left}")
    #print(f"R: {right}")
    for i, l_item in enumerate(left):
        if i >= len(right):
            return 'F'
        r_item = right[i]
        if isinstance(l_item, int) and isinstance(r_item, int):
            #print("ints")
            if l_item < r_item:
                return 'T'
            elif l_item > r_item:
                return 'F'
        elif isinstance(l_item, list) and isinstance(r_item, list):
            v = test_it(l_item, r_item)
            if v in ('T', 'F'):
                return v
        elif isinstance(l_item, int):
            v = test_it([l_item], r_item)
            if v in ('T', 'F'):
                return v
        elif isinstance(r_item, int):
            v = test_it(l_item, [r_item])
            if v in ('T', 'F'):
                return v
    if len(left) < len(right):
        return "T"
    return "C"

# part 1
count = 0
for i, (left, right) in enumerate(stuff):
    #print(i+1)
    v = test_it(left,right)
    #print(v)
    if v in ("C","T"):
        count += i + 1
        #print(i+1)
    #print()

print(count)

# part 2
all_packets = []
for left,right in stuff:
    all_packets.append(left)
    all_packets.append(right)

all_packets.append([[2]])
all_packets.append([[6]])

def compare_it(l,r):
    v = test_it(l,r)
    if v == 'T':
        return -1
    if v == 'F':
        return 1
    if v == 'C':
        return 0

all_packets.sort(key=cmp_to_key(compare_it))

#for p in all_packets:
#    print(p)

i = all_packets.index([[2]]) + 1
j = all_packets.index([[6]]) + 1
print (i)
print (j)

print(i*j)





# 6373
# 4306