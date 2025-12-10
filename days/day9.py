from enum import Enum, StrEnum

from utils import puzzle


class Pivot(StrEnum):
    TOP_LEFT = "Top Left"
    TOP_RIGHT = "Top Right"
    BOTTOM_LEFT = "Bottom Left"
    BOTTOM_RIGHT = "Bottom Right"

    @classmethod
    def from_pos(cls, first: tuple[int, int], second: tuple[int, int], pos: tuple[int, int]):
        if pos[0] <= first[0] and pos[0] <= second[0] and pos[1] <= first[1] and pos[1] <= second[1]:
            return Pivot.BOTTOM_LEFT
        if pos[0] >= first[0] and pos[0] >= second[0] and pos[1] >= first[1] and pos[1] >= second[1]:
            return Pivot.TOP_RIGHT
        if pos[0] <= first[0] and pos[0] <= second[0] and pos[1] >= first[1] and pos[1] >= second[1]:
            return Pivot.TOP_LEFT
        return Pivot.BOTTOM_RIGHT


@puzzle
def part1(puzzle_input):
    tile_positions = [
        tuple(int(val) for val in line.split(",")) for line in puzzle_input
    ]
    print(tile_positions)

    area = 0
    for i, pos1 in enumerate(tile_positions):
        for j, pos2 in enumerate(tile_positions):
            if i == j:
                continue
            this_area = _area(pos1, pos2)
            if this_area > area:
                area = this_area

    print(area)


@puzzle
def part2(puzzle_input):
    tile_positions = [
        tuple(int(val) for val in line.split(",")) for line in puzzle_input
    ]
    border_positions = {tile_positions[0]}
    for i, tile_position in enumerate(tile_positions + [tile_positions[0]]):
        border_positions.add(tile_position)
        last_position = tile_positions[i - 1]
        if tile_position[0] == last_position[0]:
            for j in range(
                min(tile_position[1], last_position[1]),
                max(tile_position[1], last_position[1]),
            ):
                border_positions.add((tile_position[0], j))
        else:
            for j in range(
                min(tile_position[0], last_position[0]),
                max(tile_position[0], last_position[0]),
            ):
                border_positions.add((j, tile_position[1]))

    area = 0
    answer1, answer2 = None, None
    for i, pos1 in enumerate(tile_positions):
        for j, pos2 in enumerate(tile_positions):
            if i == j:
                continue
            this_area = _area(pos1, pos2)
            corner1, corner2 = (pos1[0], pos2[1]), (pos2[0], pos1[1])
            if (
                this_area > area
                and _validate_border_positions(corner1, Pivot.from_pos(pos1, pos2, corner1), border_positions)
                and _validate_border_positions(corner2, Pivot.from_pos(pos1, pos2, corner2), border_positions)
            ):
                area = this_area
                answer1, answer2 = pos1, pos2
        print(f'Testing: {i}, {j}')

    print(f"{answer1} and {answer2}")
    print(area)


def _validate_border_positions(
    starting_point: tuple[int, int],
    pivot: Pivot,
    border_positions: set[tuple[int, int]],
) -> bool:
    if starting_point in border_positions:
        return True
    if pivot == Pivot.TOP_LEFT or pivot == Pivot.TOP_RIGHT:
        border_position_above = next((border_position for border_position in border_positions if border_position[0] == starting_point[0] and border_position[1] >= starting_point[1]), None)
        if border_position_above is None:
            return False
    if pivot == Pivot.BOTTOM_LEFT or pivot == Pivot.BOTTOM_RIGHT:
        border_position_below = next((border_position for border_position in border_positions if border_position[0] == starting_point[0] and border_position[1] <= starting_point[1]), None)
        if border_position_below is None:
            return False
    if pivot == Pivot.TOP_LEFT or pivot == Pivot.BOTTOM_LEFT:
        border_position_left = next((border_position for border_position in border_positions if border_position[1] == starting_point[1] and border_position[0] <= starting_point[1]), None)
        if border_position_left is None:
            return False
    if pivot == Pivot.TOP_RIGHT or pivot == Pivot.BOTTOM_RIGHT:
        border_position_right = next((border_position for border_position in border_positions if border_position[1] == starting_point[1] and border_position[0] >= starting_point[1]), None)
        if border_position_right is None:
            return False
    return True




# @puzzle
# def part2(puzzle_input):
#     tile_positions = [tuple(int(val) for val in line.split(',')) for line in puzzle_input]
#     print(tile_positions)
#     # Looking for missing 9,3 which should be between
#     border_positions = {tile_positions[0]}
#     for i, tile_position in enumerate(tile_positions + [tile_positions[0]]):
#         border_positions.add(tile_position)
#         last_position = tile_positions[i - 1]
#         if tile_position[0] == last_position[0]:
#             for j in range(min(tile_position[1], last_position[1]), max(tile_position[1], last_position[1])):
#                 border_positions.add((tile_position[0], j))
#         else:
#             for j in range(min(tile_position[0], last_position[0]), max(tile_position[0], last_position[0])):
#                 border_positions.add((j, tile_position[1]))
#
#     for i, pos1 in enumerate(tile_positions):
#         for j, pos2 in enumerate(tile_positions):
#             if i == j:
#                 continue
#             corner1, corner2 = (pos1[0], pos2[1]), (pos2[0], pos1[1])
#             if corner1 in border_positions and corner2 in border_positions:
#                 for x in range(min(corner1[0], corner2[0]), max(corner1[0], corner2[0]) + 1):
#                     for y in range(min(corner1[1], corner2[1]), max(corner1[1], corner2[1]) + 1):
#                         border_positions.add((x, y))
#             print(f'i={i}, j={j}')
#
#     area = 0
#     answer1, answer2 = None, None
#     for i, pos1 in enumerate(tile_positions):
#         for j, pos2 in enumerate(tile_positions):
#             if i == j:
#                 continue
#             this_area = _area(pos1, pos2)
#             corner1, corner2 = (pos1[0], pos2[1]), (pos2[0], pos1[1])
#             if this_area > area and corner1 in border_positions and corner2 in border_positions:
#                 area = this_area
#                 answer1, answer2 = pos1, pos2
#
#     print(f'{answer1} and {answer2}')
#     print(area)


def _area(pos1, pos2):
    max_x = max(pos1[0], pos2[0])
    max_y = max(pos1[1], pos2[1])
    min_x = min(pos1[0], pos2[0])
    min_y = min(pos1[1], pos2[1])
    return (max_y - min_y + 1) * (max_x - min_x + 1)


if __name__ == "__main__":
    part2()
