import re
from pathlib import Path

from aoc import DATA
from aoc.common.executor import Executor

REGX = re.compile(r"[\d,]+")

def read_input(file: Path) -> tuple[int, int, int, list[int]]:
    data = open(file, "r").read()

    m = REGX.findall(data)
    prog = [int(i) for i in m[-1].split(",")]

    return int(m[0]), int(m[1]), int(m[2]), prog


class Processor:

    def __init__(self, r_a: int, r_b: int, r_c: int):
        self.reg: list[int] = [r_a, r_b, r_c]
        self.ip: int = 0
        self.output = []

        self.opc_map = {
            0: self._adv,
            1: self._bxl,
            2: self._bst,
            4: self._bxc,
            5: self._out,
            6: self._bdv,
            7: self._cdv
        }

    def execute(self, program: list[int]):
        self.ip = 0

        l = len(program)
        while self.ip < l:
            opc, opr = program[self.ip:self.ip+2]

            if opc == 3:
                if self.reg[0] != 0:
                    self.ip = opr
                    continue
            else:
                self.opc_map[opc](opr)

            self.ip += 2

        out = ",".join(self.output)
        return out

    def _combo(self, opr: int):

        if opr <= 3:
            return opr

        return self.reg[opr%4]

    def _dv(self, opr: int, r: int):
        self.reg[r] = self.reg[0] >> self._combo(opr)

    def _adv(self, opr: int):
        self._dv(opr, 0)

    def _bxl(self, opr: int):
        self.reg[1] = self.reg[1] ^ opr

    def _bst(self, opr: int):
        self.reg[1] = self._combo(opr) % 8

    def _bxc(self, opr: int):
        self.reg[1] = self.reg[1] ^ self.reg[2]

    def _out(self, opr: int):
        self.output.extend(
            list(str(self._combo(opr) % 8))
        )

    def _bdv(self, opr: int):
        self._dv(opr, 1)

    def _cdv(self, opr: int):
        self._dv(opr, 2)


def part_one(file: Path):
    r_a, r_b, r_c, prog = read_input(file)

    p = Processor(r_a, r_b, r_c)
    out = p.execute(prog)

    return out

def part_two(file: Path):
    pass

def main():
    executor = Executor(
        test_file=DATA / "t17.txt",
        input_file=DATA / "i17.txt",
        f1=part_one,
        f2=part_two
    )

    executor.test_one("4,6,3,5,6,3,5,2,1,0")
    executor.one("Program output")


if __name__ == "__main__":
    main()