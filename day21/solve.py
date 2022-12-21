import re
import sys
import z3 
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

monks = {}

for line in lines:
    name, formula = line.split(": ")
    is_int = True
    try:
        v = int(formula)
    except ValueError:
        is_int = False
    if is_int:
        monks[name] = v
    else:
        monks[name] = formula.split()


def get_value(name="root"):
    v = monks[name]
    if isinstance(v, int):
        return v
    else:
        a = get_value(v[0])
        b = get_value(v[2])
        if v[1] == '+':
            c = a + b
        elif v[1] == '-':
            c = a - b
        elif v[1] == '*':
            c = a * b
        elif v[1] == '/':
            c = a // b
        return c

# part 1
print(get_value())

humn = z3.Int('z3')
monks["humn"] = humn

def get_equation(name="root"):
    v = monks[name]
    if name == "root":
        sideA = get_equation(v[0])
        print(sideA)
        sideB = get_equation(v[2])
        print(sideB)
        return sideA == sideB
    else:
        if isinstance(v, int):
            return v
            return f"{{{name}}}"
        elif isinstance(v, list):
            a = get_equation(v[0])
            b = get_equation(v[2])
            #return ({sideA} {v[1]} {sideB}
            if v[1] == '+':
                c = a + b
            elif v[1] == '-':
                c = a - b
            elif v[1] == '*':
                c = a * b
            elif v[1] == '/':
                c = a / b
            return c
        else:
            return v


a = get_equation()
print(a)
print(z3.solve(a))