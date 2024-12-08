import itertools
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Optional

import numpy as np


def read_input(file: Path) -> tuple[list[list[np.ndarray]], tuple[int, int]]:
    antennas: dict[str, list[np.ndarray]] = defaultdict(list)

    data = open(file, "r").read().split()
    bounds = (len(data[0]), len(data))
    for y, line in enumerate(data):
        for x, c in enumerate(line):

            if c == '.':
                continue

            antennas[c].append(np.array([x, y]))

    antennas: list[list[np.ndarray]] = [v for k,v in antennas.items()]
    return antennas, bounds

def in_bounds(coord: tuple, bounds: tuple) -> bool:
    assert len(coord) == len(bounds)

    return all(coord[i] in range(bounds[i]) for i in range(len(coord)))

def part_one(file: Path) -> int:
    antennas, bounds = read_input(file)

    antinodes: set[tuple] = set()
    for ants in antennas:
        for (a, b) in itertools.permutations(ants, 2):

                t = tuple(2 * a - b)
                if in_bounds(t, bounds):
                    antinodes.add(t)

    return len(antinodes)

def part_two(file: Path) -> int:
    antennas, bounds = read_input(file)

    antinodes: set[tuple] = set()
    for ants in antennas:
        for (a, b) in itertools.permutations(ants, 2):

            freq = a - b

            q: int = 0
            while True:

                pos = tuple(a + (q * freq))

                if not in_bounds(pos, bounds):
                    break

                antinodes.add(tuple(pos))
                q += 1

    return len(antinodes)


if __name__ == "__main__":
    test_one = part_one(Path("test.txt"))
    assert test_one == 14, test_one

    po = part_one(Path("input.txt"))
    print(f"Unique locations: {po}")

    test_two = part_two(Path("test.txt"))
    assert test_two == 34, test_two

    pt = part_two(Path("input.txt"))
    print(f"Unique locations: {pt}")


