from collections import ChainMap
from pathlib import Path
from typing import Optional, Iterable, Final

import numpy as np

from aoc import DATA
from aoc.common.executor import Executor

Coord = tuple[int, int]

class ObstacleMap:
    def __init__(self, obstacles: Iterable[tuple[int, int]], map_shape: tuple[int, int]):
        self._yx = [[] for _ in range(map_shape[1])]
        self._xy = [[] for _ in range(map_shape[0])]

        for (x, y) in obstacles:
            self._yx[y].append(x)
            self._xy[x].append(y)

        for li in self._yx:
            li.sort()

        for li in self._xy:
            li.sort()

    def next(self, pos: tuple[int, int], orientation: int):
        if orientation == 0:
            return self.right(pos)
        if orientation == 1:
            return self.down(pos)
        if orientation == 2:
            return self.left(pos)
        return self.up(pos)

    def up(self, pos: tuple[int, int]):
        if pos[0] not in range(len(self._xy)):
            return None

        row = self._xy[pos[0]]
        for i in range(len(row) - 1, -1, -1):

            if row[i] < pos[1]:
                return pos[0], row[i]

        return None

    def down(self, pos: tuple[int, int]):
        if pos[0] not in range(len(self._xy)):
            return None

        row = self._xy[pos[0]]
        for i in range(len(row)):

            if row[i] > pos[1]:
                return pos[0], row[i]

        return None

    def left(self, pos: tuple[int, int]):
        if pos[1] not in range(len(self._yx)):
            return None

        col = self._yx[pos[1]]
        for i in range(len(col) - 1, -1, -1):

            if col[i] < pos[0]:
                return col[i], pos[1]

        return None

    def right(self, pos: tuple[int, int]):
        if pos[1] not in range(len(self._yx)):
            return None

        col = self._yx[pos[1]]
        for i in range(len(col)):

            if col[i] > pos[0]:
                return col[i], pos[1]

        return None


def read_input(file: Path) -> tuple[set[tuple[int, int]], np.ndarray, np.ndarray, tuple[int, int]]:
    obstacles: set[tuple[int, int]] = set()
    guard_position: Optional[np.ndarray] = None
    guard_orientation: Optional[np.ndarray] = None

    # read input
    lines: list[str] = open(file, "r").read().split()

    map_shape: tuple[int, int] = (len(lines[0]), len(lines))

    ori_map = {
        '<': (-1, 0),
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1)
    }

    for y, line in enumerate(lines):
        for x, c in enumerate(line):

            if c == '.':
                continue

            if c == '#':
                obstacles.add((x, y))
                continue

            if c in ori_map:
                guard_position = np.array([x, y])
                guard_orientation = np.array(ori_map[c])
                continue

    assert guard_position is not None
    assert guard_orientation is not None

    return obstacles, guard_position, guard_orientation, map_shape

def in_bounds(pos: Coord, bounds: Coord) -> bool:
    assert len(pos) == len(bounds)

    return all(pos[i] in range(bounds[i]) for i in range(len(pos)))

def get_input(file: Path) -> tuple[list[str], Coord, int]:
    lines: list[str] = open(file, "r").read().split()

    guard_orientation: dict[chr, int] = {
        '>': 0,
        'v': 1,
        '<': 2,
        '^': 3
    }

    def find_guard() -> tuple[Coord, int]:
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                c: chr = lines[y][x]
                if c in guard_orientation:
                    return (x, y), guard_orientation[c]

    g_pos, g_ori = find_guard()
    return lines, g_pos, g_ori

def part_one(file: Path) -> set[Coord]:
    map_, g_pos, g_o_idx = get_input(file)

    orientations: Final[list[Coord]] = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]

    unique_positions: set[Coord] = set()

    while True:

        unique_positions.add(g_pos)

        x, y = g_pos
        ox, oy = orientations[g_o_idx]
        xn, yn = x+ox, y+oy

        if not (0 <= xn < len(map_[0])):
            break

        if not (0 <= yn < len(map_)):
            break

        if map_[yn][xn] == '#':
            g_o_idx = (g_o_idx + 1) % len(orientations)
            continue

        g_pos = xn , yn

    return unique_positions


def create_lookup(obstacle: tuple[int], omap: ObstacleMap) -> dict[tuple[int], tuple[int]]:
    lookup = dict()

    # left case
    next_obs = omap.next((obstacle[0]-1, obstacle[1]), 1)
    next_obs = (next_obs[0], next_obs[1]-1, 1) if next_obs is not None else None

    p = (obstacle[0]-1, obstacle[1], 0)
    lookup[p] = next_obs
    pos = (obstacle[0], obstacle[1]-1)
    end = omap.next(obstacle, 2)
    while True:
        pos = omap.next(pos, 2)

        if pos is None:
            break

        if end is not None and pos[0] <= end[0]:
            break

        lookup[(pos[0], pos[1]+1, 3)] = p

    # down case
    next_obs = omap.next((obstacle[0], obstacle[1]+1), 0)
    next_obs = (next_obs[0]-1, next_obs[1], 0) if next_obs is not None else None

    p = (obstacle[0], obstacle[1]+1, 3)
    lookup[p] = next_obs
    pos = (obstacle[0]-1, obstacle[1])
    end = omap.next(obstacle, 1)
    while True:
        pos = omap.next(pos, 1)

        if pos is None:
            break

        if end is not None and pos[1] >= end[1]:
            break

        lookup[(pos[0]+1, pos[1], 2)] = p

    # right case
    next_obs = omap.next((obstacle[0]+1, obstacle[1]), 3)
    next_obs = (next_obs[0], next_obs[1] + 1, 3) if next_obs is not None else None

    p = (obstacle[0] + 1, obstacle[1], 2)
    lookup[p] = next_obs
    pos = (obstacle[0], obstacle[1]+1)
    end = omap.next(obstacle, 0)
    while True:
        pos = omap.next(pos, 0)

        if pos is None:
            break

        if end is not None and pos[0] >= end[0]:
            break

        lookup[(pos[0], pos[1]-1, 1)] = p

    # up case
    next_obs = omap.next((obstacle[0], obstacle[1]-1), 2)
    next_obs = (next_obs[0]+1, next_obs[1], 2) if next_obs is not None else None

    p = (obstacle[0], obstacle[1]-1, 1)
    lookup[p] = next_obs
    pos = (obstacle[0]+1, obstacle[1])
    end = omap.next(obstacle, 3)
    while True:
        pos = omap.next(pos, 3)

        if pos is None:
            break

        if end is not None and pos[1] <= end[1]:
            break

        lookup[(pos[0]-1, pos[1], 0)] = p

    return lookup


def part_two(file: Path) -> set[tuple[int]]:

    obstacles, guard_pos, guard_ori, map_shape = read_input(file)

    ori_map = {
        (1, 0): 0,  # right
        (0, 1): 1,  # down
        (-1, 0): 2, # left
        (0, -1): 3  # up
    }

    rotation_map = {v:k for k,v in ori_map.items()}

    omap = ObstacleMap(obstacles, map_shape)
    move_lookup: dict[tuple[int], tuple[int]] = dict()
    temp_lookup: dict[tuple[int], tuple[int]] = dict()
    state_lookup = ChainMap(temp_lookup, move_lookup)
    loop_positions: set[tuple[int]] = set()
    checked_obstacles = set()

    rot_m = np.array([[0, -1], [1, 0]])

    while in_bounds(guard_pos+guard_ori, map_shape):

        orientation: int = ori_map[tuple(guard_ori)]
        pose = (*tuple(guard_pos), orientation)
        obstacle = tuple(guard_pos + guard_ori)

        if obstacle in obstacles:
            guard_ori = rot_m @ guard_ori
            continue

        visited_poses: set[tuple[int]] = set()

        temp_lookup.clear()
        temp_lookup.update(create_lookup(obstacle, omap))

        if obstacle not in checked_obstacles:
            while True:

                if pose is None:
                    # no loop
                    break

                if pose in visited_poses:
                    # loop
                    loop_positions.add(obstacle)
                    break

                visited_poses.add(pose)

                if pose not in state_lookup:
                    orientation_ = pose[-1]
                    next_pose = omap.next(pose[:2], (orientation_+1)%4)

                    if next_pose is not None:
                        rot = rotation_map[(orientation_-1)%4]
                        next_pose = (next_pose[0] + rot[0], next_pose[1] + rot[1], (orientation_+1)%4)

                    move_lookup[pose] =  next_pose

                pose = state_lookup[pose]

        checked_obstacles.add(obstacle)

        guard_pos += guard_ori

    return loop_positions

def main():
    executor = Executor(
        test_file=DATA / "t06.txt",
        input_file=DATA / "i06.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(41)
    executor.one("Unique positions")

    executor.test_two(6)
    executor.two("Loop positions")

if __name__ == "__main__":
    main()



