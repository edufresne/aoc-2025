"""
I mis-interpreted part2 here and thought we could go over the joltage levels so I developed an algorithm to find the
minimum by always pressing the next button that reduces the remaining joltage goals the most. Turns out they need to
be set exactly. Because of this, I used the solution found here:
https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/.

Which finds the pattern in which you get all even remaining goals as you know that you can just duplicate press the
rest of the buttons since in part 1 you could compute which unique buttons to press. There seems to be another linear
algebra function using gaussian elimination.
"""
import itertools
import re
from collections import defaultdict
from copy import copy, deepcopy
from functools import cache

from utils import puzzle


@puzzle
def part1(machines: list[str]):
    """
    A couple notes.
    - Probably have to put everything into a lookup map. Look up the current state, figure out which ones need to be
    toggled on. This will essentially turn into a directed acyclic graph. Acyclic because doing two presses of the same
    button yields nothing so it's wasted presses.
    """
    result = 0
    for machine in machines:
        i = machine.find("]")
        j = machine.find("{")
        lights = {i: c == "#" for i, c in enumerate(machine[1:i])}
        buttons = [
            tuple(
                int(val)
                for val in item.strip().replace("(", "").replace(")", "").split(",")
            )
            for item in machine[i + 1 : j].split()
            if item.strip()
        ]
        for length in range(1, len(buttons) + 1):
            found = False
            combos = list(itertools.combinations(buttons, length))
            for combo in combos:
                current = {i: False for i in range(len(lights))}
                for button in combo:
                    for light in button:
                        current[light] = not current[light]
                if current == lights:
                    print(length)
                    result += length
                    found = True
                    break
            if found:
                break
    print(result)


from functools import cache
from itertools import combinations


def patterns(coeffs: list[tuple[int, ...]]) -> dict[tuple[int, ...], int]:
    out = {}
    num_buttons = len(coeffs)
    num_variables = len(coeffs[0])
    for pattern_len in range(num_buttons + 1):
        for buttons in combinations(range(num_buttons), pattern_len):
            pattern = tuple(
                map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons)))
            )
            if pattern not in out:
                out[pattern] = pattern_len
    return out


def solve_single(coeffs: list[tuple[int, ...]], goal: tuple[int, ...]) -> int:
    pattern_costs = patterns(coeffs)

    @cache
    def solve_single_aux(goal: tuple[int, ...]) -> int:
        if all(i == 0 for i in goal):
            return 0
        answer = 1000000
        for pattern, pattern_cost in pattern_costs.items():
            if all(i <= j and i % 2 == j % 2 for i, j in zip(pattern, goal)):
                new_goal = tuple((j - i) // 2 for i, j in zip(pattern, goal))
                answer = min(answer, pattern_cost + 2 * solve_single_aux(new_goal))
        return answer

    return solve_single_aux(goal)


def solve(raw: str):
    answer = 0
    lines = raw.splitlines()
    for I, L in enumerate(lines, 1):
        _, *coeffs, goal = L.split()
        goal = tuple(int(i) for i in goal[1:-1].split(","))
        coeffs = [[int(i) for i in r[1:-1].split(",")] for r in coeffs]
        coeffs = [tuple(int(i in r) for i in range(len(goal))) for r in coeffs]

        subanswer = solve_single(coeffs, goal)
        print(f"Line {I}/{len(lines)}: answer {subanswer}")
        answer += subanswer
    print(answer)


@puzzle
def part2(machines: list[str]):
    """
    A couple notes.
    - Probably have to put everything into a lookup map. Look up the current state, figure out which ones need to be
    toggled on. This will essentially turn into a directed acyclic graph. Acyclic because doing two presses of the same
    button yields nothing so it's wasted presses. Best answer so far: 20526
    """
    answer = 0
    for I, L in enumerate(machines, 1):
        _, *coeffs, goal = L.split()
        goal = tuple(int(i) for i in goal[1:-1].split(","))
        coeffs = [[int(i) for i in r[1:-1].split(",")] for r in coeffs]
        coeffs = [tuple(int(i in r) for i in range(len(goal))) for r in coeffs]

        subanswer = solve_single(coeffs, goal)
        print(f'Line {I}/{len(machines)}: answer {subanswer}')
        answer += subanswer
    print(answer)


def _check_function(goals, buttons: list[tuple]) -> None:
    current = list(goals)
    for button in buttons:
        for value in button:
            current[value] -= 1
    assert all(value <= 0 for value in current)


if __name__ == "__main__":
    part2()
