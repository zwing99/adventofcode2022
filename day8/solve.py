from pprint import pprint
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]
    
grid = []
for line in lines:
    row = []
    for item in line:
        row.append(item)
    grid.append(row)

#pprint(grid)

width = len(grid[0])
height = len(grid)

# part 1
count = 0
for i in range(1, width - 1):
    for j in range(1, height - 1):
        is_vis = False
        my_tree = grid[j][i]

        # look left 
        see_left = True
        for z in range(i-1, -1, -1):
            t = grid[j][z]
            if t >= my_tree:
                see_left = False
                break

        # look right 
        see_right = True
        for z in range(i+1, width):
            t = grid[j][z]
            if t >= my_tree:
                see_right = False
                break

        # look up 
        see_up = True
        for z in range(j-1, -1, -1):
            t = grid[z][i]
            if t >= my_tree:
                see_up = False
                break

        # look down 
        see_down = True
        for z in range(j+1, width):
            t = grid[z][i]
            if t >= my_tree:
                see_down = False
                break

        is_vis = any([see_left, see_right, see_up, see_down])
        if is_vis:
            count += 1

count += (2* height) + (2 * (width - 2))
print(count)

# part 2
max_score = 0
for i in range(1, width - 1):
    for j in range(1, height - 1):
        my_tree = grid[j][i]

        # look left 
        left = 1
        for z in range(i-1, -1, -1):
            t = grid[j][z]
            if t >= my_tree:
                break
            elif z != 0:
                left += 1

        # look right 
        right = 1
        for z in range(i+1, width):
            t = grid[j][z]
            if t >= my_tree:
                break
            elif z != width -1:
                right += 1

        # look up 
        up = 1
        for z in range(j-1, -1, -1):
            t = grid[z][i]
            if t >= my_tree:
                break
            elif z != 0:
                up += 1

        # look down 
        down = 1
        for z in range(j+1, width):
            t = grid[z][i]
            if t >= my_tree:
                break
            elif z != height -1:
                down += 1

        tree_score = left * right * up * down
        if tree_score > max_score:
            print(up,left,down,right)
            max_score = tree_score

print(max_score)
