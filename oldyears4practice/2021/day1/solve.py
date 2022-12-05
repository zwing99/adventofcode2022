import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [int(line.strip()) for line in fh.readlines()]

# part 1
last = lines[0]
count = 0
for line in lines[1:]:
    if line > last:
        count += 1
    last = line

print(count)

# part 2
last = sum(lines[0:3])
count = 0
for i in range(1,len(lines)-2):
    this = sum(lines[i:i+3])
    if this > last:
        count += 1
    last = this

print(count)
