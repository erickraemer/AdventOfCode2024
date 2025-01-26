import re
from pathlib import Path

from aoc import DATA
from src.aoc.common.executor import Executor


def part_one(file: Path) -> int:
    with open(file, "r") as f:
        s = f.read()

    pattern = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")

    sum_: int = 0
    for match in pattern.finditer(s):
        sum_ += int(match.group(1)) * int(match.group(2))

    return sum_


def part_two(file: Path) -> int:
    with open(file, "r") as f:
        s = f.read()

    pattern = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don't\(\)")

    enabled: bool = True
    sum_: int = 0
    for match in pattern.finditer(s):
        c: chr = match.group(0)[2]

        assert c in {'l', 'n', '('}

        if c == 'l':
            if enabled:
                sum_ += int(match.group(1)) * int(match.group(2))
        else:
            enabled = (c == '(')

    return sum_


def main():
    executor = Executor(
        test_file=DATA / "t03_01.txt",
        test_file_2=DATA / "t03_02.txt",
        input_file=DATA / "i03.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(161)
    executor.one("Product")

    executor.test_two(48)
    executor.two("Product")


if __name__ == "__main__":
    main()
