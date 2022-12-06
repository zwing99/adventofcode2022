import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

data = lines[0]

# part1
last3 = data[:3]
for i, part in enumerate(data[2:]):
    the_set = set(last3)
    the_set.add(part)
    if len(the_set) == 4:
        print(the_set)
        print("found")
        break
    last3 = last3[1:] + part

print(i+3)

# part2
last3 = data[:13]
for i, part in enumerate(data[12:]):
    the_set = set(last3)
    the_set.add(part)
    if len(the_set) == 14:
        print(the_set)
        print("found")
        break
    last3 = last3[1:] + part

print(i+13)
