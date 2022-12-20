import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

parts = []
for line in lines:
    i, o = line.split('|')
    parts.append((i.strip().split(),o.strip().split()))

known = { 2, 4, 3, 7, }


# part 1
count = 0
for i, o in parts:
    for p in o:
        if len(p) in known:
            count += 1

print(count)

# part 2
nums = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]
nums_map = {
    tuple([s for s in n]): i
    for i, n in enumerate(nums)
}
lens_map = {
    len(n): tuple([s for s in n])
    for n in nums
}
del lens_map[5]

for i, o in parts:
    i_lens_map = {
        len(n): tuple([s for s in n])
        for n in i
    }
    mappings = {}
    for l in known:
        p = i_lens_map[l]
        print(p)
        pm = lens_map[len(p)]
        print(pm)
        mappings.update(dict(zip(p, pm)))
    for j, d in enumerate(reversed(o)):
        dp = tuple([n for n in d])
        print(dp)
        dp = tuple([mappings[n] for n in d])
        print(dp)
        dv = nums_map[dp]

