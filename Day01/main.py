import numpy as np


def main():
    l1 = []
    l2 = []

    # read input into two lists
    with open("input.txt", "r") as f:
        for line in f.readlines():
            out = line.split("   ")
            l1.append(int(out[0]))
            l2.append(int(out[1]))

    # check if both lists have the same length
    assert len(l1) == len(l2)

    # sort lists
    l1.sort()
    l2.sort()

    # convert lists into vectors
    v1 = np.array(l1, dtype=int)
    v2 = np.array(l2, dtype=int)

    # calculate the l1 norm between both vectors
    distance: int = int(np.sum(np.abs(v1 - v2)))

    print(f"Distance: {distance}")


if __name__ == "__main__":
    main()
