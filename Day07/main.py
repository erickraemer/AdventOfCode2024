from pathlib import Path

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
    test_one = part_one(Path("test.txt"))
    assert test_one == 3749, test_one

    po = part_one(Path("input.txt"))
    print(f"Calibration result: {po}")

    test_two = part_two(Path("test.txt"))
    assert test_two == 11387, test_two

    pt = part_two(Path("input.txt"))
    print(f"Calibration result: {pt}")
