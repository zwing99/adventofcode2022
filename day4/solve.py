import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

def make_set(e):
    n1, n2 = [int(v) for v in e.split('-')]
    return set(range(n1,n2+1))


with open(filename) as fh:
    lines = [[make_set(e) for e in line.strip().split(',')] for line in fh.readlines()]

# part 1
count = 0
for e1,e2 in lines:
    common_sections = e1 & e2
    if len(e1) == len(common_sections):
        count += 1
    elif len(e2) == len(common_sections):
        count += 1

print(count)


# part 2
count = 0
for e1,e2 in lines:
    common_sections = e1 & e2
    if len(common_sections) > 0:
        count += 1

print(count)
