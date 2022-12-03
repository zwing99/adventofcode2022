import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

def split_up(line):
    half = int(len(line)/2)
    p1 = set(line[:half])
    p2 = set(line[half:])
    return p1,p2

def priority(ch):
    if ch.islower():
        return ord(ch) - ord('a') + 1
    elif ch.isupper():
        return ord(ch) - ord('A') + 27

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

# part 1
total = 0
for line in lines:
    upper, lower = split_up(line)
    common = upper & lower
    priorities = sum([priority(c) for c in common])
    total += priorities
    
print(total)

# part 2
total = 0
i = 0
by_threes = int(len(lines))/3
while i < by_threes: 
    next_three = lines[3*i:3*i+3]
    i += 1
    common_item = set(next_three[0]) & set(next_three[1]) & set(next_three[2])
    p = sum([priority(c) for c in common_item])
    total += p

print(total)
