import math
import re
from pathlib import Path

from aoc import DATA
from aoc.common.executor import Executor

_REGEX = re.compile(r"p=(-?\d+),(-?\d+)\sv=(-?\d+),(-?\d+)")
Coord = tuple[int, int]

def read_input(file: Path) -> list[list[int]]:
    data = open(file, "r").read()

    data = [[int(c) for c in m] for m in _REGEX.findall(data)]

    return data

def visualize(i: int, robots: list[list[int]], width: int, height: int):
    # requires numpy and opencv-python packages
    import cv2
    import numpy as np

    array = np.zeros((height, width))

    for robot in robots:
        x, y, vx, vy = robot
        px = (x + i * vx) % width
        py = (y + i * vy) % height

        array[py][px] += 1

    array[array > 1] = 1.0
    cv2.imshow("robots", array)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def part_one(file: Path, width: int = 101, height: int = 103):
    robots = read_input(file)

    iterations: int = 100
    quadrants: list[int] = [0] * 4

    for robot in robots:
        x, y, vx, vy = robot
        px = (x + iterations * vx) % width
        py = (y + iterations * vy) % height

        if px == (width // 2):
            continue

        if py == (height // 2):
            continue

        k = int(py > height / 2)
        l = int(px > width / 2)
        quadrants[k * 2 + l] += 1

    result: int = math.prod(quadrants)
    return result

def part_two(file: Path, viz=False):
    width: int = 101
    height: int = 103

    # tree appears periodically at every i value
    # find first appearance, i = 1
    i: int = 1

    k = int((88*width-12*height)/(width-height) + i*width*height)

    if viz:
        robots = read_input(file)
        visualize(k, robots, width, height)

    return k

def main():
    executor = Executor(
        test_file=DATA / "t14.txt",
        input_file=DATA / "i14.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one(12, 11, 7)
    executor.one("Safety Factor")

    executor.two("Easter egg")

if __name__ == "__main__":
    main()
