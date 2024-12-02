from collections import defaultdict
from pathlib import Path

import numpy as np


def read_input(file: Path) -> tuple[list[int], list[int]]:
    l1 = []
    l2 = []

    # read input into two lists
    with open(file, "r") as f:
        for line in f.readlines():
            out = line.split("   ")
            l1.append(int(out[0]))
            l2.append(int(out[1]))

    # check if both lists have the same length
    assert len(l1) == len(l2)

    return l1, l2


def part_one():
    input_file = Path("input.txt")
    l1, l2 = read_input(input_file)

    # sort lists
    l1.sort()
    l2.sort()

    # convert lists into vectors
    v1 = np.array(l1, dtype=int)
    v2 = np.array(l2, dtype=int)

    # calculate the l1 norm between both vectors
    distance: int = int(np.sum(np.abs(v1 - v2)))

    print(f"Distance: {distance}")


def part_two():
    input_file = Path("input.txt")
    l1, l2 = read_input(input_file)

    appearances = defaultdict(int)

    # count appearances
    for i in l2:
        appearances[i] += 1

    # calculate similarity score
    sum_ = 0
    for i in l1:
        sum_ += i * appearances[i]

    print(f"Similarity Score: {sum_}")


if __name__ == "__main__":
    part_one()
    part_two()
