import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

interesting = list(range(20,221,40))
print(interesting)
def cycle_check(cycle, register):
    if cycle in interesting:
        return cycle * register
    return 0

sum = 0
cycles = 0
register = 1
for line in lines:
    if line == 'noop':
        pass
        cycles += 1
        sum += cycle_check(cycles, register)
    else:
        _, x = line.split()
        x = int(x)
        cycles += 1
        sum += cycle_check(cycles, register)
        cycles += 1
        sum += cycle_check(cycles, register)
        register += x

print(sum)


row = []
interesting = list(range(1,241,40))
def draw(cycles, register):
    global row
    if cycles in interesting:
        print("".join(row))
        row = []
    pixel = (cycles) % 40
    if pixel >= register and pixel <= register + 2:
        row += "#"
    else:
        row += " "

cycles = 0
register = 1
for line in lines:
    if line == 'noop':
        pass
        cycles += 1
        draw(cycles, register)
    else:
        _, x = line.split()
        x = int(x)
        cycles += 1
        draw(cycles, register)
        cycles += 1
        draw(cycles, register)
        register += x

print("".join(row))