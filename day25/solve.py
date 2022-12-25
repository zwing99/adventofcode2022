import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

MAP = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}
MAP_R = {v: k for k, v in MAP.items()}


total = 0
for line in lines:
    v_line = 0
    for i in range(len(line)):
        index = (i + 1) * -1
        amt = 5**i
        v_line += amt * MAP[line[index]]
    # print(line, ",", v_line)
    total += v_line


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def to_weird(n):
    v = numberToBase(n, 5)
    new = []
    if v[0] > 2:
        new.append(1)
        new.append(v[0] - 5)
    else:
        new.append(v[0])
    for i in v[1:]:
        if i > 2:
            for z in range(len(new)):
                z = -1 * (z + 1)
                if new[z] + 1 <= 2:
                    new[z] += 1
                    break
                else:
                    new[z] = -2
            new.append(i - 5)
        else:
            new.append(i)

    print(new)
    return "".join([MAP_R[n] for n in new])


print(to_weird(total))


# 28927640190471
    