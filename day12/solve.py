import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

grid = []
counts = []
for line in lines:
    part = []
    count = []
    for v in line:
        part.append(v)
        count.append(0)
    grid.append(part)
    counts.append(count)

xmax = len(grid[0])
ymax = len(grid)

for i in range(xmax):
    for j in range(ymax):
        if grid[j][i] == 'S':
            start = (i,j)
            grid[j][i] = 0
        elif grid[j][i] == 'E':
            end = (i,j)
            grid[j][i] = 27 
        else:
            grid[j][i] = ord(grid[j][i]) - ord('a') + 1

#print(grid)
#print(start, end)


# algorithm: https://en.wikipedia.org/wiki/Pathfinding#Sample_algorithm

queue = {end: 0}

def check_cell(q, x1,y1,v,c):
    #print(x1,y1)
    cell_v = grid[y1][x1]

    # cant go this way
    #print("cell",cell_v, v)
    if cell_v - v < -1:
        return 

    # is aleady in queue
    if (x1,y1) in q:
        current_c = q[(x,y)]
        if (c < current_c):
            print("oops")
            print(x1,y1,v,c,current_c)
            exit(1)
        return

    q[(x1,y1)] = c

prior_len = 0
while len(queue) > prior_len:
    prior_len = len(queue)
    current_keys = list(queue.keys())
    for item in current_keys:
        x,y = item
        c = queue[(x,y)]
        new_c = c + 1
        v = grid[y][x]
        if y < ymax - 1: # can look up
            #print('up')
            check_cell(queue,x,y+1,v,new_c)
        if y > 0: # can look down
            #print('down')
            check_cell(queue,x,y-1,v,new_c)
        if x < xmax - 1: # can look right
            #print('right')
            check_cell(queue,x+1,y,v,new_c)
        if x > 0: # can look left
            #print('left')
            check_cell(queue,x-1,y,v,new_c)
    #print(len(queue), prior_len)

#part 1
x,y = start
print(queue[start])

#part 2
shortest = 99E99
for i in range(xmax):
    for j in range(ymax):
        if grid[j][i] == 1: # a
            if (i,j) in queue:
                v = queue[(i,j)]
                if v < shortest:
                    shortest = v

print(shortest)