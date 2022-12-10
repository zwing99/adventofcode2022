import sys
from operator import add
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

numbers = len(lines[0])
total_num = len(lines)

# part 1
all_nums = [0 for i in range(total_num)]
for line in lines:
    line = [int(x) for x in line]
    all_nums = list(map(add,line,all_nums))

gamma = ''
epsil = ''
for num in all_nums:
    if num > total_num / 2:
        digit_g= '1'
        digit_e= '0'
    else:
        digit_g = '0'
        digit_e = '1'

    gamma += digit_g
    epsil += digit_e
    
print(gamma)
print(epsil)

exec(f'g = 0b{gamma}')
exec(f'e = 0b{epsil}')

print(g)
print(e)
print(g*e)
print()
    
# part 2
items_left = lines[:]
for i in range(numbers):
    zeros = 0
    ones = 0
    for item in items_left:
        if item[i] == '0':
            zeros += 1
        elif item[i] == '1':
            ones += 1
    if zeros > ones:
        items_left = [item for item in items_left if item[i] == '0']
    elif ones >= zeros:
        items_left = [item for item in items_left if item[i] == '1']
    if len(items_left) == 1:
        break 

exec(f'oxy = 0b{items_left[0]}')
print(oxy)

items_left = lines[:]
for i in range(numbers):
    zeros = 0
    ones = 0
    for item in items_left:
        if item[i] == '0':
            zeros += 1
        elif item[i] == '1':
            ones += 1
    if zeros <= ones:
        items_left = [item for item in items_left if item[i] == '0']
    elif ones < zeros:
        items_left = [item for item in items_left if item[i] == '1']
    if len(items_left) == 1:
        break 

exec(f'co2 = 0b{items_left[0]}')
print(co2)
print(oxy*co2)