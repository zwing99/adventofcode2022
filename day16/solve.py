import sys
from dataclasses import dataclass, field
import statistics
from itertools import product
from copy import deepcopy
filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]

@dataclass
class Valve:
    name: str
    rate: int
    leads_to: list[str]


valves: dict[str, Valve] = {}

for line in lines:
    valve_def, leads_to = line.split(";")
    valve_def_s = valve_def.split()
    name = valve_def_s[1]
    rate = int(valve_def_s[4].split("=")[1])
    valve = Valve(name, rate, [])
    leads_to_split = leads_to.split(" ")
    while leads_to_split[-1] not in ("valves", "valve"):
        valve.leads_to.append(leads_to_split.pop(-1).strip(","))
    valves[valve.name] = valve

for v in valves.values():
    print(f"{v.name} -> {v.leads_to}")


@dataclass
class State:
    location: str
    e_location: str
    valve_states: dict[str, bool] = field(repr=False)
    flow_total: int = 0
    path: list[str] = field(default_factory=list)
    e_path: list[str] = field(default_factory=list)
    releases: list[int] = field(default_factory=list)

    def update_flow(self):
        release = sum([
            v.rate
            for v in valves.values()
            if self.valve_states[v.name]
        ])
        self.releases.append(release)
        self.flow_total += release


def get_starting_state():
    return State(
        "AA",
        "AA",
        {v.name: True if v.rate == 0 else False for v in valves.values()},
    )

def valve_count(s):
    return len([v for v in s.valve_states.values() if v])

def run_for_x(max_time=30, elephant=False):
    states: list[State] = [get_starting_state()]
    min_valves = min(set([valve_count(s) for s in states]))
    all_open: list[State] = []
    time = 0
    while time < max_time:
        time += 1
        print(time)
        new_states: list[State] = []
        for state in all_open:
            state.update_flow()
        for state in states:
            #print(state)
            state.update_flow()
            # Open a Valve
            #print(f"open {state.location}")
            move_human = True
            move_elephant = elephant
            if not state.valve_states[state.location]:
                state.valve_states[state.location] = True
                move_human = False
            if move_elephant:
                if not state.valve_states[state.e_location]:
                    state.valve_states[state.e_location] = True
                    move_elephant = False
            if all(state.valve_states.values()):
                #print(f"all open {state.location}")
                all_open.append(state)
            else:
                human_next = [state.location]
                elephant_next = [state.e_location]
                if move_human:
                    human_next = valves[state.location].leads_to
                if move_elephant:
                    elephant_next = valves[state.e_location].leads_to
                for h_next, e_next in product(human_next, elephant_next):
                    new_states.append(
                        State(
                            h_next,
                            e_next,
                            deepcopy(state.valve_states),
                            state.flow_total,
                            state.path + [state.location],
                            state.e_path + [state.e_location],
                            deepcopy(state.releases),
                        )
                    )
        # TODO: purge
        old_len = len(new_states)
        #locations = set([s.location for s in new_states])
        #new_states.sort(key=lambda x: x.location, reverse=True)
        #for state in new_states:
        #    print(state)
        #print('----')
        #for location in locations:
        #    loc_state = [s for s in new_states if s.location == location]
        #    #if len(loc_state) > 1:
        #    #    print(loc_state)
        #    max_flow = max(loc_state, key=lambda x: x.flow_total).flow_total
        #    for state in filter(lambda x: x.flow_total != max_flow, loc_state):
        #        new_states.remove(state)
        #for state in new_states:
        #    print(state)
        #print(old_len, len(new_states))
        print(set([len([v for v in s.valve_states.values() if v]) for s in new_states]))
        CULL = 50_000
        if len(new_states) > CULL:
            #median = statistics.median([s.flow_total for s in new_states])
            #new_states = [s for s in new_states if s.flow_total >= median]
            new_states = [s for s in new_states if valve_count(s) > min_valves]
            new_states.sort(key=lambda x: x.flow_total, reverse=True)
            new_states=new_states[:CULL]
        states = new_states
        print (len(states), len(all_open))
        #if time > 6:
        #    break

    everything = states + all_open
    everything.sort(key=lambda x: x.flow_total, reverse=True)
    return everything


# part 1
#everything = run_for_x(30)
#print(len(everything))
#for e in everything[:3]:
#    print(e.flow_total)
#    print(e.path)
#    print(e.releases)
#
# part 2
everything = run_for_x(26, True)
print(len(everything))
for e in everything[:3]:
    print(e.flow_total)
    print(e.path)
    print(e.e_path)
    print(e.releases)


# 2520