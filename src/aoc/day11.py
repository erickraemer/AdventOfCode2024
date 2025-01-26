from pathlib import Path

from aoc import DATA
from src.aoc.common.executor import Executor


def read_input(file: Path) -> list[int]:
    arr = [int(i) for i in open(file, "r").read().split(" ")]
    return arr


def rec(iteration: int, state: int, lookup: dict[tuple[int, int], int], max_depth: int):
    if iteration == max_depth:
        return 1

    # states are completely deterministic which means
    # iterations and state will always result in the
    # same number of stones produced
    t: tuple[int, int] = (iteration, state)
    if t in lookup:
        return lookup[t]

    if state == 0:
        # add
        lookup[t] = rec(iteration + 1, 1, lookup, max_depth)
    else:
        s: str = str(state)
        l: int = len(s)
        if l % 2 == 0:
            m: int = l // 2

            # split stone
            lookup[t] = sum([
                rec(iteration + 1, int(s[:m]), lookup, max_depth),
                rec(iteration + 1, int(s[m:]), lookup, max_depth)
            ])
        else:
            # multiply
            lookup[t] = rec(iteration + 1, state * 2024, lookup, max_depth)

    return lookup[t]


def common_part(file: Path, blinks: int) -> int:
    state = read_input(file)

    # populate lookup
    lookup: dict[(int, int), int] = {}
    [rec(0, i, lookup, blinks) for i in state]

    n_stones = sum(lookup[(0, i)] for i in state)

    return n_stones


def part_one(file: Path) -> int:
    return common_part(file, 25)


def part_two(file: Path) -> int:
    return common_part(file, 75)


def main():
    executor = Executor(
        test_file=DATA / "t11.txt",
        input_file=DATA / "i11.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(55312)
    executor.one("Stones")

    executor.two("Stones")


if __name__ == "__main__":
    main()
