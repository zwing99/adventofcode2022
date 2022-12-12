import sys
import math
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

fish_counts = {i:0 for i in range(0,9)}
for x in lines[0].split(","):
    fish_counts[int(x)] += 1

# part 1
for j in range(80):
    new_counts = {i:0 for i in range(0,9)}
    for i in range(0,9):
        if i > 0:
            new_counts[i-1] += fish_counts[i]
        else:
            new_counts[6] += fish_counts[i]
            new_counts[8] += fish_counts[i]
    fish_counts = new_counts

print(sum(fish_counts.values()))

# part 2
fish_counts = {i:0 for i in range(0,9)}
for x in lines[0].split(","):
    fish_counts[int(x)] += 1

for j in range(256):
    new_counts = {i:0 for i in range(0,9)}
    for i in range(0,9):
        if i > 0:
            new_counts[i-1] += fish_counts[i]
        else:
            new_counts[6] += fish_counts[i]
            new_counts[8] += fish_counts[i]
    fish_counts = new_counts

print(sum(fish_counts.values()))
