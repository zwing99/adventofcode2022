import statistics
import math
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

# part 1
positions = [int(x) for x in lines[0].split(',')]
best_position = int(round(statistics.median(positions)))

fuel = 0
for item in positions:
    fuel += abs(item-best_position)

print (best_position)
print(fuel)

# part 2
positions = [int(x) for x in lines[0].split(',')]
max_val = max(positions)
min_val = min(positions)

min_fuel = 99E9999
for j in range(min_val, max_val+1):
    fuel = 0
    for item in positions:
        amt = abs(item-j)
        for i in range(1, amt+1):
            fuel += i
    print(j, fuel)
    if fuel < min_fuel:
        min_fuel = fuel

print(min_fuel)
