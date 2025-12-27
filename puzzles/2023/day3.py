"""
Another two pointer but pretty easy one combined with cartisian coordinates. This one is probably just a warm up for
coordinate systems and crawling through them. No real algorithm here other than the two pointer to parse potential
values. There is a tricky thing here to account for which is for adjacent digits being of the same number which is why
you have to combine them.
"""

from utils import puzzle, adj_coords


def find_symbols(puzzle_input: list[str]) -> set[str]:
    s = set()
    for line in puzzle_input:
        for c in line:
            if c != "." and not c.isdigit():
                s.add(c)

    return s


@puzzle
def part1(puzzle_input):
    symbols = find_symbols(puzzle_input)
    result = 0
    s = ""
    adjacent_symbol = False
    for i, line in enumerate(puzzle_input):
        for j, c in enumerate(line):
            if c.isdigit():
                s += c
                if not adjacent_symbol and any(
                    puzzle_input[coord[0]][coord[1]] in symbols
                    for coord in adj_coords(puzzle_input, i, j)
                ):
                    adjacent_symbol = True
            elif s and adjacent_symbol:
                print(f"Found ID: {s}")
                result += int(s)
                s = ""
                adjacent_symbol = False
            else:
                s = ""
                adjacent_symbol = False
        if s and adjacent_symbol:
            print(f"Found ID: {s}")
            result += int(s)

        adjacent_symbol = False
        s = ""
    print(result)


@puzzle
def part2(puzzle_input):
    result = 0
    for i, line in enumerate(puzzle_input):
        for j, c in enumerate(line):
            value = puzzle_input[i][j]
            if value == "*":
                coords = adj_coords(puzzle_input, i, j)
                coords_with_numbers = [
                    coord
                    for coord in coords
                    if puzzle_input[coord[0]][coord[1]].isdigit()
                ]
                h_coords = [coord for coord in coords_with_numbers if coord[0] == i]
                below_coords = _merge_adj_horizontal(
                    [coord for coord in coords_with_numbers if coord[0] == i + 1]
                )
                above_coords = _merge_adj_horizontal(
                    [coord for coord in coords_with_numbers if coord[0] == i - 1]
                )
                all_coords = h_coords + below_coords + above_coords
                if len(all_coords) == 2:
                    print(f"Found gear ({i}, {j}): {all_coords}")
                    result += _parse_number(
                        puzzle_input, all_coords[0]
                    ) * _parse_number(puzzle_input, all_coords[1])

                else:
                    print(f"Ignoring gear ({i}, {j}): {all_coords}")

    print(result)


def _merge_adj_horizontal(coords: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if len(coords) == 3:
        # All are the same number because of adjacency
        return [coords[0]]
    elif len(coords) == 2:
        if abs(coords[0][1] - coords[1][1]) == 1:
            return [coords[0]]

    return coords


def _parse_number(puzzle_input: list[str], coord: tuple[int, int]) -> int:
    s = puzzle_input[coord[0]][coord[1]]
    i, j = coord[1] - 1, coord[1] + 1
    width = len(puzzle_input[0])
    while (0 <= i < width and puzzle_input[coord[0]][i].isdigit()) or (
        0 <= j < width and puzzle_input[coord[0]][j].isdigit()
    ):
        if puzzle_input[coord[0]][i].isdigit():
            s = puzzle_input[coord[0]][i] + s
            i -= 1
        if puzzle_input[coord[0]][j].isdigit():
            s = s + puzzle_input[coord[0]][j]
            j += 1
    return int(s)


if __name__ == "__main__":
    part2()
