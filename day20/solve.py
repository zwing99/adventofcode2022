import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

class Wrap:
    def __init__(self, v: int) -> None:
        self.v = v


all: list[Wrap] = [Wrap(int(i)) for i in lines]
all_p2: list[Wrap] = all[:]

all_iter: list[Wrap] = all[:]
l = len(all_iter)

#print([i.v for i in all])
for item in all_iter:
    if item.v == 0:
        continue
    index = all.index(item)
    all.pop(index)
    index_shift = (index + item.v) % (l - 1)
    orig = index_shift

    all.insert(index_shift, item)

#print([i.v for i in all])

zero = [a for a in all if a.v == 0 ][0]
index_z = all.index(zero)

i = all[(index_z+1000)%l].v
j = all[(index_z+2000)%l].v
k = all[(index_z+3000)%l].v

print(i,j,k,i+j+k)


KEY = 811589153
for i in all_iter:
    i.v = i.v * KEY
#print([i.v for i in all_p2])
# part 2
for z in range(10):
    for item in all_iter:
        if item.v == 0:
            continue
        index = all_p2.index(item)
        all_p2.pop(index)
        index_shift = (index + item.v) % (l - 1)
        orig = index_shift
        
        all_p2.insert(index_shift, item)
    #print(f"{z+1}: {[i.v for i in all_p2]}")

zero = [a for a in all_p2 if a.v == 0 ][0]
index_z = all_p2.index(zero)

i = all_p2[(index_z+1000)%l].v # * KEY
j = all_p2[(index_z+2000)%l].v # * KEY
k = all_p2[(index_z+3000)%l].v # * KEY

print(i,j,k,i+j+k)


# 442 L
# 5562 H