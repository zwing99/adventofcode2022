fh = open('input.txt')
lines = fh.readlines()

calories = []

accumulator = 0
for line in lines:
    cleanline = line.strip()
    if cleanline == '':
        calories.append(accumulator)
        accumulator = 0
    else:
        accumulator += int(cleanline)

if accumulator != 0:
    calories.append(accumulator)


print(max(calories))
print(calories.index(max(calories))+1)
print()

print(sum(sorted(calories, reverse=True)[:3]))
