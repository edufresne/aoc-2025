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
    tile_positions = [tuple(int(val) for val in line.split(',')) for line in puzzle_input]
    lines = []
    for i, tile_position in enumerate(tile_positions + [tile_positions[0]]):
        last_position = tile_positions[i - 1]
        lines.append((last_position, tile_position))


    rectangles = []
    for i, pos1 in enumerate(tile_positions):
        for k, pos2 in enumerate(tile_positions):
            if i == k:
                continue

            area = _area(pos1, pos2)
            rectangles.append((pos1, pos2, area))

    rectangles = sorted(rectangles, key=lambda x: x[2])
    while rectangles:
        pos1, pos2, area = rectangles.pop()
        print(f'Original: {(pos1, pos2, area)}')
        corner1, corner2 = (pos1[0], pos2[1]), (pos2[0], pos1[1])
        print(f'Testing corners: {(corner1, corner2)}')
        if (corner1 in tile_positions or _in_polygon(corner1, lines)) and (corner2 in tile_positions or _in_polygon(corner2, lines)):
            print(area)
            return


def _in_polygon(pos, lines: list[tuple[tuple, tuple]]) -> bool:
    print(f'Testing: {pos} in polygon')
    for line in lines:
        if _point_intersects(line, pos):
            print(f'On edge of {line}')
            return True
    segments_to_trace = sorted([line for line in lines if line[0][0] == line[1][0] and min(line[0][1], line[1][1]) <= pos[1] < max(line[0][1], line[1][1])], key=lambda x: x[0][0])
    rays = 0
    last_dir = None
    for segment in segments_to_trace:
        min_y = min(segment[0][1], segment[1][1])
        max_y = max(segment[0][1], segment[1][1])
        if segment[0][1] == pos[1] and segment[0][1] == min_y or segment[1][1] == pos[1] and segment[1][1] == min_y:
            # Hit bottom
            current_dir = 'up'
            if current_dir == last_dir:
                rays += 1
                last_dir = None
            else:
                last_dir = current_dir
        elif segment[0][1] == pos[1] and segment[0][1] == max_y or segment[1][1] == pos[1] and segment[1][1] == max_y:
            current_dir = 'down'
            if current_dir == last_dir:
                rays += 1
                last_dir = None
            else:
                last_dir = current_dir
        else:
            last_dir = None
            rays += 1
    result = rays % 2 == 1
    print(f'Ray traced: {rays}. Is in polygon: {result}')
    return result


def _point_intersects(line: tuple[tuple, tuple], point: tuple[int, int]):
    min_x, max_x, min_y, max_y = min(line[0][0], line[1][0]), max(line[0][0], line[1][0]), min(line[0][1], line[1][1]), max(line[0][1], line[1][1])
    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y

def _area(pos1, pos2):
    max_x = max(pos1[0], pos2[0])
    max_y = max(pos1[1], pos2[1])
    min_x = min(pos1[0], pos2[0])
    min_y = min(pos1[1], pos2[1])
    return (max_y - min_y + 1) * (max_x - min_x + 1)


if __name__ == "__main__":
    part2()
