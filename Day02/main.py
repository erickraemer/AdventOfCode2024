from copy import copy
from pathlib import Path

from common.executor import execute


def is_safe(report: list[int]) -> bool:
    if len(report) <= 1:
        return True

    ascending: bool = report[0] < report[1]

    for i in range(len(report) - 1):
        asc: bool = report[i] < report[i + 1]

        if ascending != asc:
            return False

        delta: int = abs(report[i] - report[i + 1])

        if delta not in range(1, 4):
            return False

    return True


def load_input(file: Path) -> list[list[int]]:
    reports: list[list[int]] = []
    with open(file, "r") as f:
        for line in f.readlines():
            report = [int(i) for i in line.split(" ")]
            reports.append(report)

    return reports


def part_one(file: Path):
    reports: list[list[int]] = load_input(file)

    safe_reports: int = 0

    report: list[int]
    for report in reports:
        safe_reports += int(is_safe(report))

    return safe_reports


def part_two(file: Path):
    reports: list[list[int]] = load_input(file)

    safe_reports: int = 0

    report: list[int]
    for report in reports:
        b = is_safe(report)

        # brute-force method
        # very inefficient but fast to code
        if not b:
            for k in range(len(report)):
                report_copy = copy(report)
                report_copy.pop(k)

                b = is_safe(report_copy)
                if b:
                    break

        safe_reports += int(b)

    return safe_reports


if __name__ == "__main__":
    execute(
        Path("Day02/test.txt"),
        Path("Day02/input.txt"),
        part_one,
        2,
        "[1] Safe Reports"
    )

    execute(
        Path("Day02/test.txt"),
        Path("Day02/input.txt"),
        part_two,
        4,
        "[2] Safe Reports"
    )