import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

parts = []
for line in lines:
    i, o = line.split('|')
    parts.append((i.strip().split(),o.strip().split()))

info = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}

count = 0
for i, o in parts:
    if len(o) in info:
        count += info[len(o)]

print(count)