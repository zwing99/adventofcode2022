import sys
from collections import deque
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.rstrip() for line in fh.readlines()]



class Monkey:
    def __init__(self, monkey_num, items, op_text, divis_by, true_loc, false_loc):
        self.monkey_num = 0
        self.items = deque(items)
        self.op_text = op_text
        self.divis_by = divis_by
        self.true_loc = true_loc
        self.false_loc = false_loc
        self.code = f"self.new = {self.op_text}"
        self.item_count = 0
        self.total_div = 3
    
    def process_items(self):
        while len(self.items) > 0:
            self.item_count += 1
            item = self.items.popleft()
            item = self.new_worry(item)
            #item = int(item/3)
            item = item % total_div
            self.throw_item(item)
    
    def new_worry(self, old):
        exec(self.code)
        return self.new
    
    def throw_item(self, item):
        if item % self.divis_by == 0:
            monkeys[self.true_loc].catch_item(item)
        else:
            monkeys[self.false_loc].catch_item(item)
    
    def catch_item(self, item):
        self.items.append(item)

monkeys: dict[int, Monkey] = {}
total_div = 1

for i in range(int(len(lines)/7)):
    block = lines[7*i+1:7*i+7]
    #print(block)
    monkey_num = i
    items = [int(j) for j in block[1].split(":")[1].split(",")]
    #print(items)
    op_text = block[2].split(":")[1].split("=")[1].strip()
    #print(op_text)
    divis_by = int(block[3].split()[-1])
    #print(divis_by)
    true_loc = int(block[4].split()[-1])
    #print(true_loc)
    false_loc = int(block[5].split()[-1])
    #print(false_loc)
    monkeys[monkey_num] = Monkey(monkey_num, items, op_text, divis_by, true_loc, false_loc)
    total_div *= divis_by

# part 2
for i, m in monkeys.items():
    m.total_div = total_div

#for r in range(20):
for r in range(10000):
    #print(r)
    for i, m in monkeys.items():
        m.process_items()
    for i, m in monkeys.items():
        ...
        #print(m.items)
    #print()

sorted_monkeys = list(monkeys.values())
sorted_monkeys.sort(key=lambda x: x.item_count, reverse=True)

print(sorted_monkeys[0].item_count*sorted_monkeys[1].item_count)
