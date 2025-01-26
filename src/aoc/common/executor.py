import logging
import timeit
from collections.abc import Callable
from numbers import Real
from pathlib import Path
from typing import Union, Iterable, Optional

_REPEATS = 10

timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""


def scale_time(time: float):
    ms = round(time * 1e+3, 2)
    if str(ms)[0] == '0':
        return f"{round(time * 1e+6, 2)}μs"

    if str(time)[0] == '0':
        return f"{ms}ms"

    if time < 60:
        return f"{round(time, 2)}s"

    return f"{int(time / 60)}m {int(time % 60)}s"


def _test(test_file: Path, f: Callable, expected_result: int, n: int, *args):
    time, ret = timeit.Timer(lambda: f(test_file, *args)).timeit(_REPEATS)
    time /= _REPEATS

    if not isinstance(ret, Real):
        ret = len(ret)

    if ret != expected_result:
        logging.error(f"~ Test {n} failed: Expected {expected_result}, got {ret}")
    else:
        logging.info(f"~ Test {n} passed ({scale_time(time)})")


def _execute(input_file: Path, f: Callable[[Path], Union[int, Iterable]], msg: str, *args):
    time, ret = timeit.Timer(lambda: f(input_file, *args)).timeit(_REPEATS)
    time /= _REPEATS

    if not isinstance(ret, Real):
        ret = len(ret)

    print(f"{msg}:\n\t- result: {ret}\n\t- runs: {_REPEATS}\n\t- avg time: {scale_time(time)}\n")


class Executor:

    def __init__(self, test_file: Optional[Path] = None, test_file_2: Optional[Path] = None,
                 input_file: Optional[Path] = None, f1: Optional[Callable] = None, f2: Optional[Callable] = None):
        self._test_file = test_file
        self._test_file_2 = test_file_2
        self._input_file = input_file
        self._f1 = f1
        self._f2 = f2

    def test_one(self, expected_result: int, *args):
        if not self._test_file.is_file():
            logging.warning(f"Test: {self._test_file} not found!")
            return

        _test(self._test_file, self._f1, expected_result, 1, *args)

    def test_two(self, expected_result: int, *args):
        test_file = self._test_file_2 if self._test_file_2 is not None else self._test_file

        if not test_file.is_file():
            logging.warning(f"Test: {test_file} not found!")
            return

        _test(test_file, self._f2, expected_result, 2, *args)

    def one(self, output_description: str, *args):
        if not self._input_file.is_file():
            logging.warning(f"Executor: {self._input_file} not found!")
            return

        _execute(self._input_file, self._f1, f"[1] {output_description}", *args)

    def two(self, output_description: str, *args):
        if not self._input_file.is_file():
            logging.warning(f"Executor: {self._input_file} not found!")
            return

        _execute(self._input_file, self._f2, f"[2] {output_description}", *args)
