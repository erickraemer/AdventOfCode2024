import re
from pathlib import Path

from common.executor import execute


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

if __name__ == "__main__":
    execute(
        Path("Day03/test01.txt"),
        Path("Day03/input.txt"),
        part_one,
        161,
        "[1] Safe Reports"
    )

    execute(
        Path("Day03/test02.txt"),
        Path("Day03/input.txt"),
        part_two,
        48,
        "[2] Safe Reports"
    )
