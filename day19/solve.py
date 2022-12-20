from dataclasses import dataclass, field, replace, asdict
import math
import sys
from enum import Enum
import re
import typing as typ
from copy import deepcopy

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"


class RoboTypes(Enum):
    Unknown = 0
    OreRobo = 1
    ClayRobo = 2
    ObsRobo = 3
    GeoRobo = 4


class Stuff(Enum):
    Ore = 1
    Clay = 2
    Obs = 3
    Geo = 4


STUFF_TO_ROBO = {
    Stuff.Ore: RoboTypes.OreRobo,
    Stuff.Clay: RoboTypes.ClayRobo,
    Stuff.Obs: RoboTypes.ObsRobo,
    Stuff.Geo: RoboTypes.GeoRobo,
}


@dataclass
class Blueprint:
    bp_id: int
    costs: dict[RoboTypes, dict[Stuff, int]]
    robo_counts: dict[RoboTypes, int]
    stuff_counts: dict[Stuff, int]
    maxes: dict[Stuff, int]
    costs: dict[RoboTypes, dict[Stuff, int]]
    next_robo: RoboTypes = RoboTypes.Unknown
    clock: int = 0

    @classmethod
    def factory(
        cls,
        bp_id: int,
        orerobo_ore: int,
        clayrobo_ore: int,
        obsrobo_ore: int,
        obsrobo_clay: int,
        georobo_ore: int,
        georobo_obs: int,
    ) -> "Blueprint":
        return cls(
            bp_id=bp_id,
            costs=deepcopy(
                {
                    RoboTypes.OreRobo: {Stuff.Ore: orerobo_ore},
                    RoboTypes.ClayRobo: {Stuff.Ore: clayrobo_ore},
                    RoboTypes.ObsRobo: {
                        Stuff.Ore: obsrobo_ore,
                        Stuff.Clay: obsrobo_clay,
                    },
                    RoboTypes.GeoRobo: {Stuff.Ore: georobo_ore, Stuff.Obs: georobo_obs},
                }
            ),
            maxes=deepcopy(
                {
                    Stuff.Ore: max(orerobo_ore, clayrobo_ore, obsrobo_ore),
                    Stuff.Clay: obsrobo_clay,
                    Stuff.Obs: georobo_obs,
                }
            ),
            robo_counts=deepcopy(
                {
                    RoboTypes.OreRobo: 1,
                    RoboTypes.ClayRobo: 0,
                    RoboTypes.ObsRobo: 0,
                    RoboTypes.GeoRobo: 0,
                }
            ),
            stuff_counts=deepcopy(
                {
                    Stuff.Ore: 0,
                    Stuff.Clay: 0,
                    Stuff.Obs: 0,
                    Stuff.Geo: 0,
                }
            ),
        )

    def get_state(self, time_left: min):
        return (
            self.clock,
            self.next_robo.value,
            self.robo_counts[RoboTypes.OreRobo],
            self.robo_counts[RoboTypes.ClayRobo],
            self.robo_counts[RoboTypes.ObsRobo],
            self.robo_counts[RoboTypes.GeoRobo],
            min(
                self.stuff_counts[Stuff.Ore],
                time_left * self.maxes[Stuff.Ore] - (time_left - 1) * self.robo_counts[RoboTypes.OreRobo],
            ),
            min(
                self.stuff_counts[Stuff.Clay],
                time_left * self.maxes[Stuff.Clay] - (time_left - 1) * self.robo_counts[RoboTypes.ClayRobo],
            ),
            min(
                self.stuff_counts[Stuff.Obs],
                time_left * self.maxes[Stuff.Obs] - (time_left - 1) * self.robo_counts[RoboTypes.ObsRobo],
            ),
            self.stuff_counts[Stuff.Geo],
        )

    def time_to_make(self, rt: RoboTypes) -> int:
        cost = self.costs[rt]
        times = [
            int(
                math.ceil(
                    (amt - self.stuff_counts[r]) / self.robo_counts[STUFF_TO_ROBO[r]]
                )
            )
            for r, amt in cost.items()
        ]
        return max(times)

    def set_next(self, first_target: RoboTypes):
        self.next_robo = first_target

    def can_build_next_robo(self) -> bool:
        for rt, amt in self.costs[self.next_robo].items():
            if self.stuff_counts[rt] < amt:
                return False
        return True

    def harvest(self):
        self.stuff_counts[Stuff.Ore] += self.robo_counts[RoboTypes.OreRobo]
        self.stuff_counts[Stuff.Clay] += self.robo_counts[RoboTypes.ClayRobo]
        self.stuff_counts[Stuff.Obs] += self.robo_counts[RoboTypes.ObsRobo]
        self.stuff_counts[Stuff.Geo] += self.robo_counts[RoboTypes.GeoRobo]

    def step_one_minute(self) -> bool:
        self.clock += 1
        can_build = self.can_build_next_robo()
        self.harvest()
        if can_build:
            for rt, amt in self.costs[self.next_robo].items():
                self.stuff_counts[rt] -= amt
            self.robo_counts[self.next_robo] += 1

        return can_build


asdf = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)
with open(filename) as fh:
    lines = [line.strip() for line in fh.readlines()]


bps: list[Blueprint] = []
for line in lines:
    m = asdf.match(line)
    bp = Blueprint.factory(*[int(i) for i in m.groups()])
    bps.append(bp)


def create_clone(bp: Blueprint, next_robo: RoboTypes) -> Blueprint:
    bp1 = Blueprint(**asdict(bp))
    bp1.set_next(next_robo)
    return bp1


# pt2
qualities = []
# for bp in bps[1:]:
for bp in bps[:3]:
    print("-" * 40)
    print(f"{bp.bp_id}")
    print("-" * 40)
    simset: list[Blueprint] = [
        create_clone(bp, RoboTypes.OreRobo),
        create_clone(bp, RoboTypes.ClayRobo),
    ]
    MAX_TIME = 32
    # best_order2 = [Stuff.Ore, Stuff.Clay, Stuff.Obs, Stuff.Geo]
    visited = set()
    for i in range(MAX_TIME):
        next_set: list[Blueprint] = []
        time_left = MAX_TIME - i - 1
        for item in simset:
            state = item.get_state(time_left)
            if state in visited:
                continue
            visited.add(state)
            if item.step_one_minute():
                options = []
                if (
                    item.time_to_make(RoboTypes.OreRobo) <= time_left
                    and item.robo_counts[RoboTypes.OreRobo] < item.maxes[Stuff.Ore]
                ):
                    options.append(RoboTypes.OreRobo)

                if (
                    item.time_to_make(RoboTypes.ClayRobo) <= time_left
                    and item.robo_counts[RoboTypes.ClayRobo] < item.maxes[Stuff.Clay]
                ):
                    options.append(RoboTypes.ClayRobo)

                if (
                    item.robo_counts[RoboTypes.ClayRobo] > 0
                    and item.time_to_make(RoboTypes.ObsRobo) <= time_left
                    and item.robo_counts[RoboTypes.ObsRobo] < item.maxes[Stuff.Obs]
                ):
                    options.append(RoboTypes.ObsRobo)

                if (
                    item.robo_counts[RoboTypes.ObsRobo] > 0
                    and item.time_to_make(RoboTypes.GeoRobo) <= time_left
                ):
                    options.append(RoboTypes.GeoRobo)

                if options:
                    next_set.extend([create_clone(item, o) for o in options])
                else:
                    next_set.append(item)
            else:
                next_set.append(item)

        simset = next_set

        # for item in next_set:
        #    add_it = True
        #    if (
        #        item.robo_counts[RoboTypes.ObsRobo] == 0
        #        and item.time_to_make(RoboTypes.ObsRobo) > time_left
        #    ):
        #        add_it = False
        #    elif (
        #        item.robo_counts[RoboTypes.GeoRobo] == 0
        #        and item.time_to_make(RoboTypes.GeoRobo) > time_left
        #    ):
        #        add_it = False
        #    if add_it:
        #        simset.append(item)

        print(f"Time: {i}, Count: {len(simset)}")

    best = max(simset, key=lambda x: x.stuff_counts[Stuff.Geo])
    print(best.robo_counts)
    print(best.stuff_counts)
    qualities.append(best.stuff_counts[Stuff.Geo])

print(qualities)
print(sum(qualities))
