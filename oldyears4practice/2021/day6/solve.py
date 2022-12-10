import sys
import math
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

fishes = [int(x) for x in lines[0].split(",")]
for i in range(80):
    new_list = []
    extended = []
    for fish in fishes:
        if fish > 0:
            new_list.append(fish-1)
        else:
            new_list.append(6)
            extended.append(8)
    fishes = new_list + extended

print(len(fishes))

fishes = [int(x) for x in lines[0].split(",")]
total = 0
for fish in fishes:
    asdf = [fish]
    for i in range(80):
        new_list = []
        extended = []
        for f in asdf:
            if f > 0:
                new_list.append(f-1)
            else:
                new_list.append(6)
                extended.append(8)
        asdf = new_list + extended
        print(len(asdf))
    print(fish)
    print(len(asdf))
    total += len(asdf)
print(total)

exit(0)
            
# part 2
fishes = [int(x) for x in lines[0].split(",")]
for i in range(256):
    print (i)
    new_list = []
    extended = []
    for fish in fishes:
        if fish > 0:
            new_list.append(fish-1)
        else:
            new_list.append(6)
            extended.append(8)
    fishes = new_list + extended

print(len(fishes))