import sys
from pprint import pprint
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

segments = []
max_x = 0
min_x = 99E99
max_y = 0
min_y = 99E99
for line in lines:
    segment = []
    for part in line.split(' -> '):
        x, y = [int(i) for i in part.split(',')]
        if x > max_x: max_x = x
        if y > max_y: max_y = y
        if x < min_x: min_x = x
        if y < min_y: min_y = y
        segment.append((x,y))
    segments.append(segment)

# Part 1

def get_direction(a,b):
    d = b - a
    if d == 0:
        return 0
    return int(d/abs(d))

def build_and_fill_grid(min_x, max_x, max_y):
    shift_x = min_x - 1
    grid = []
    for i in range(max_y+2):
        grid.append([0 for j in range(min_x-shift_x,max_x-shift_x+2)])
    # build floor
    grid.append([2 for j in range(min_x-shift_x,max_x-shift_x+2)])

    for segment in segments:
        p1 = segment[0]
        for i in range(1, len(segment)):
            p2 = segment[i]
            p1x, p1y = p1
            p1x -= shift_x
            p2x, p2y = p2
            p2x -= shift_x
            if p1y == p2y: # is vertical
                d = get_direction(p1x, p2x)
                for j in range(0,abs(p2x-p1x)+1):
                    #print(p1x+d*j, p1y)
                    grid[p1y][p1x+d*j] = 2
            elif p1x == p2x: # is horizontal
                d = get_direction(p1y, p2y)
                for j in range(0,abs(p2y-p1y)+1):
                    #print(p1x, p1y+d*j)
                    grid[p1y+d*j][p1x] = 2
            else:
                print('bad')
            p1 = p2
    
    return grid, shift_x

def print_grid(grid):
    print()
    for row in grid:
        print("".join([str(i) for i in row]))


def sand_fall(grid, shift_x, let_fall=False):
    end_state = False
    count = 0
    while not end_state and count < 1E5:
        sand_x, sand_y = 500-shift_x, 0
        fell_off = False
        while True:
            # print(sand_x, sand_y)
            if not let_fall and (sand_x <= min_x - 1 - shift_x or sand_x >= max_x + 1 - shift_x or let_fall or sand_y > max_y + 1):
                fell_off = True
                break 
            if grid[sand_y+1][sand_x] == 0:  # fall down
                sand_y += 1
            elif grid[sand_y+1][sand_x-1] == 0:  # fall down and left
                sand_y += 1
                sand_x -= 1
            elif grid[sand_y+1][sand_x+1] == 0:  # fall down and right
                sand_y += 1
                sand_x += 1
            else:  # end of line
                grid[sand_y][sand_x] = 1
                break
        
        if fell_off:
            break

        count += 1

        # final exit
        if sand_x == 500-shift_x and sand_y == 0:
            break

    return count


# part 1
grid, shift_x = build_and_fill_grid(min_x, max_x, max_y)
print_grid(grid)
count = sand_fall(grid, shift_x)
print_grid(grid)
print(count)


# part 2
shift_x = min_x - 1
grid, shift_x = build_and_fill_grid(min_x-max_y, max_x+ max_y+1, max_y)
print_grid(grid)
count = sand_fall(grid, shift_x, let_fall=True)
print_grid(grid)
print(count)










