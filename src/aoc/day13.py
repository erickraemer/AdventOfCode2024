import re
from pathlib import Path

import numpy as np

from aoc import DATA
from aoc.common.executor import Executor

INPUT_REGX = re.compile(r"\D+(\d+)\D+(\d+)\n\D+(\d+)\D+(\d+)\n\D+(\d+)\D+(\d+)")

def read_input(file: Path) -> list[tuple[int, ...]]:
    
    data = open(file, "r").read()

    arcades = [
        tuple(int(c) for c in m)
        for m in INPUT_REGX.findall(data)
    ]

    return arcades

def binary_search(a_vec: np.ndarray, b_vec: np.ndarray, goal: np.ndarray) -> np.ndarray:
    """
    Uses binary search to find values for a and b. The algorithm starts with the range of
    R = [0, goal / (a.x, a.y)]. Each iteration calculates an estimate of b and trims either
    the upper or lower half of the range R, based on the error function |b.x - b.y|.
    :param a_vec: a vector
    :param b_vec: b vector
    :param goal: goal vector
    :return: (a presses, b presses) if a solution exists else (0,0)
    """
    def error(a_):
        b_: np.ndarray = (goal - (a_ * a_vec)) / b_vec
        return abs(b_[0] - b_[1])

    lower_bound: float = 0
    upper_bound: float = np.min(goal / a_vec)

    while True:

        m: float = (upper_bound - lower_bound) / 2
        a: int = int(lower_bound + m)
        b: np.ndarray = (goal - (a * a_vec)) / b_vec

        if b[0] == b[1]:
            # found solution
            return np.array([a, int(b[0].item())])

        if int(lower_bound) == int(upper_bound):
            # no solution
            return np.zeros(2)

        m2: float = m / 2
        error_lower: float = error(lower_bound + m - m2)
        error_higher: float = error(lower_bound + m + m2)

        # adjust lower or upper bound based on smaller error
        if error_lower < error_higher:
            upper_bound = upper_bound - m
        else:
            lower_bound = lower_bound + m

def brute_force(file: Path, pt_two: bool = False):
    """
    Brute force binary search approach
    """
    data = read_input(file)
    data = np.array([i for t in data for i in t], dtype=int).reshape((-1, 6))
    A = data[:, :2]
    B = data[:, 2:4]
    G = data[:, 4:]

    if pt_two:
        G += int(1e+13)

    presses = np.empty((len(data), 2))
    for i in range(len(data)):

        presses[i] = binary_search(A[i], B[i], G[i])

    result = int(np.sum(presses * np.array([3, 1])).item())
    return result

def adj(m: np.ndarray):
    a = np.empty_like(m)

    a[:, 0, 0] = m[:, 1, 1]
    a[:, 0, 1] = -m[:, 0, 1]
    a[:, 1, 0] = -m[:, 1, 0]
    a[:, 1, 1] = m[:, 0, 0]

    return a

def equation_based(file: Path, pt_two: bool = False):
    data = read_input(file)
    data = np.array([[t[0], t[2], t[1], *t[3:]] for t in data], dtype=int).reshape((-1, 6))

    # A = [A.x B.x]
    #     [A.y B.y]
    A = data[:, :4].reshape((-1, 2, 2))

    # Calculate determinate of A
    # np.linalg.det() is to imprecise
    A_det = A[:, 0, 0] * A[:, 1, 1] - A[:, 0, 1] * A[:, 1, 0]

    # Calculate the adjugate matrix of A
    # A_adj = [ B.y -B.x]
    #         [-A.y  A.x]
    A_adj = adj(A)

    # Prize vector
    # B = [P.x P.y]
    B = data[:, 4:]

    if pt_two:
        B += int(1e+13)

    # A_adj * B
    X = A_adj @ B[:, :, None]

    # Solution is valid if a and b are integers
    # => (A_adj * B) mod det(A) == 0
    is_int = np.sum(X % A_det[:, None, None], axis=1).squeeze() == 0

    # Calculate a and b vector
    # X = (A_adj * B) / det(A)
    X = (X[is_int].squeeze() / A_det[is_int][:, None]).astype(int)

    # Multiply by weight and sum up
    W = np.array([3, 1]).T
    result = int(np.sum(X @ W).item())

    return result

def part_one_bf(file: Path):
    return brute_force(file)

def part_one_eq(file: Path):
    return equation_based(file)

def part_two_bf(file: Path):
    return brute_force(file, True)

def part_two_eq(file: Path):
    return equation_based(file, True)

def main():
    executor_bf = Executor(
        test_file=DATA / "t13.txt",
        input_file=DATA / "i13.txt",
        f1=part_one_bf,
        f2=part_two_bf
    )

    executor_eq = Executor(
        test_file=DATA / "t13.txt",
        input_file=DATA / "i13.txt",
        f1=part_one_eq,
        f2=part_two_eq
    )

    executor_bf.test_one(480)
    executor_eq.test_one(480)
    executor_bf.one("Binary Search")
    executor_eq.one("Linear Equation")

    executor_bf.two("Binary Search")
    executor_eq.two("Linear Equation")


if __name__ == "__main__":
    main()

