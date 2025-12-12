"""
Hardest one so far omg. Works by sorting through all the areas of all the combinations of tile swaps. This forms a
rectangle. But the trick is, you need to see if the 2 vertices on the opposite corners fall inside the polygon created
by the coordinates. To do this you have to use ray tracing which you draw a line from that point in the same direction.
If that line intersects an even number of times, you are outside the polygon. You have to ignore certain edges if you
fall right on the vertex (so you don't double count) and you have to ignore completely parallel lines. Once you know
the four points are in the polygon, do one last check to ensure the edges they create don't intersect with anything. If
they do, the line draws outside the bounds of the polygon.
"""
from utils import puzzle


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
    tile_positions = [
        tuple(int(val) for val in line.split(",")) for line in puzzle_input
    ]
    lines = []
    for i, tile_position in enumerate(tile_positions):
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
        print(f"Original: {(pos1, pos2, area)}")
        corner1, corner2 = (pos1[0], pos2[1]), (pos2[0], pos1[1])
        if (
            _in_polygon(corner1, lines)
            and _in_polygon(corner2, lines)
            and not _crosses_any((pos1, corner1), lines)
            and not _crosses_any((pos2, corner1), lines)
            and not _crosses_any((pos1, corner2), lines)
            and not _crosses_any((pos2, corner2), lines)
        ):
            print(area)
            xs, ys = zip(*(tile_positions + [tile_positions[0]]))

            import plotly.graph_objects as go

            fig = go.Figure(go.Scatter(x=xs, y=ys, fill="toself"))
            fig.add_shape(
                type="rect",
                x0=min(corner1[0], corner2[0]),
                x1=max(corner1[0], corner2[0]),
                y0=min(corner1[1], corner2[1]),
                y1=max(corner1[1], corner2[1]),
                line=dict(color="red"),
            )
            fig.show()
            return


def _in_polygon(pos, lines: list[tuple[tuple, tuple]]) -> bool:
    for line in lines:
        if _is_on_line(line, pos):
            return True
    counter = 0
    for line in lines:
        if _intersects(line, pos):
            counter += 1
    return counter % 2 == 1


def _is_on_line(line, pos) -> bool:
    return (
        pos[0] == line[0][0]
        and min(line[0][1], line[1][1]) <= pos[1] <= max(line[0][1], line[1][1])
    ) or (
        pos[1] == line[0][1]
        and min(line[0][0], line[1][0]) <= pos[0] <= max(line[0][0], line[1][0])
    )


def _crosses_any(line, lines) -> bool:
    print(f"Testing line: {line}")
    for line2 in lines:
        if line == line2:
            continue
        if line[0][0] == line[1][0]:
            # Vertical
            if line2[0][0] == line2[1][0]:
                # Parallel
                continue
            if min(line2[0][0], line2[1][0]) < line[0][0] < max(
                line2[0][0], line2[1][0]
            ) and min(line[0][1], line[1][1]) < line2[0][1] < max(
                line[0][1], line[1][1]
            ):
                return True
        if line[0][1] == line[1][1]:
            # Horizontal
            if line2[0][1] == line[1][1]:
                # Parallel
                continue
            if min(line2[0][1], line2[1][1]) < line[0][1] < max(
                line2[0][1], line2[1][1]
            ) and min(line[0][0], line[1][0]) < line2[0][0] < max(
                line[0][0], line[1][0]
            ):
                return True

    return False


def _intersects(line, pos) -> bool:
    # If line is a horizontal line, do not count it
    if line[0][1] == line[1][1]:
        return False
    # If line is left of pos, do not count it
    if line[0][0] < pos[0]:
        return False
    return min(line[0][1], line[1][1]) <= pos[1] < max(line[0][1], line[1][1])


def _area(pos1, pos2):
    max_x = max(pos1[0], pos2[0])
    max_y = max(pos1[1], pos2[1])
    min_x = min(pos1[0], pos2[0])
    min_y = min(pos1[1], pos2[1])
    return (max_y - min_y + 1) * (max_x - min_x + 1)


if __name__ == "__main__":
    part2()
