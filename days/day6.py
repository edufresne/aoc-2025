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








if __name__ == '__main__':
    part1()