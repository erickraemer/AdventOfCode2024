from pathlib import Path

from aoc import DATA
from src.aoc.common.executor import Executor


def load_input(file: Path) -> list[str]:
    text: list[str] = []
    with open(file, "r") as f:
        for line in f.readlines():
            text.append(line.replace("\n", ""))

    return text


def part_one(file: Path):
    text: list[str] = load_input(file)

    word: str = "XMAS"
    w_len: int = len(word)

    # assume a rectangle
    y_len: int = len(text)
    x_len: int = len(text[0])

    # precalculate coordinates for all directions
    #         \ | /
    #         - x -
    #         / | \
    coordinates = [
        [(y * k, x * k) for k in range(w_len)]
        for y in (0, 1, -1)
        for x in (0, 1, -1)
        if (x, y) != (0, 0)
    ]

    appearances: int = 0

    # use sliding window approach
    for y in range(y_len):
        for x in range(x_len):
            for coords in coordinates:

                # check bounds
                cy, cx = coords[-1]

                if y + cy not in range(0, y_len):
                    continue

                if x + cx not in range(0, x_len):
                    continue

                # collect word from direction
                s: str = "".join(text[y + cy][x + cx] for (cy, cx) in coords)

                if s == word:
                    appearances += 1

    return appearances


def part_two(file: Path):
    text: list[str] = load_input(file)

    word: str = "MAS"
    w_len: int = len(word)

    # assume a rectangle
    y_len: int = len(text)
    x_len: int = len(text[0])

    # precalculate coordinates for all directions
    #         \ | /
    #         - x -
    #         / | \
    coordinates = [
        [(k * i, k * l) for k in range(-w_len // 2 + 1, w_len // 2 + 1)]
        for i in (1, -1)
        for l in (1, -1)
    ]

    appearances: int = 0

    # use sliding window approach
    for y in range(y_len):
        for x in range(x_len):

            count: int = 0
            for coords in coordinates:

                s = ""
                for (cy, cx) in coords:
                    if y + cy not in range(0, y_len):
                        break

                    if x + cx not in range(0, x_len):
                        break

                    s += text[y + cy][x + cx]

                if s == word:
                    count += 1

                if count == 2:
                    appearances += 1
                    break

    return appearances


def main():
    executor = Executor(
        test_file=DATA / "t04.txt",
        input_file=DATA / "i04.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(18)
    executor.one("XMAS Appearances")

    executor.test_two(9)
    executor.two("X-MAS Appearances")


if __name__ == "__main__":
    main()
