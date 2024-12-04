import re


def part_one():
    with open("input.txt", "r") as f:
        s = f.read()

    pattern = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")

    sum_: int = 0
    for match in pattern.finditer(s):
        sum_ += int(match.group(1)) * int(match.group(2))

    print(f"Sum: {sum_}")


def part_two():
    with open("input.txt", "r") as f:
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

    print(f"Sum: {sum_}")


if __name__ == "__main__":
    part_one()
    part_two()
