from pathlib import Path

from common.executor import execute


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

def main(file: Path, blinks: int) -> int:
    state = read_input(file)

    # populate lookup
    lookup: dict[(int, int), int] = {}
    [rec(0, i, lookup, blinks)for i in state]

    n_stones = sum(lookup[(0,i)] for i in state)

    return n_stones

def part_one(file: Path) -> int:
    return main(file, 25)

def part_two(file: Path) -> int:
    return main(file, 75)

if __name__ == "__main__":
    execute(
        Path("Day11/test.txt"),
        Path("Day11/input.txt"),
        part_one,
        55312,
        "[1] Stones"
    )

    execute(
        None,
        Path("Day11/input.txt"),
        part_two,
        0,
        "[1] Stones"
    )