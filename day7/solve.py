import sys
from pprint import pprint
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

the_stuff = dict()

path = []
i = 0
while i < len(lines):
    line = lines[i]
    if line[0] == '$':
        i += 1
        print(f"is command: {line}")
        cmd = line.split(maxsplit=1)[1]
        if cmd == 'cd /':
            print("is chddir")
            path = []
        elif cmd[:2] == 'cd':
            print("is chddir")
            the_dir = cmd.split()[1]
            if the_dir == '..':
                if len(path) != 0:
                    path.pop()
                else:
                    print('no path to ..')
            else:
                d = the_stuff
                for part in path:
                    d = d[part]
                if the_dir not in d:
                    d[the_dir] = {}
                path.append(the_dir)
                print(path)
        elif cmd == 'ls':
            print("is listing")
            while i < len(lines):
                line = lines[i]
                if line[0] == '$':
                    print(f"reseting: {line}")
                    break
                print(line)
                line_parts = line.split()
                if line_parts[0] == 'dir':
                    print("is dir")
                    d = the_stuff
                    for part in path:
                        d = d[part]
                    d[line_parts[1]] = {}
                else:
                    print("is file")
                    size = line_parts[0]
                    file_name = line_parts[1]
                    d = the_stuff
                    for part in path:
                        print(f"put in {part}")
                        d = d[part]
                    d[file_name] = int(size)
                i += 1
    else:
        print('bad')
    print()


dir_sizes = {}

def calc_size(n, d):
    size = 0
    for dn, s in d.items():
        if isinstance(s, dict):
            size += calc_size(f"{n}/{dn}", s)
        else:
            size += s
    dir_sizes[n] = size
    return size

calc_size('/', the_stuff)

# part1
total = 0
for d, size in dir_sizes.items():
    if size <= 100000:
        total += size

print(total)
print()
        


# part2
dir_sizes_items = sorted(dir_sizes.items(), reverse=True, key=lambda x: x[1])

used = dir_sizes_items[0][1]
total = 70000000
free = total - used
print(free)

needed = 30000000 - free
print(needed)

last_size = 0
for n, s in dir_sizes_items:
    if s > needed:
        last_size = s
    else:
        break
print(last_size)
    




