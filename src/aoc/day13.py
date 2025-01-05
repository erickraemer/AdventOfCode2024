import re
from pathlib import Path
from typing import Final

import numpy as np

from aoc import DATA
from aoc.common.executor import Executor

INPUT_REGX = re.compile(r"\D+(\d+)\D+(\d+)\n\D+(\d+)\D+(\d+)\n\D+(\d+)\D+(\d+)")

def read_input(file: Path) -> list[tuple]:
    
    data = open(file, "r").read()

    arcades = [
        tuple(int(c) for c in m)
        for m in INPUT_REGX.findall(data)
    ]

    return arcades


def part_one(file: Path) -> int:
    data = read_input(file)

    epsilon: Final[float] = 1e-10

    # Solve equation system by using cramer's rule
    # M     = [ A.X A.Y ]
    #         [ B.X B.Y ]
    #
    # M_hat = [  B.Y -B.X ]
    #         [ -A.Y  A.X ]
    #
    # P     = [ P.X / det(M) ]
    #         [ P.Y / det(M) ]
    #
    # [A, B].T = Ḿ * P

    # create arrays
    data = np.array([i for t in data for i in t]).reshape((-1, 6))
    M = data[:, :4].reshape((-1, 2, 2))
    P = data[:, 4:]

    # calculate solutions
    P = P / np.linalg.det(M)[:, None]
    M_hat = M[:,::-1,::-1] * np.array([[1, -1], [-1, 1]])
    results = (M_hat @ P[:, :, None]).squeeze()

    # ignore rounding errors smaller than epsilon
    # and ignore solutions which are not integers
    rounded = np.round(results, 0)
    rounded[np.abs(rounded - results) > epsilon] = 0

    # sum up all valid results
    tokens = int(np.sum(np.array([3, 1]) @ rounded.T))

    return tokens


def part_two(file: Path):
    pass

def main():
    executor = Executor(
        test_file=DATA / "t13.txt",
        input_file=DATA / "i13.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(480)
    executor.one("Tokens")


if __name__ == "__main__":
    main()

