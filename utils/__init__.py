import os.path
import re
from pathlib import Path
from typing import Callable

_REGEX = re.compile(r'day(\d+).py$')


def puzzle(f: Callable) -> Callable:
    def _callable() -> None:
        file_name = f.__code__.co_filename
        cache_dir = Path(__file__).parents[1].joinpath('.puzzle_cache')
        if not cache_dir.exists():
            os.makedirs(cache_dir)

        match = _REGEX.search(file_name)
        if not match:
            raise ValueError(f'Cannot determine puzzle day for file: {file_name}')
        value = match.group(1)
        cache_filename = cache_dir.joinpath(f'{value}.txt')
        if not cache_filename.exists():
            raise ValueError(f'Missing puzzle input for day: {value}')
        else:
            puzzle_input = cache_filename.read_text()
        f(puzzle_input=puzzle_input.splitlines())
    return _callable



