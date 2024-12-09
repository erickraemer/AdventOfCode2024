from pathlib import Path


def read_input(file: Path) -> list[int]:

    data = open(file, "r").read()
    array = [int(c) for c in data]

    return array

def part_one(file: Path):
    array = read_input(file)

    unpacked = []
    # unpack
    for i, ic in enumerate(array):
        if i % 2 == 0:
            unpacked.extend([i // 2] * ic)
        else:
            unpacked.extend(['.'] * ic)

    i: int = 0
    j: int = len(unpacked) - 1
    # sort
    while i <= j:

        if unpacked[i] == '.':
            if unpacked[j] != '.':
                # swap
                unpacked[i], unpacked[j] = unpacked[j], unpacked[i]
                i += 1
            j -= 1
        else:
            i += 1

    # calculate checksum
    checksum = sum(i * c for i, c in enumerate(unpacked) if c != '.')

    return checksum


def part_two(file: Path):
    array = read_input(file)

    spaces: list[list] = []
    files: list[list] = []
    csum: int = 0
    # unpack
    for i, ic in enumerate(array):
        if i % 2 == 0:
            # start, size, id
            files.append([csum, int(ic), i//2])
        else:
            # start, size, id
            spaces.append([csum, int(ic), '.'])
        csum += ic

    # sort
    for k in range(len(files)-1, -1, -1):
        file = files[k]

        i = 0
        while i < len(spaces):
            space = spaces[i]

            if file[0] < space[0]:
                break

            if space[1] == 0:
                spaces.pop(i)
                continue

            if file[1] <= space[1]:
                spaces.append([file[0], file[1], '.'])
                files[k][0] = space[0]
                spaces[i][1] = space[1] - file[1]
                spaces[i][0] = space[0] + file[1]
                break

            i += 1

    unpacked = [
        t[2]  for t in sorted(spaces + files, key=lambda x: x[0]) for _ in range(t[1])
    ]

    # calculate checksum
    checksum = sum(i * c for i, c in enumerate(unpacked) if c != '.')

    return checksum


def main():
    test_one = part_one(Path("test.txt"))
    assert test_one == 1928, test_one

    po = part_one(Path("input.txt"))
    print(f"[1] Checksum: {po}")

    test_two = part_two(Path("test.txt"))
    assert test_two == 2858, test_two

    pt = part_two(Path("input.txt"))
    print(f"[2] Checksum: {pt}")

if __name__ == "__main__":
    main()