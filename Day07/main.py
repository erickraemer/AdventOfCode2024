from pathlib import Path

from common.executor import execute

def read_input(file: Path) -> list[tuple[int, list[int]]]:
    equations: list[tuple[int, list[int]]] = []

    data = open(file, "r").read()

    for line in data.split("\n"):
        eq = line.split(":")
        operands = [int(op) for op in eq[1].strip().split(" ")]

        equations.append(
            (int(eq[0]), operands)
        )

    return equations

def part_one_rec(result: int, accumulator: int, operands: list[int], index: int) -> bool:
    if accumulator == result:
        return True

    if accumulator > result:
        return False

    if index >= len(operands):
        return False

    op: int = operands[index]
    index += 1

    return (
        part_one_rec(result, accumulator * op, operands, index) or
        part_one_rec(result, accumulator + op, operands, index)
    )


def part_one(file: Path) -> int:
    equations = read_input(file)

    sum_: int = 0
    for (result, operands) in equations:
        if part_one_rec(result, operands[0], operands, 1):
            sum_ += result

    return sum_

def part_two_rec(result: int, accumulator: int, operands: list[int], index: int) -> bool:
    if accumulator == result:
        return True

    if accumulator > result:
        return False

    if index >= len(operands):
        return False

    op: int = operands[index]
    index += 1

    return (
        part_two_rec(result, accumulator * op, operands, index) or
        part_two_rec(result, accumulator + op, operands, index) or
        part_two_rec(result, int(str(accumulator) + str(op)), operands, index)
    )


def part_two(file: Path) -> int:
    equations = read_input(file)

    sum_: int = 0
    for (result, operands) in equations:
        if part_two_rec(result, operands[0], operands, 1):
            sum_ += result

    return sum_


if __name__ == "__main__":
    execute(
        Path("Day07/test.txt"),
        Path("Day07/input.txt"),
        part_one,
        3749,
        "[1] Calibration result"
    )

    execute(
        Path("Day07/test.txt"),
        Path("Day07/input.txt"),
        part_two,
        11387,
        "[2] Calibration result"
    )
