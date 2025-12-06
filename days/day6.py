from utils import puzzle

@puzzle
def part1(puzzle_input):
    cols = []
    ops = []
    for line in puzzle_input:
        if '*' in line or '+' in line:
            ops.extend([val.strip() for val in line.split() if val.strip()])
        else:
            items = [int(val.strip()) for val in line.split() if val.strip()]
            print(items)
            if not cols:
                cols = [[] for _ in range(len(items))]
            for k, item in enumerate(items):
                cols[k].append(item)

    total = 0
    for i, op in enumerate(ops):
        if op == '+':
            total += sum(cols[i])
        else:
            col_total = cols[i][0]
            for item in cols[i][1:]:
                col_total *= item
            total += col_total

    print(total)

@puzzle
def part2(puzzle_input):
    max_length = max([len(item) for item in puzzle_input[:-1]])
    ops = [val.strip() for val in puzzle_input[-1].split() if val.strip()][::-1]
    cols = []

    padded_input = []
    # Add RHS padding to allow for right to left enumeration
    for i, item in enumerate(puzzle_input[:-1]):
        if len(item) < max_length:
            item += ' ' * (max_length - len(item))
        padded_input.append(item)

    current_col = []
    for i in range(max_length):
        index = max_length - i - 1
        digit_found = False
        s = ""
        for line in padded_input:
            if line[index].isdigit():
                digit_found = True
                s += line[index]
        if s:
            current_col.append(int(s))

        if not digit_found:
            cols.append(current_col)
            current_col = []
    if current_col:
        cols.append(current_col)
    print(cols)
    total = 0
    for i, op in enumerate(ops):
        if op == '+':
            total += sum(cols[i])
        else:
            col_total = cols[i][0]
            for item in cols[i][1:]:
                col_total *= item
            total += col_total
    print(total)










if __name__ == '__main__':
    part2()