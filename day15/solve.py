import sys
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

target = 2000000 if filename == 'input.txt' else 10

def parse_coord(coord):
    x, y = coord.split(",")
    x = int(x.split('=')[1])
    y = int(y.split('=')[1])
    return x,y

def mdistance(b, a):
    return abs(b[0]-a[0])+abs(b[1]-a[1])

ymin = 99E99
ymax = -99E99
xmin = 99E99
xmax = -99E99
max_distance = 0
sensors = []
beacons = []
distances = []
for line in lines:
    line = line[9:]
    sensor, beacon = [parse_coord(p) for p in line.split(': closest beacon is at ')]
    distance = mdistance(sensor, beacon)
    #print(sensor, beacon)
    for c in (sensor, beacon):
        if c[0] > xmax:
            xmax = c[0]
        if c[0] < xmin:
            xmin = c[0]
        if c[1] > ymax:
            ymax = c[1]
        if c[1] < ymin:
            ymin = c[1]
    if distance > max_distance:
        max_distance = distance
    sensors.append(sensor)
    distances.append(distance)
    beacons.append(beacon)

#print(sensors)
#print(beacons)
print(xmin,xmax,ymin,ymax)
#print(max_distance)

def part1():
    count = 0
    for x in range(xmin-max_distance, xmax+max_distance+1):
        y = target
        #print(x,y)
        if (x ,y) in sensors or (x ,y) in beacons:
            #print('is beacon or sensor')
            continue
        for (sx ,sy), d in zip(sensors, distances):
            target_distance = mdistance((sx,sy),(x,y))
            if target_distance <= d:
                #print('is close')
                count += 1
                break
    return count

# print(part1())

max_bounds = 4000000 if filename == "input.txt" else 20

def part2():
    y = 0
    while y <= max_bounds:
        print(f"y:{y}")
        x = 0
        while x <= max_bounds:
            #print(x)
            #print(f"x:{x}")
            found = False
            if (x ,y) in sensors or (x ,y) in beacons:
                #print('is beacon or sensor')
                x += 1
                continue
            for (sx ,sy), d in zip(sensors, distances):
                target_distance = mdistance((sx,sy),(x,y))
                if target_distance <= d:
                    found = True
                    x_shift = d - mdistance((x,y),(sx, sy)) 
                    x += x_shift
                    break
            if not found:
                return (x,y)
            x += 1
        y += 1

(x,y) = part2()
print(x,y)
print(x*4000000+y)
