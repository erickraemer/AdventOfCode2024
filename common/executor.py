import timeit
from collections.abc import Callable
from pathlib import Path
from typing import Union, Iterable

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
    if str(time)[0] == '0':
        return f"{round(time*1000,2)}ms"

    return f"{round(time,2)}s"

def execute(test_input: Path, puzzle_input: Path, f: Callable[[Path], Union[int, Iterable]], test_expected: int, msg: str):
    test = f(test_input)

    if not isinstance(test, int):
        test = len(test)

    assert test == test_expected, f"Expected {test_expected}, got {test}"

    time, ret = timeit.Timer(lambda: f(puzzle_input)).timeit(1)

    if not isinstance(ret, int):
        ret = len(ret)

    print(f"{msg}: {ret}\n\t~ {scale_time(time)}\n")
