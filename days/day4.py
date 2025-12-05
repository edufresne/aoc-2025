"""
Day 4. What felt like an easy one. This one you simply just need to use grid positioning to check to see if you can remove the
paper towel if the # of adjacent paper towels is less than 4. Removal affecting other removal potentials just means that
you need to iterate through it until you have removed no more. I think there may be a way to optimize this by doing a
BFS instead of re-iterating to make this from O(nm^2) to a (nm log(nm)) search in which you find one to remove, then
see if it affects any adjacent paper towels in their removal.
"""
from utils import puzzle


def _get_adj_positions(grid: list[str] | list[list], row: int, col: int) -> list[tuple[int, int]]:
    n_rows = len(grid)
    n_cols = len(grid[0])
    return [pos for pos in [
        (row - 1, col - 1),
        (row - 1, col),
        (row, col - 1),
        (row -1, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row, col + 1),
        (row + 1, col + 1)
    ] if 0 <= pos[0] < n_rows and 0 <= pos[1] < n_cols]

@puzzle
def part1(puzzle_input):
    result = 0
    for i, row in enumerate(puzzle_input):
        for j, col in enumerate(row):
            val = puzzle_input[i][j]
            if val == '@':
                print(f'Towel found at: {(row, col)}')
                adj_count = 0
                for adj_row, adj_col in _get_adj_positions(puzzle_input, i, j):
                    if puzzle_input[adj_row][adj_col] == '@':
                        adj_count += 1
                if adj_count < 4:
                    result += 1
    print(result)


@puzzle
def part2(puzzle_input):
    grid = [[c for c in s] for s in puzzle_input]
    result = 0
    iteration = 1
    while True:
        removed = False
        print(f'Iteration: {iteration}')
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val == '@':
                    adj_count = 0
                    for adj_row, adj_col in _get_adj_positions(grid, i, j):
                        if grid[adj_row][adj_col] == '@':
                            adj_count += 1
                    if adj_count < 4:
                        result += 1
                        grid[i][j] = '.'
                        removed = True
                        print(f'Replaced at {i}, {j}')
        if not removed:
            break
        iteration += 1
    print(result)





if __name__ == '__main__':
    part2()