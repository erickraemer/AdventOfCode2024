from collections import defaultdict
from copy import copy
from pathlib import Path

from aoc import DATA
from src.aoc.common.executor import Executor


def read_input(file: Path) -> tuple[list[tuple[int, int]], list[list[int]]]:
    with open(file, "r") as f:
        s = f.read()

    s = s.split("\n\n")
    update_rules: list[tuple[int, int]] = [
        (int(l), int(r)) for (l, r) in
        (line.split("|") for line in s[0].split("\n"))
    ]

    sequences: list[list[int]] = [
        [int(i) for i in seq.split(",")]
        for seq in s[1].split("\n")
    ]

    return update_rules, sequences


def part_one(file: Path) -> int:
    update_rules, sequences = read_input(file)

    rule_lookup = defaultdict(set)

    for (i, k) in update_rules:
        rule_lookup[i].add(k)

    def scan_backwards(seq: list[int]):
        # scan backwards for rule violations

        for i in range(1, len(seq)):
            for k in range(i - 1, -1, -1):

                # stop when finding the same element backwards
                if seq[k] == seq[i]:
                    break

                if seq[k] in rule_lookup[seq[i]]:
                    return False

        return True

    sum_: int = 0
    for seq in sequences:

        # ignore on rule violation
        if not scan_backwards(seq):
            continue

        # add middle number
        sum_ += seq[len(seq) // 2]

    return sum_


def part_two(file: Path) -> int:
    update_rules, sequences = read_input(file)

    rule_lookup = defaultdict(set)

    for (i, k) in update_rules:
        rule_lookup[i].add(k)

    def sort_sequence(seq: list[int]):
        # scan backwards and move page to the right on rule violation

        seq = copy(seq)
        i = 1
        while i < len(seq):

            moves = 0
            for k in range(i-1, -1, -1):

                # stop when finding the same element backwards
                if seq[i] == seq[k]:
                    break

                # move page to the right
                if seq[k] in rule_lookup[seq[i]]:
                    seq.insert(i, seq.pop(k))
                    i -= 1
                    moves += 1

            i += 1 + moves
        return seq

    sum_: int = 0
    for seq in sequences:

        ss = sort_sequence(seq)

        # ignore if sequence was correct
        if seq == ss:
            continue

        # add middle number
        sum_ += ss[len(seq) // 2]

    return sum_


def main():
    executor = Executor(
        test_file=DATA / "t05.txt",
        input_file=DATA / "i05.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(143)
    executor.one("Middle page number sum")

    executor.test_two(123)
    executor.two("Middle page number sum")

if __name__ == "__main__":
    main()
