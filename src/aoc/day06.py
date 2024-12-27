import curses
import time
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Optional

import numpy as np

from aoc import DATA
from src.aoc.common.executor import Executor


def read_input(file: Path) -> tuple[set[tuple[int, int]], np.ndarray, np.ndarray, np.ndarray]:
    obstacles: set[tuple[int, int]] = set()
    guard_position: Optional[np.ndarray] = None
    guard_orientation: Optional[np.ndarray] = None

    # read input
    lines: list[str] = open(file, "r").read().split()

    map_shape: np.ndarray = np.array([len(lines[0]), len(lines)])

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


def part_one(file: Path) -> set[tuple]:
    obstacles, guard_pos, guard_ori, map_shape = read_input(file)

    visited_positions: set[tuple] = set()
    rot_m = np.array([[0, -1], [1, 0]])

    while True:

        if guard_pos[0] not in range(map_shape[0]):
            break

        if guard_pos[1] not in range(map_shape[1]):
            break

        next_pos: np.ndarray = guard_pos + guard_ori

        if tuple(next_pos) in obstacles:
            guard_ori = rot_m @ guard_ori
            continue

        visited_positions.add(tuple(guard_pos))
        guard_pos = next_pos

    return visited_positions


ORI_MAP = {
    (-1, 0): '<',
    (0, -1): '^',
    (1, 0): '>',
    (0, 1) : 'v'
}

def draw(stdscr, obstacles, visited_positions, guard_pos, guard_ori, map_shape, size=16):

    size = min(map_shape[0], size)

    # Clear screen
    curses.curs_set(0)
    stdscr.clear()

    for y in range(size):
        for x in range(size):
            pos = guard_pos + np.array([-size // 2 + x, -size // 2 + y])

            if np.array_equal(pos, guard_pos):
                stdscr.addstr(y, x * 2, ORI_MAP[tuple(guard_ori)] + ' ')
            elif tuple(pos) in obstacles:
                stdscr.addstr(y, x * 2, '# ')
            elif tuple(pos) in visited_positions:
                stdscr.addstr(y, x * 2, 'x ')
            elif pos[0] not in range(map_shape[0]):
                stdscr.addstr(y, x * 2, '  ')
            elif pos[1] not in range(map_shape[1]):
                stdscr.addstr(y, x * 2, '  ')
            else:
                stdscr.addstr(y, x * 2, '. ')

    stdscr.refresh()
    time.sleep(1 / 60)


def find_loop(stdscr, obstacles, guard_pos, guard_ori, map_shape):
    guard_pos = deepcopy(guard_pos)
    guard_ori = deepcopy(guard_ori)
    visited_positions: dict[tuple, set[tuple]] = defaultdict(set)
    rot_m = np.array([[0, -1], [1, 0]])

    while True:

        # visualize guard
        if stdscr is not None:
            draw(stdscr, obstacles, visited_positions, guard_pos, guard_ori, map_shape)

        if guard_pos[0] not in range(map_shape[0]):
            return False

        if guard_pos[1] not in range(map_shape[1]):
            return False

        next_pos: np.ndarray = guard_pos + guard_ori
        next_pos_t = tuple(next_pos)

        if tuple(next_pos) in obstacles:
            guard_ori = rot_m @ guard_ori
            continue

        guard_pos_t = tuple(guard_pos)
        if guard_pos_t in visited_positions[next_pos_t]:
            return True

        visited_positions[next_pos_t].add(guard_pos_t)
        guard_pos = next_pos

def part_two(file: Path, draw: bool = False) -> int:
    obstacles, guard_pos, guard_ori, map_shape = read_input(file)
    visited_pos = part_one(file)

    obstruction_pos = set()

    for i, pos in enumerate(visited_pos):

        print(f"\rProcessing: {round(100 * i / len(visited_pos), 2)}%", end="", flush=True)

        args = [obstacles | {pos},
            guard_pos,
            guard_ori,
            map_shape
        ]

        if draw:
            loop = curses.wrapper(
                find_loop,
                *args
            )
        else:
            loop = find_loop(None, *args)

        if loop:
            obstruction_pos.add(pos)


    print("\r", end="", flush=True)
    return len(obstruction_pos)


def main():
    executor = Executor(
        test_file=DATA / "t06.txt",
        input_file=DATA / "i06.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(41)
    executor.one("Distinct positions")

    executor.test_two(6)
    executor.two("Obstacle positions")

if __name__ == "__main__":
    main()