from utils import puzzle


@puzzle
def part1(puzzle_input):
    ranges = []
    ids = []
    for line in puzzle_input:
        if line:
            if '-' in line:
                parts = line.split('-')
                ranges.append((int(parts[0].strip()), int(parts[1].strip())))
            else:
                ids.append(int(line))
    print(ranges)
    print(ids)
    result = 0
    for id_ in ids:
        if any(range[0] <= id_ <= range[1] for range in ranges):
            result += 1
    print(result)


@puzzle
def part2(puzzle_input):
    ranges = []
    for line in puzzle_input:
        if line:
            if '-' in line:
                parts = line.split('-')
                ranges.append((int(parts[0].strip()), int(parts[1].strip())))

    consolidated_ranges = []
    while ranges:
        r = ranges.pop()
        if not consolidated_ranges:
            consolidated_ranges.append(r)
        else:
            found = False
            for consolidated_range in consolidated_ranges:
                if consolidated_range[0] <= r[0] <= consolidated_range[1] or consolidated_range[0] <= r[1] <= consolidated_range[1] or r[0] <= consolidated_range[0] <= r[1] or r[0] <= consolidated_range[1] <= r[1]:
                    consolidated_ranges.remove(consolidated_range)
                    ranges.append((min(consolidated_range[0], r[0]), max(consolidated_range[1], r[1])))
                    print(f'Consolidating: {consolidated_range} + {r} = {ranges[-1]}')
                    found = True
                    break
            if not found:
                print(f'No duplicate. Adding: {r}')
                consolidated_ranges.append(r)

    answer = sum(r[1] - r[0] + 1 for r in consolidated_ranges)
    print(answer)






if __name__ == '__main__':
    part2()