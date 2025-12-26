"""
This one was very easy and was simply just parsing the input. For part 1, just see if all counts don't exceed the max for
the given colors. For part 2, simply find the max count for each color.
"""
from collections import defaultdict

from utils import puzzle


_MAX_VALS = {
    'red': 12,
    'green': 13,
    'blue': 14
}



def is_possible(pull: tuple[int, str]) -> bool:
    return pull[0] <= _MAX_VALS[pull[1]]

def are_pulls_possible(pulls: list[tuple[int, str]]) -> bool:
    return all(is_possible(pull) for pull in pulls)

def is_game_possible(game: list[list[tuple[int, str]]]) -> bool:
    return all(are_pulls_possible(pull_set) for pull_set in game)


def parse_pull(pull) -> tuple[int, str]:
    vals = pull.split()
    return int(vals[0]), vals[1]

def parse_set(pull_set: str) -> list[tuple[int, str]]:
    vals = pull_set.strip().split(',')
    return [parse_pull(pull) for pull in vals]


@puzzle
def part1(puzzle_input: str):
    result = 0
    for line in puzzle_input:
        id_ = int(line[:line.index(':')][5:])
        pulls = [parse_set(pull_set) for pull_set in line[line.index(':') + 1:].strip().split(';')]
        if is_game_possible(pulls):
            result += id_

    print(result)


def power(game: list[list[tuple[int, str]]]) -> int:
    maxes = {
        'green': 0,
        'blue': 0,
        'red': 0
    }
    for pull_set in game:
        for count, color in pull_set:
            if count > maxes[color]:
                maxes[color] = count
    return maxes['green'] * maxes['blue'] * maxes['red']


@puzzle
def part2(puzzle_input: str):
    result = 0
    for line in puzzle_input:
        pulls = [parse_set(pull_set) for pull_set in line[line.index(':') + 1:].strip().split(';')]
        result += power(pulls)

    print(result)





if __name__ == '__main__':
    part2()